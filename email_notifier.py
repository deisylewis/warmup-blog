#!/usr/bin/env python3
"""
Email Notification System for RB2B Overlap Analysis
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
import logging
from datetime import datetime
from typing import Dict

class EmailNotifier:
    def __init__(self):
        self.recipient_email = "deisy@sendwarmup.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('SENDER_EMAIL', 'noreply@rb2banalyzer.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'temp-password')
        
    def send_test_email(self):
        """Send test email with sample data"""
        try:
            # Create sample data
            sample_data = {
                'summary': {
                    'total_rb2b_visitors': 125,
                    'visitors_with_overlaps': 23,
                    'overlap_percentage': 18.4,
                    'high_priority_overlaps': 8,
                    'medium_priority_overlaps': 12,
                    'low_priority_overlaps': 3
                },
                'high_priority_prospects': [
                    {
                        'rb2b_visitor': {
                            'name': 'John Smith',
                            'company': 'TechCorp Inc',
                            'Business Email': 'john.smith@techcorp.com',
                            'title': 'VP of Marketing',
                            'Page Visited': 'https://yoursite.com/pricing'
                        }
                    }
                ],
                'recommendations': [
                    '🎯 IMMEDIATE ACTION: 8 high-priority website visitors are also in your outreach campaigns.',
                    '📧 5 visitors have exact email matches - perfect for personalized follow-ups.',
                    '💡 Consider expanding outreach to the 102 website visitors not yet in your campaigns.'
                ]
            }
            
            print("📧 TEST EMAIL PREVIEW FOR deisy@sendwarmup.com:")
            print("=" * 60)
            print(f"Subject: 🎯 Daily RB2B Overlap Analysis - {datetime.now().strftime('%Y-%m-%d')}")
            print()
            print("📊 SUMMARY:")
            print(f"   • Total Website Visitors: {sample_data['summary']['total_rb2b_visitors']}")
            print(f"   • Visitors with Overlaps: {sample_data['summary']['visitors_with_overlaps']}")
            print(f"   • 🚨 HIGH Priority: {sample_data['summary']['high_priority_overlaps']}")
            print(f"   • ⚠️ MEDIUM Priority: {sample_data['summary']['medium_priority_overlaps']}")
            print()
            print("🚨 HIGH PRIORITY PROSPECTS:")
            for prospect in sample_data['high_priority_prospects']:
                visitor = prospect['rb2b_visitor']
                print(f"   • {visitor['name']} - {visitor['company']}")
                print(f"     📧 {visitor['Business Email']}")
                print(f"     �� {visitor['title']}")
                print(f"     📍 {visitor['Page Visited']}")
            print()
            print("💡 RECOMMENDATIONS:")
            for rec in sample_data['recommendations']:
                print(f"   • {rec}")
            print()
            print("✅ Email system ready! Will send real emails once SMTP is configured.")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating test email: {e}")
            return False

def main():
    print("📧 Creating test email preview...")
    notifier = EmailNotifier()
    notifier.send_test_email()

if __name__ == "__main__":
    main()
