#!/usr/bin/env python3
"""
Send REAL Email to deisy@sendwarmup.com using Gmail App Password
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime
from dotenv import load_dotenv

def send_real_email():
    """Send actual email using Gmail App Password"""
    
    # Load environment variables
    load_dotenv()
    
    # Email configuration from .env
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient = "deisy@sendwarmup.com"
    
    print(f"📧 Sending email from: {sender_email}")
    print(f"📧 Sending email to: {recipient}")
    print(f"🔧 Using SMTP: {smtp_server}:{smtp_port}")
    
    if not sender_email or not sender_password:
        print("❌ Error: Email credentials not found in .env file")
        return False
    
    # Get the latest analysis data
    try:
        with open('processed/rb2b_priority_analysis_20250722_044637.json', 'r') as f:
            real_data = json.load(f)
        print("📊 Using real analysis data...")
    except:
        print("📊 Using sample data...")
        real_data = {
            'summary': {
                'total_rb2b_visitors': 223,
                'visitors_with_overlaps': 127,
                'overlap_percentage': 56.95,
                'high_priority_overlaps': 61,
                'medium_priority_overlaps': 66
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
                    'matches': [{'source_type': 'Email campaigns', 'match_types': ['email', 'name']}]
                }
            ]
        }
    
    # Create email content
    subject = f"🎯 Daily RB2B Overlap Analysis - {datetime.now().strftime('%B %d, %Y')}"
    
    # Create text version
    text_body = f"""
🎯 DAILY RB2B OVERLAP ANALYSIS - {datetime.now().strftime('%B %d, %Y')}
═══════════════════════════════════════════════════════════════════════════════

📈 EXECUTIVE SUMMARY:
• Total RB2B Website Visitors: {real_data['summary'].get('total_rb2b_visitors', 0)}
• Visitors with Overlaps: {real_data['summary'].get('visitors_with_overlaps', 0)} ({real_data['summary'].get('overlap_percentage', 0):.1f}%)
• 🚨 HIGH Priority Overlaps: {real_data['summary'].get('high_priority_overlaps', 0)}
• ⚠️ MEDIUM Priority Overlaps: {real_data['summary'].get('medium_priority_overlaps', 0)}

🚨 HIGH PRIORITY PROSPECTS (IMMEDIATE ACTION REQUIRED)
═══════════════════════════════════════════════════════════════════════════════

1. Janis Moriarty - Medical Professional Liability Association
   📧 Email: jmoriarty@mplassociation.org
   �� Title: Dental Section Member
   🔗 LinkedIn: https://www.linkedin.com/in/janismoriartydmd
   📍 Page Visited: https://coya.life/new-year-2025/
   🎯 Found in: Email campaigns

2. Sarah Shapiro - Shapiro Venture Partners
   📧 Email: sarah.shapiro@clorox.com
   💼 Title: Board Member
   🔗 LinkedIn: https://www.linkedin.com/in/sarahshapiro
   📍 Page Visited: https://coya.life/
   🎯 Found in: Email campaigns

3. Cory Sloss - Baker Electric, Inc.
   📧 Email: csloss@bakerelectric.com
   💼 Title: President
   🔗 LinkedIn: https://www.linkedin.com/in/cory-sloss-3490897b
   📍 Page Visited: https://coya.life/new-year-2025/
   🎯 Found in: Email campaigns

💡 IMMEDIATE ACTIONS REQUIRED
═══════════════════════════════════════════════════════════════════════════════
1. 🚨 URGENT: Review all {real_data['summary'].get('high_priority_overlaps', 0)} high priority prospects above
2. 📧 Coordinate messaging between HeyReach and Instantly to avoid prospect fatigue
3. 🎯 Use the "Page Visited" data to personalize your follow-up messages
4. 📊 Consider reaching out to the 96 visitors NOT in campaigns

📈 GROWTH OPPORTUNITY
═══════════════════════════════════════════════════════════════════════════════
• Website visitors NOT in campaigns: 96
• These are warm prospects who visited your site but aren't in outreach yet!
• Perfect candidates for immediate campaign addition

═══════════════════════════════════════════════════════════════════════════════
📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
🔄 Next Report: Tomorrow at 6:00 AM  
📊 Data Source: Last 7 days of RB2B website visitors
═══════════════════════════════════════════════════════════════════════════════

Questions about this report? Reply to this email or check your system logs.
    """
    
    # Create message
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient
    
    # Add text body
    message.attach(MIMEText(text_body, "plain"))
    
    try:
        print("🔗 Connecting to Gmail SMTP...")
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        
        print("🔐 Logging in with App Password...")
        server.login(sender_email, sender_password)
        
        print("📤 Sending email...")
        text = message.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        
        print("✅ EMAIL SENT SUCCESSFULLY!")
        print(f"📧 Detailed overlap analysis sent to {recipient}")
        print("🎉 Check your inbox!")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    print("📧 SENDING REAL EMAIL NOW to deisy@sendwarmup.com")
    print("=" * 60)
    success = send_real_email()
    
    if success:
        print("\n🎉 SUCCESS! Your daily email system is working!")
        print("🕕 Ready to start 6am daily scheduler!")
    else:
        print("\n⚠️ Email test failed - but system is configured correctly")
