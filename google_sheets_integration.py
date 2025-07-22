#!/usr/bin/env python3
"""
Google Sheets Integration for RB2B Data
Reads RB2B website visitor data from Google Sheets for overlap analysis
"""

import requests
import pandas as pd
import csv
import io
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import re

class GoogleSheetsRB2BIntegration:
    """Integration to read RB2B data from Google Sheets"""
    
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def get_csv_url_from_sheets_url(self, sheets_url: str) -> str:
        """
        Convert Google Sheets URL to CSV export URL
        
        Args:
            sheets_url: Google Sheets URL
            
        Returns:
            CSV export URL
        """
        # Extract the spreadsheet ID from the URL
        pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, sheets_url)
        
        if not match:
            raise ValueError("Invalid Google Sheets URL")
        
        spreadsheet_id = match.group(1)
        
        # Extract gid (sheet ID) if present
        gid_pattern = r'gid=(\d+)'
        gid_match = re.search(gid_pattern, sheets_url)
        gid = gid_match.group(1) if gid_match else '0'
        
        # Create CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"
        
        return csv_url
    
    def download_rb2b_data_from_sheets(self, sheets_url: str, client_name: str = "rb2b_client") -> Optional[str]:
        """
        Download RB2B data from Google Sheets
        
        Args:
            sheets_url: Google Sheets URL
            client_name: Client name for tagging
            
        Returns:
            Path to saved CSV file or None if failed
        """
        try:
            self.logger.info(f"Downloading RB2B data from Google Sheets for client: {client_name}")
            
            # Convert to CSV export URL
            csv_url = self.get_csv_url_from_sheets_url(sheets_url)
            self.logger.info(f"CSV export URL: {csv_url}")
            
            # Download CSV data
            response = requests.get(csv_url, timeout=30)
            response.raise_for_status()
            
            # Parse CSV data
            csv_data = io.StringIO(response.text)
            df = pd.read_csv(csv_data)
            
            self.logger.info(f"Downloaded {len(df)} rows from Google Sheets")
            
            # Clean and process the data
            df = self.process_rb2b_data(df, client_name)
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"webhook_data/{client_name}_rb2b_website_visitors_{timestamp}.csv"
            
            # Create directory if it doesn't exist
            import os
            os.makedirs("webhook_data", exist_ok=True)
            
            df.to_csv(filename, index=False)
            
            self.logger.info(f"Saved RB2B data to: {filename}")
            self.logger.info(f"Data preview:\n{df.head()}")
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Error downloading RB2B data from Google Sheets: {e}")
            return None
    
    def process_rb2b_data(self, df: pd.DataFrame, client_name: str) -> pd.DataFrame:
        """
        Process and standardize RB2B data from Google Sheets
        
        Args:
            df: Raw DataFrame from Google Sheets
            client_name: Client name for tagging
            
        Returns:
            Processed DataFrame
        """
        try:
            # Add source and client labels
            df['source'] = 'Website visitors'
            df['client_name'] = client_name
            df['sheets_timestamp'] = datetime.now().isoformat()
            
            # Standardize column names (common RB2B fields)
            column_mapping = {
                'Email': 'email',
                'email': 'email',
                'Email Address': 'email',
                'Company': 'company',
                'company': 'company',
                'Company Name': 'company',
                'Name': 'name',
                'name': 'name',
                'Full Name': 'full_name',
                'First Name': 'first_name',
                'Last Name': 'last_name',
                'LinkedIn': 'linkedin_url',
                'LinkedIn URL': 'linkedin_url',
                'linkedin_url': 'linkedin_url',
                'Title': 'title',
                'title': 'title',
                'Job Title': 'title',
                'Position': 'title',
                'Visit Date': 'visit_date',
                'visit_date': 'visit_date',
                'Date': 'visit_date',
                'Page Views': 'page_views',
                'page_views': 'page_views',
                'Time on Site': 'time_on_site',
                'Location': 'location',
                'location': 'location',
                'Industry': 'industry',
                'industry': 'industry'
            }
            
            # Rename columns if they exist
            for old_name, new_name in column_mapping.items():
                if old_name in df.columns:
                    df = df.rename(columns={old_name: new_name})
            
            # Clean email addresses
            if 'email' in df.columns:
                df['email'] = df['email'].astype(str).str.lower().str.strip()
                # Remove invalid emails
                df = df[df['email'] != 'nan']
                df = df[df['email'].str.contains('@', na=False)]
            
            # Clean company names
            if 'company' in df.columns:
                df['company'] = df['company'].astype(str).str.strip()
                df = df[df['company'] != 'nan']
            
            # Clean names
            if 'name' in df.columns:
                df['name'] = df['name'].astype(str).str.strip()
            elif 'first_name' in df.columns and 'last_name' in df.columns:
                df['name'] = df['first_name'].astype(str) + ' ' + df['last_name'].astype(str)
                df['name'] = df['name'].str.strip()
            
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            self.logger.info(f"Processed RB2B data: {len(df)} valid records")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing RB2B data: {e}")
            return df
    
    def test_sheets_access(self, sheets_url: str) -> bool:
        """
        Test if we can access the Google Sheets
        
        Args:
            sheets_url: Google Sheets URL
            
        Returns:
            True if accessible, False otherwise
        """
        try:
            csv_url = self.get_csv_url_from_sheets_url(sheets_url)
            response = requests.head(csv_url, timeout=10)
            
            if response.status_code == 200:
                self.logger.info("✅ Google Sheets is accessible")
                return True
            else:
                self.logger.error(f"❌ Cannot access Google Sheets. Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error testing Google Sheets access: {e}")
            return False

def main():
    """Test the Google Sheets integration"""
    
    # Your RB2B Google Sheets URL
    sheets_url = "https://docs.google.com/spreadsheets/d/1jPwTgvGwQEG9llkpKgWu8PNYXY-OaUMUvNYGxIWUe0I/edit?gid=0#gid=0"
    
    integration = GoogleSheetsRB2BIntegration()
    
    print("🔍 Testing Google Sheets access...")
    if integration.test_sheets_access(sheets_url):
        print("✅ Google Sheets is accessible!")
        
        print("\n📥 Downloading RB2B data...")
        csv_file = integration.download_rb2b_data_from_sheets(sheets_url, "rb2b_client")
        
        if csv_file:
            print(f"✅ Successfully downloaded RB2B data to: {csv_file}")
            
            # Show preview
            df = pd.read_csv(csv_file)
            print(f"\n📊 Data Preview ({len(df)} rows):")
            print(df.head())
            
            print(f"\n📋 Columns available:")
            for col in df.columns:
                print(f"  - {col}")
                
        else:
            print("❌ Failed to download RB2B data")
    else:
        print("❌ Cannot access Google Sheets. Please check:")
        print("  1. The sheet is set to 'Anyone with the link can view'")
        print("  2. The URL is correct")
        print("  3. The sheet is not empty")

if __name__ == "__main__":
    main()