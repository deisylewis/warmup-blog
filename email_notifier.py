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
        
    def send_overlap_report(self, analysis_data):
        """Send detailed overlap report with all prospect names and companies"""
        try:
            print(f"📧 SENDING DETAILED OVERLAP REPORT TO: {self.recipient_email}")
            print("=" * 70)
            
            # Create detailed email content
            email_content = self.create_detailed_email_content(analysis_data)
            
            print("EMAIL CONTENT PREVIEW:")
            print(email_content)
            print("\n✅ Email ready to send!")
            print("🔧 Configure SMTP settings to send actual emails")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating overlap report: {e}")
            return False
    
    def send_test_email(self):
        """Send test email with sample data"""
        try:
            # Create sample data with detailed prospect information
            sample_data = {
                'summary': {
                    'total_rb2b_visitors': 223,
                    'visitors_with_overlaps': 127,
                    'overlap_percentage': 56.95,
                    'high_priority_overlaps': 61,
                    'medium_priority_overlaps': 66,
                    'low_priority_overlaps': 0
                },
                'high_priority_prospects': [
                    {
                        'rb2b_visitor': {
                            'name': 'Janis Moriarty',
                            'company': 'Medical Professional Liability Association',
                            'Business Email': 'jmoriarty@mplassociation.org',
                            'title': 'Dental Section Member',
                            'Page Visited': 'https://coya.life/new-year-2025/',
                            'Linked In URL ': 'https://www.linkedin.com/in/janismoriartydmd'
                        },
                        'matches': [
                            {'source_type': 'Email campaigns', 'match_types': ['email', 'name']}
                        ],
                        'priority': 'HIGH'
                    },
                    {
                        'rb2b_visitor': {
                            'name': 'Sarah Shapiro',
                            'company': 'Shapiro Venture Partners',
                            'Business Email': 'sarah.shapiro@clorox.com',
                            'title': 'Board Member',
                            'Page Visited': 'https://coya.life/new-year-2025/',
                            'Linked In URL ': 'https://www.linkedin.com/in/sarahshapiro'
                        },
                        'matches': [
                            {'source_type': 'LinkedIn campaigns', 'match_types': ['linkedin', 'company']}
                        ],
                        'priority': 'HIGH'
                    },
                    {
                        'rb2b_visitor': {
                            'name': 'Cory Sloss',
                            'company': 'Baker Electric, Inc.',
                            'Business Email': 'csloss@bakerelectric.com',
                            'title': 'President',
                            'Page Visited': 'https://coya.life/new-year-2025/',
                            'Linked In URL ': 'https://www.linkedin.com/in/corysloss'
                        },
                        'matches': [
                            {'source_type': 'Email campaigns', 'match_types': ['email']}
                        ],
                        'priority': 'HIGH'
                    }
                ],
                'medium_priority_prospects': [
                    {
                        'rb2b_visitor': {
                            'name': 'Anne Robertson',
                            'company': 'East Bay Asian Local Development Corporation',
                            'Business Email': '',
                            'title': 'Executive & Board Operations Manager',
                            'Page Visited': 'https://coya.life/new-year-2025/',
                            'Linked In URL ': 'https://www.linkedin.com/in/annerobertson67'
                        },
                        'matches': [
                            {'source_type': 'LinkedIn campaigns', 'match_types': ['name']}
                        ],
                        'priority': 'MEDIUM'
                    }
                ],
                'recommendations': [
                    '🎯 IMMEDIATE ACTION: 61 high-priority website visitors are also in your outreach campaigns.',
                    '📧 Multiple visitors have exact email matches - perfect for personalized follow-ups.',
                    '📊 REVIEW: 66 medium-priority overlaps may represent the same prospects with different contact information.',
                    '💡 Consider expanding outreach to the 96 website visitors not yet in your campaigns.'
                ]
            }
            
                                    return self.send_overlap_report(sample_data)
    
    def create_detailed_email_content(self, analysis_data):
        """Create detailed email content with all prospect information"""
        summary = analysis_data.get('summary', {})
        high_priority = analysis_data.get('high_priority_prospects', [])
        medium_priority = analysis_data.get('medium_priority_prospects', [])
        recommendations = analysis_data.get('recommendations', [])
        
        content = f"""
📧 DAILY RB2B OVERLAP ANALYSIS REPORT
To: {self.recipient_email}
Subject: 🎯 Daily RB2B Overlap Analysis - {datetime.now().strftime('%Y-%m-%d')}

═══════════════════════════════════════════════════════════════════

📊 EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════════
• Total RB2B Website Visitors: {summary.get('total_rb2b_visitors', 0)}
• Visitors with Overlaps: {summary.get('visitors_with_overlaps', 0)} ({summary.get('overlap_percentage', 0)}%)
• 🚨 HIGH Priority Overlaps: {summary.get('high_priority_overlaps', 0)}
• ⚠️ MEDIUM Priority Overlaps: {summary.get('medium_priority_overlaps', 0)}
• ✅ LOW Priority Overlaps: {summary.get('low_priority_overlaps', 0)}

🚨 HIGH PRIORITY PROSPECTS (IMMEDIATE ACTION REQUIRED)
═══════════════════════════════════════════════════════════════════
"""
        
        # Add all high priority prospects with full details
        if high_priority:
            for i, prospect in enumerate(high_priority, 1):
                visitor = prospect.get('rb2b_visitor', {})
                matches = prospect.get('matches', [])
                
                content += f"""
{i}. {visitor.get('name', 'Unknown Name')} - {visitor.get('company', 'Unknown Company')}
   📧 Email: {visitor.get('Business Email', 'No email available')}
   💼 Title: {visitor.get('title', 'No title available')}
   🔗 LinkedIn: {visitor.get('Linked In URL ', 'No LinkedIn available')}
   📍 Page Visited: {visitor.get('Page Visited', 'No page data')}
   🎯 Found in: {', '.join([m.get('source_type', 'Unknown') for m in matches])}
   🔍 Match Types: {', '.join([str(m.get('match_types', [])) for m in matches])}
"""
        else:
            content += "\n   No high priority overlaps found.\n"
        
        # Add medium priority prospects
        if medium_priority:
            content += f"""
⚠️ MEDIUM PRIORITY PROSPECTS (REVIEW RECOMMENDED)
═══════════════════════════════════════════════════════════════════
"""
            for i, prospect in enumerate(medium_priority[:10], 1):  # Show top 10 medium priority
                visitor = prospect.get('rb2b_visitor', {})
                matches = prospect.get('matches', [])
                
                content += f"""
{i}. {visitor.get('name', 'Unknown Name')} - {visitor.get('company', 'Unknown Company')}
   📧 Email: {visitor.get('Business Email', 'No email available')}
   💼 Title: {visitor.get('title', 'No title available')}
   📍 Page Visited: {visitor.get('Page Visited', 'No page data')}
   🎯 Found in: {', '.join([m.get('source_type', 'Unknown') for m in matches])}
"""
            
            if len(medium_priority) > 10:
                content += f"\n... and {len(medium_priority) - 10} more medium priority prospects.\n"
        
        # Add recommendations
        if recommendations:
            content += f"""
💡 RECOMMENDATIONS
═══════════════════════════════════════════════════════════════════
"""
            for i, rec in enumerate(recommendations, 1):
                content += f"{i}. {rec}\n"
        
        # Add next steps
        content += f"""
📋 IMMEDIATE NEXT STEPS
═══════════════════════════════════════════════════════════════════
1. 🚨 URGENT: Review all {summary.get('high_priority_overlaps', 0)} high priority prospects
2. 📧 Coordinate messaging to avoid prospect fatigue
3. 🎯 Use website visit data to personalize follow-ups
4. 📊 Update your HeyReach and Instantly campaigns accordingly
5. 💬 Consider reaching out to prospects who visited but aren't in campaigns

📈 GROWTH OPPORTUNITIES
═══════════════════════════════════════════════════════════════════
• Website visitors NOT in campaigns: {summary.get('total_rb2b_visitors', 0) - summary.get('visitors_with_overlaps', 0)}
• These are warm prospects ready for outreach!

═══════════════════════════════════════════════════════════════════
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
System: RB2B Overlap Analysis (Last 7 days)
═══════════════════════════════════════════════════════════════════
"""
        
        return content
             
    def old_test_preview(self):
        """Old test preview method"""
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
