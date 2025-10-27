#!/usr/bin/env python3
"""
Email System for RB2B Overlap Analysis - Send to deisy@sendwarmup.com
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime

class RB2BEmailer:
    def __init__(self):
        self.recipient = "deisy@sendwarmup.com"
        # Using a free SMTP service for testing
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "rb2b.analyzer@gmail.com"  # Will need real credentials
        self.sender_password = "your_app_password"     # Will need real password
        
    def send_detailed_report(self, analysis_data):
        """Send detailed overlap report with all prospect names and companies"""
        
        # Create the detailed email content
        email_content = self.create_detailed_email(analysis_data)
        
        # For now, print the email since we don't have SMTP configured
        print("📧 EMAIL READY TO SEND TO: deisy@sendwarmup.com")
        print("=" * 80)
        print(email_content)
        print("=" * 80)
        print("✅ Email system ready! Configure SMTP to send actual emails.")
        
        return True
    
    def create_detailed_email(self, data):
        """Create detailed email with all prospect information"""
        
        summary = data.get('summary', {})
        high_priority = data.get('high_priority_prospects', [])
        medium_priority = data.get('medium_priority_prospects', [])
        recommendations = data.get('recommendations', [])
        
        email_body = f"""
To: deisy@sendwarmup.com
From: RB2B Overlap Analysis System
Subject: 🎯 Daily RB2B Overlap Analysis - {datetime.now().strftime('%B %d, %Y')}

═══════════════════════════════════════════════════════════════════════════════
📊 DAILY RB2B OVERLAP ANALYSIS REPORT
═══════════════════════════════════════════════════════════════════════════════

📈 EXECUTIVE SUMMARY:
• Total RB2B Website Visitors: {summary.get('total_rb2b_visitors', 0)}
• Visitors with Overlaps: {summary.get('visitors_with_overlaps', 0)} ({summary.get('overlap_percentage', 0)}%)
• 🚨 HIGH Priority Overlaps: {summary.get('high_priority_overlaps', 0)}
• ⚠️ MEDIUM Priority Overlaps: {summary.get('medium_priority_overlaps', 0)}

🚨 HIGH PRIORITY PROSPECTS (IMMEDIATE ACTION REQUIRED)
═══════════════════════════════════════════════════════════════════════════════
"""
        
        if high_priority:
            for i, prospect in enumerate(high_priority, 1):
                visitor = prospect.get('rb2b_visitor', {})
                matches = prospect.get('matches', [])
                
                email_body += f"""
{i}. {visitor.get('name', 'Unknown Name')} - {visitor.get('company', 'Unknown Company')}
   📧 Email: {visitor.get('Business Email', 'No email available')}
   💼 Title: {visitor.get('title', 'No title available')}
   🔗 LinkedIn: {visitor.get('Linked In URL ', 'No LinkedIn available')}
   📍 Page Visited: {visitor.get('Page Visited', 'No page data')}
   🎯 Found in: {', '.join([m.get('source_type', 'Unknown') for m in matches])}
   🔍 Match Types: {', '.join([str(m.get('match_types', [])) for m in matches])}
"""
        else:
            email_body += "\n   ✅ No high priority overlaps found - all website visitors are new prospects!\n"
        
        if medium_priority:
            email_body += f"""
⚠️ MEDIUM PRIORITY PROSPECTS (REVIEW RECOMMENDED)  
═══════════════════════════════════════════════════════════════════════════════
"""
            for i, prospect in enumerate(medium_priority[:15], 1):  # Show top 15
                visitor = prospect.get('rb2b_visitor', {})
                matches = prospect.get('matches', [])
                
                email_body += f"""
{i}. {visitor.get('name', 'Unknown Name')} - {visitor.get('company', 'Unknown Company')}
   📧 Email: {visitor.get('Business Email', 'No email available')}
   💼 Title: {visitor.get('title', 'No title available')}
   📍 Page Visited: {visitor.get('Page Visited', 'No page data')}
   🎯 Found in: {', '.join([m.get('source_type', 'Unknown') for m in matches])}
"""
            
            if len(medium_priority) > 15:
                email_body += f"\n... and {len(medium_priority) - 15} more medium priority prospects.\n"
        
        if recommendations:
            email_body += f"""
💡 RECOMMENDATIONS & IMMEDIATE ACTIONS
═══════════════════════════════════════════════════════════════════════════════
"""
            for i, rec in enumerate(recommendations, 1):
                email_body += f"{i}. {rec}\n"
        
        email_body += f"""
📋 NEXT STEPS FOR TODAY
═══════════════════════════════════════════════════════════════════════════════
1. 🚨 URGENT: Review all {summary.get('high_priority_overlaps', 0)} high priority prospects above
2. 📧 Coordinate messaging between HeyReach and Instantly to avoid prospect fatigue  
3. 🎯 Use the "Page Visited" data to personalize your follow-up messages
4. 📊 Update your campaign sequences based on these overlaps
5. 💬 Consider reaching out to the {summary.get('total_rb2b_visitors', 0) - summary.get('visitors_with_overlaps', 0)} visitors NOT in campaigns

📈 GROWTH OPPORTUNITY
═══════════════════════════════════════════════════════════════════════════════
• Website visitors NOT in campaigns: {summary.get('total_rb2b_visitors', 0) - summary.get('visitors_with_overlaps', 0)}
• These are warm prospects who visited your site but aren't in outreach yet!
• Perfect candidates for immediate campaign addition

═══════════════════════════════════════════════════════════════════════════════
📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
🔄 Next Report: Tomorrow at 6:00 AM  
📊 Data Source: Last 7 days of RB2B website visitors
═══════════════════════════════════════════════════════════════════════════════

Questions about this report? Reply to this email or check your system logs.
        """
        
        return email_body

def send_test_email():
    """Send test email with current real data"""
    
    # Get the latest analysis data
    try:
        with open('processed/rb2b_priority_analysis_20250722_044637.json', 'r') as f:
            real_data = json.load(f)
        print("📊 Using real analysis data from your latest run...")
    except:
        # Fallback to sample data
        real_data = {
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
                    'matches': [{'source_type': 'Email campaigns', 'match_types': ['email', 'name']}],
                    'priority': 'HIGH'
                }
            ],
            'recommendations': [
                '🎯 IMMEDIATE ACTION: 61 high-priority website visitors are also in your outreach campaigns.',
                '📧 Multiple visitors have exact email matches - perfect for personalized follow-ups.',
                '💡 Consider expanding outreach to website visitors not yet in campaigns.'
            ]
        }
        print("📊 Using sample data for email preview...")
    
    emailer = RB2BEmailer()
    emailer.send_detailed_report(real_data)

if __name__ == "__main__":
    print("📧 CREATING DETAILED EMAIL FOR deisy@sendwarmup.com")
    print("=" * 60)
    send_test_email()
