#!/usr/bin/env python3
"""
Setup SMTP for actual email sending
"""

import os

def setup_smtp_config():
    """Configure SMTP settings for sending emails"""
    
    print("📧 SMTP Configuration Options:")
    print("1. Gmail (recommended)")
    print("2. Outlook/Hotmail")
    print("3. Custom SMTP")
    
    print("\n🔧 For Gmail:")
    print("1. Go to https://myaccount.google.com/apppasswords")
    print("2. Generate an 'App Password' for this application")
    print("3. Use your Gmail address and the app password")
    
    print("\n📝 Add these to your .env file:")
    print("SMTP_SERVER=smtp.gmail.com")
    print("SMTP_PORT=587")
    print("SENDER_EMAIL=your-email@gmail.com")
    print("SENDER_PASSWORD=your-app-password")
    
    print("\n✅ Once configured, emails will be sent automatically!")
    print("🕕 Daily emails will start tomorrow at 6:00 AM")

if __name__ == "__main__":
    setup_smtp_config()
