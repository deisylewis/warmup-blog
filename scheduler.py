#!/usr/bin/env python3
"""
Scheduler for automated CSV download and OpenAI processing

This script allows you to schedule the CSV processing pipeline to run
at regular intervals using the schedule library.
"""

import schedule
import time
import logging
import sys
from datetime import datetime
from main import CSVProcessingApp

class CSVScheduler:
    """Scheduler for automated CSV processing"""
    
    def __init__(self, sources=None, analysis_type="insights", prompt=None):
        self.sources = sources or ['rb2b', 'heyreach']
        self.analysis_type = analysis_type
        self.prompt = prompt
        self.app = CSVProcessingApp()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the scheduler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scheduler.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_pipeline(self):
        """Execute the CSV processing pipeline"""
        try:
            self.logger.info("Scheduled pipeline execution starting...")
            start_time = datetime.now()
            
            result = self.app.run_full_pipeline(
                sources=self.sources,
                prompt=self.prompt,
                analysis_type=self.analysis_type
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            if result['success']:
                self.logger.info(f"Scheduled pipeline completed successfully in {duration:.2f} seconds")
                self.logger.info(f"Files downloaded: {result['summary']['files_downloaded']}")
                self.logger.info(f"Files processed: {result['summary']['files_processed']}")
            else:
                self.logger.error(f"Scheduled pipeline failed: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            self.logger.error(f"Error in scheduled pipeline execution: {e}")
    
    def start_hourly_schedule(self):
        """Start hourly scheduled execution"""
        self.logger.info("Starting hourly schedule...")
        schedule.every().hour.do(self.run_pipeline)
        self._run_scheduler()
    
    def start_daily_schedule(self, time_str="09:00"):
        """Start daily scheduled execution at specified time"""
        self.logger.info(f"Starting daily schedule at {time_str}...")
        schedule.every().day.at(time_str).do(self.run_pipeline)
        self._run_scheduler()
    
    def start_interval_schedule(self, minutes=30):
        """Start interval-based scheduled execution"""
        self.logger.info(f"Starting interval schedule every {minutes} minutes...")
        schedule.every(minutes).minutes.do(self.run_pipeline)
        self._run_scheduler()
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        self.logger.info("Scheduler started. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"Scheduler error: {e}")

def main():
    """Main entry point for the scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Schedule automated CSV download and OpenAI processing"
    )
    
    parser.add_argument(
        '--schedule-type',
        choices=['hourly', 'daily', 'interval'],
        default='daily',
        help='Type of schedule (default: daily)'
    )
    
    parser.add_argument(
        '--time',
        type=str,
        default='09:00',
        help='Time for daily schedule in HH:MM format (default: 09:00)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=30,
        help='Interval in minutes for interval schedule (default: 30)'
    )
    
    parser.add_argument(
        '--sources',
        nargs='+',
        choices=['rb2b', 'heyreach'],
        default=['rb2b', 'heyreach'],
        help='Sources to download from (default: both)'
    )
    
    parser.add_argument(
        '--analysis-type',
        choices=['insights', 'summary', 'custom', 'compare'],
        default='insights',
        help='Type of OpenAI analysis to perform (default: insights)'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        help='Custom prompt for OpenAI processing (required for custom analysis)'
    )
    
    parser.add_argument(
        '--run-now',
        action='store_true',
        help='Run the pipeline once immediately before starting the schedule'
    )
    
    args = parser.parse_args()
    
    # Validate custom analysis requirements
    if args.analysis_type == 'custom' and not args.prompt:
        print("Error: --prompt is required for custom analysis type")
        sys.exit(1)
    
    # Initialize scheduler
    scheduler = CSVScheduler(
        sources=args.sources,
        analysis_type=args.analysis_type,
        prompt=args.prompt
    )
    
    try:
        # Run immediately if requested
        if args.run_now:
            print("Running pipeline immediately...")
            scheduler.run_pipeline()
        
        # Start the appropriate schedule
        if args.schedule_type == 'hourly':
            scheduler.start_hourly_schedule()
        elif args.schedule_type == 'daily':
            scheduler.start_daily_schedule(args.time)
        elif args.schedule_type == 'interval':
            scheduler.start_interval_schedule(args.interval)
    
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Scheduler error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()