#!/usr/bin/env python3
"""
Weekly Scheduler for CSV Download and Prospect Overlap Analysis

This script runs every Sunday night to download the last 7 days of data
from all client APIs and perform overlap analysis.
"""

import schedule
import time
import logging
import sys
from datetime import datetime, timedelta
from main import CSVProcessingApp
import os

class WeeklyScheduler:
    """Weekly scheduler for automated CSV processing"""
    
    def __init__(self):
        self.setup_logging()
        self.app = CSVProcessingApp()
    
    def setup_logging(self):
        """Setup logging for the weekly scheduler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('weekly_scheduler.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_weekly_analysis(self):
        """Execute the weekly CSV download and overlap analysis"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("🗓️ WEEKLY ANALYSIS STARTING - Sunday Night Run")
            self.logger.info("=" * 60)
            
            start_time = datetime.now()
            
            # Calculate the date range (last 7 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            self.logger.info(f"📅 Data range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            self.logger.info(f"👥 Configured clients: {len(self.app.client_configs)}")
            
            # List all clients
            for client_config in self.app.client_configs:
                client_name = client_config.get('name', 'unknown')
                sources = []
                if client_config.get('rb2b_api_key'): sources.append('RB2B')
                if client_config.get('heyreach_api_key'): sources.append('HeyReach')
                if client_config.get('instantly_api_key'): sources.append('Instantly')
                self.logger.info(f"   • {client_name}: {', '.join(sources)}")
            
            # Run overlap analysis pipeline
            self.logger.info("🔍 Starting prospect overlap analysis pipeline...")
            downloaded_files = self.app.download_csvs(days_back=7)
            
            if not downloaded_files:
                self.logger.error("❌ No CSV files were downloaded successfully")
                return
            
            self.logger.info(f"📥 Downloaded {len(downloaded_files)} CSV files")
            
            # Perform overlap analysis
            overlap_results = self.app.analyze_prospect_overlaps(downloaded_files)
            
            if 'error' in overlap_results:
                self.logger.error(f"❌ Overlap analysis failed: {overlap_results['error']}")
                return
            
            # Log results summary
            summary = overlap_results.get('summary', {})
            
            self.logger.info("📊 WEEKLY ANALYSIS RESULTS:")
            self.logger.info("-" * 40)
            
            # Sources analyzed
            sources_analyzed = summary.get('sources_analyzed', [])
            self.logger.info(f"Data sources: {', '.join(sources_analyzed)}")
            
            # Records by source
            total_records = 0
            for source, count in summary.get('total_records_by_source', {}).items():
                self.logger.info(f"   • {source}: {count:,} records")
                total_records += count
            
            self.logger.info(f"Total records processed: {total_records:,}")
            
            # Overlaps found
            total_overlaps = 0
            overlap_details = summary.get('total_overlaps_by_identifier', {})
            
            if overlap_details:
                self.logger.info("🔍 Overlaps discovered:")
                for identifier_type, count in overlap_details.items():
                    self.logger.info(f"   • {identifier_type}: {count:,} overlaps")
                    total_overlaps += count
            
            if total_overlaps > 0:
                self.logger.info(f"🎯 TOTAL OVERLAPS: {total_overlaps:,}")
                
                # Find most common overlap type
                if overlap_details:
                    top_overlap = max(overlap_details.items(), key=lambda x: x[1])
                    self.logger.info(f"Most common overlap: {top_overlap[0]} ({top_overlap[1]:,} matches)")
            else:
                self.logger.info("⚠️ No overlaps found between data sources")
            
            # Report file locations
            if overlap_results.get('csv_report_path'):
                self.logger.info(f"📋 CSV report: {overlap_results['csv_report_path']}")
            
            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.info(f"⏱️ Analysis completed in {duration:.2f} seconds")
            self.logger.info(f"📁 All results saved in: {self.app.processed_dir}")
            
            # Send summary email (if configured)
            self.send_weekly_summary_email(summary, total_overlaps, duration)
            
            self.logger.info("=" * 60)
            self.logger.info("✅ WEEKLY ANALYSIS COMPLETED SUCCESSFULLY")
            self.logger.info("=" * 60)
            
        except Exception as e:
            self.logger.error(f"❌ Error in weekly analysis: {e}")
            self.logger.exception("Full error details:")
    
    def send_weekly_summary_email(self, summary: dict, total_overlaps: int, duration: float):
        """Send weekly summary email (placeholder for email integration)"""
        # This is a placeholder - implement email sending if needed
        self.logger.info("📧 Weekly summary email would be sent here")
        
        # You can implement email sending using smtplib or a service like SendGrid
        # Example structure:
        # - Total clients processed
        # - Total records analyzed
        # - Number of overlaps found
        # - Top overlap types
        # - Links to detailed reports
    
    def start_weekly_schedule(self, run_time: str = "22:00"):
        """
        Start weekly scheduled execution every Sunday night
        
        Args:
            run_time: Time to run in HH:MM format (default: 22:00 - 10 PM)
        """
        self.logger.info(f"🕙 Starting weekly scheduler - runs every Sunday at {run_time}")
        self.logger.info("Press Ctrl+C to stop the scheduler")
        
        # Schedule for every Sunday at the specified time
        schedule.every().sunday.at(run_time).do(self.run_weekly_analysis)
        
        # Log next run time
        next_run = schedule.next_run()
        self.logger.info(f"📅 Next scheduled run: {next_run}")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("🛑 Weekly scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Scheduler error: {e}")
    
    def run_now_and_schedule(self, run_time: str = "22:00"):
        """Run analysis immediately and then start weekly schedule"""
        self.logger.info("🚀 Running analysis immediately, then starting weekly schedule...")
        
        # Run immediately
        self.run_weekly_analysis()
        
        # Start weekly schedule
        self.start_weekly_schedule(run_time)

def main():
    """Main entry point for the weekly scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Weekly scheduler for CSV download and prospect overlap analysis"
    )
    
    parser.add_argument(
        '--time',
        type=str,
        default='22:00',
        help='Time for Sunday runs in HH:MM format (default: 22:00 - 10 PM)'
    )
    
    parser.add_argument(
        '--run-now',
        action='store_true',
        help='Run analysis immediately before starting the weekly schedule'
    )
    
    parser.add_argument(
        '--test-run',
        action='store_true',
        help='Run analysis once and exit (no scheduling)'
    )
    
    args = parser.parse_args()
    
    # Initialize scheduler
    scheduler = WeeklyScheduler()
    
    try:
        if args.test_run:
            # Test run only
            print("🧪 Running test analysis...")
            scheduler.run_weekly_analysis()
            
        elif args.run_now:
            # Run now and schedule
            scheduler.run_now_and_schedule(args.time)
            
        else:
            # Start weekly schedule only
            scheduler.start_weekly_schedule(args.time)
    
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Scheduler error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()