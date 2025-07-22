#!/usr/bin/env python3
"""
Daily 6am Scheduler for RB2B Overlap Analysis
Runs every day at 6am, analyzes last 7 days of data, emails results to deisy@sendwarmup.com
"""

import schedule
import time
import logging
import sys
from datetime import datetime, timedelta
from rb2b_priority_analyzer import RB2BPriorityAnalyzer
from email_notifier import EmailNotifier
import json
import os

class Daily6AMScheduler:
    """Daily scheduler for 6am RB2B overlap analysis"""
    
    def __init__(self):
        self.setup_logging()
        self.analyzer = RB2BPriorityAnalyzer()
        self.email_notifier = EmailNotifier()
        self.rb2b_sheets_url = "https://docs.google.com/spreadsheets/d/1jPwTgvGwQEG9llkpKgWu8PNYXY-OaUMUvNYGxIWUe0I/edit?gid=0#gid=0"
    
    def setup_logging(self):
        """Setup logging for the daily scheduler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('daily_scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_daily_analysis(self):
        """Run the daily RB2B overlap analysis"""
        try:
            self.logger.info("🌅 Starting daily 6am RB2B overlap analysis...")
            
            # Run the analysis
            result = self.analyzer.analyze_rb2b_priority_overlaps(
                self.rb2b_sheets_url, 
                "webhook_data"
            )
            
            if result['success']:
                self.logger.info("✅ Analysis completed successfully")
                
                # Load the detailed report
                report_data = result.get('report', {})
                
                # Send email notification
                self.logger.info("📧 Sending email notification to deisy@sendwarmup.com...")
                
                # Send detailed email with all prospect information
                email_sent = self.email_notifier.send_overlap_report(report_data)
                
                if email_sent:
                    self.logger.info("✅ Email notification sent successfully")
                else:
                    self.logger.error("❌ Failed to send email notification")
                
                # Also log the results for backup
                self.log_daily_results(report_data)
                
                self.logger.info("✅ Daily analysis and notification complete!")
                
            else:
                self.logger.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.logger.error(f"❌ Error in daily analysis: {e}")
    
    def log_daily_results(self, report_data):
        """Log daily results (will be replaced with email when SMTP configured)"""
        summary = report_data.get('summary', {})
        high_priority = report_data.get('high_priority_prospects', [])
        recommendations = report_data.get('recommendations', [])
        
        self.logger.info("📊 DAILY ANALYSIS RESULTS:")
        self.logger.info(f"   • Total RB2B Website Visitors: {summary.get('total_rb2b_visitors', 0)}")
        self.logger.info(f"   • Visitors with Overlaps: {summary.get('visitors_with_overlaps', 0)}")
        self.logger.info(f"   • Overlap Percentage: {summary.get('overlap_percentage', 0)}%")
        self.logger.info(f"   • 🚨 HIGH Priority Overlaps: {summary.get('high_priority_overlaps', 0)}")
        self.logger.info(f"   • ⚠️ MEDIUM Priority Overlaps: {summary.get('medium_priority_overlaps', 0)}")
        
        if high_priority:
            self.logger.info("🚨 HIGH PRIORITY PROSPECTS:")
            for i, prospect in enumerate(high_priority[:5]):  # Log top 5
                visitor = prospect.get('rb2b_visitor', {})
                self.logger.info(f"   {i+1}. {visitor.get('name', 'Unknown')} - {visitor.get('company', 'Unknown')}")
                self.logger.info(f"      📧 {visitor.get('Business Email', 'N/A')}")
                self.logger.info(f"      💼 {visitor.get('title', 'N/A')}")
        
        if recommendations:
            self.logger.info("💡 RECOMMENDATIONS:")
            for rec in recommendations:
                self.logger.info(f"   • {rec}")
        
        # Save daily summary to file
        daily_summary = {
            'date': datetime.now().isoformat(),
            'summary': summary,
            'high_priority_count': len(high_priority),
            'recommendations': recommendations
        }
        
        summary_file = f"daily_summaries/summary_{datetime.now().strftime('%Y%m%d')}.json"
        os.makedirs("daily_summaries", exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(daily_summary, f, indent=2, default=str)
        
        self.logger.info(f"💾 Daily summary saved: {summary_file}")
    
    def start_scheduler(self):
        """Start the daily scheduler"""
        self.logger.info("�� Setting up daily scheduler for 6:00 AM...")
        
        # Schedule daily run at 6:00 AM
        schedule.every().day.at("06:00").do(self.run_daily_analysis)
        
        self.logger.info("✅ Scheduler started! Next run: Tomorrow at 6:00 AM")
        self.logger.info("📧 Results will be emailed to: deisy@sendwarmup.com")
        self.logger.info("📊 Analysis covers: Last 7 days of data")
        self.logger.info("🔄 Press Ctrl+C to stop the scheduler")
        
        # Run the scheduler
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
                # Log status every hour
                if datetime.now().minute == 0:
                    next_run = schedule.next_run()
                    if next_run:
                        self.logger.info(f"⏰ Scheduler running. Next analysis: {next_run.strftime('%Y-%m-%d at %I:%M %p')}")
                    
            except KeyboardInterrupt:
                self.logger.info("👋 Scheduler stopped by user")
                break
            except Exception as e:
                self.logger.error(f"❌ Scheduler error: {e}")
                time.sleep(60)  # Wait a minute before retrying
    
    def run_test_now(self):
        """Run a test analysis immediately"""
        self.logger.info("🧪 Running test analysis now...")
        self.run_daily_analysis()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Daily 6am RB2B Overlap Analysis Scheduler')
    parser.add_argument('--test-now', action='store_true', help='Run analysis immediately for testing')
    parser.add_argument('--start-scheduler', action='store_true', help='Start the daily 6am scheduler')
    
    args = parser.parse_args()
    
    scheduler = Daily6AMScheduler()
    
    if args.test_now:
        print("🧪 RUNNING TEST ANALYSIS NOW...")
        scheduler.run_test_now()
    elif args.start_scheduler:
        print("🕕 STARTING DAILY 6AM SCHEDULER...")
        scheduler.start_scheduler()
    else:
        print("📋 DAILY 6AM SCHEDULER")
        print("=" * 40)
        print("Options:")
        print("  --test-now        Run analysis immediately")
        print("  --start-scheduler Start daily 6am scheduler")
        print("")
        print("Examples:")
        print("  python3 daily_6am_scheduler.py --test-now")
        print("  python3 daily_6am_scheduler.py --start-scheduler")

if __name__ == "__main__":
    main()
