#!/usr/bin/env python3
"""
Simple Webhook Test Script
This creates a temporary webhook URL for testing with HeyReach
"""

import requests
import json
import time

def create_webhook_site():
    """Create a temporary webhook URL using webhook.site"""
    try:
        # Create a new webhook.site endpoint
        response = requests.post('https://webhook.site/token')
        if response.status_code == 201:
            data = response.json()
            webhook_url = f"https://webhook.site/{data['uuid']}"
            admin_url = f"https://webhook.site/#!/{data['uuid']}"
            
            print("🎯 TEMPORARY WEBHOOK CREATED!")
            print("=" * 50)
            print(f"📡 HeyReach Webhook URL: {webhook_url}")
            print(f"👀 View Requests At: {admin_url}")
            print("=" * 50)
            print()
            print("📋 INSTRUCTIONS:")
            print("1. Copy the webhook URL above")
            print("2. Add it to your HeyReach webhook settings")
            print("3. Open the admin URL to see incoming data")
            print("4. Test by sending data from HeyReach")
            print()
            
            return webhook_url, admin_url
        else:
            print("❌ Failed to create webhook.site endpoint")
            return None, None
            
    except Exception as e:
        print(f"❌ Error creating webhook: {e}")
        return None, None

def main():
    print("🚀 Creating Temporary Webhook for HeyReach Testing...")
    print()
    
    webhook_url, admin_url = create_webhook_site()
    
    if webhook_url:
        print("✅ SUCCESS! Your temporary webhook is ready!")
        print()
        print("🔄 This webhook will:")
        print("   - Receive data from HeyReach")
        print("   - Show you exactly what data is being sent")
        print("   - Help us understand the data format")
        print()
        print("⏰ This webhook will stay active for 7 days")
        print("📞 Once we see the data format, we can set up the permanent system")
        
        # Keep the script running and check for data
        print("\n🔍 Monitoring for incoming webhooks... (Press Ctrl+C to stop)")
        try:
            while True:
                time.sleep(30)
                print(".", end="", flush=True)
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped.")
    else:
        print("❌ Could not create temporary webhook. Let's try a different approach.")

if __name__ == "__main__":
    main()