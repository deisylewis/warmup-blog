#!/usr/bin/env python3
"""
Demo script to create sample Instantly data for testing overlap analysis
"""

import pandas as pd
import json
from datetime import datetime

def create_demo_instantly_data():
    """Create demo Instantly email campaign data"""
    
    # Sample Instantly data - some prospects overlap with HeyReach
    instantly_data = [
        {
            "email": "sameer.khan@techcorp.com",  # Same person as HeyReach, different email
            "first_name": "Sameer",
            "last_name": "Khan Mohammed", 
            "full_name": "Sameer Khan Mohammed",
            "company": "TechCorp Inc",
            "position": "Senior DevOps Engineer",
            "campaign_name": "Tech Professionals Q1",
            "campaign_id": "camp_001",
            "status": "replied",
            "sent_date": "2025-07-20T10:30:00Z",
            "response_date": "2025-07-20T14:22:00Z"
        },
        {
            "email": "jason@gomaxone.com",  # Same email as HeyReach sender
            "first_name": "Jason",
            "last_name": "Mejeur",
            "full_name": "Jason Mejeur", 
            "company": "GoMaxOne",
            "position": "Sales Director",
            "campaign_name": "Sales Outreach 2025",
            "campaign_id": "camp_002", 
            "status": "opened",
            "sent_date": "2025-07-19T09:15:00Z"
        },
        {
            "email": "mike.johnson@startup.io",
            "first_name": "Mike",
            "last_name": "Johnson",
            "full_name": "Mike Johnson",
            "company": "Startup.io",
            "position": "CTO",
            "campaign_name": "Tech Leaders Campaign",
            "campaign_id": "camp_003",
            "status": "bounced",
            "sent_date": "2025-07-18T16:45:00Z"
        },
        {
            "email": "sarah.wilson@consulting.com",
            "first_name": "Sarah", 
            "last_name": "Wilson",
            "full_name": "Sarah Wilson",
            "company": "Wilson Consulting",
            "position": "Managing Partner",
            "campaign_name": "Executive Outreach",
            "campaign_id": "camp_004",
            "status": "clicked",
            "sent_date": "2025-07-17T11:20:00Z"
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(instantly_data)
    
    # Add required fields
    df['source'] = 'Email campaigns'
    df['client_name'] = 'test_client'
    df['api_timestamp'] = datetime.now().isoformat()
    
    # Save as CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"webhook_data/test_client_instantly_email_campaigns_{timestamp}.csv"
    df.to_csv(filename, index=False)
    
    print(f"✅ Created demo Instantly data: {filename}")
    print(f"📊 Records: {len(df)}")
    print("\n🔍 Sample data:")
    print(df[['full_name', 'email', 'company', 'campaign_name', 'status']].head())
    
    return filename

if __name__ == "__main__":
    create_demo_instantly_data()