import requests
import pandas as pd
import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import json

class CSVDownloader:
    """
    A class to handle downloading CSV files from RB2B and HeyReach APIs
    """
    
    def __init__(self, download_dir: str = "./downloads"):
        self.download_dir = download_dir
        self.setup_logging()
        self.ensure_download_directory()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('csv_downloader.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def ensure_download_directory(self):
        """Ensure the download directory exists"""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            self.logger.info(f"Created download directory: {self.download_dir}")
    
    def download_from_rb2b(self, api_key: str, api_url: str, params: Optional[Dict] = None) -> Optional[str]:
        """
        Download CSV from RB2B API (Website visitors)
        
        Args:
            api_key: RB2B API key
            api_url: RB2B API endpoint URL
            params: Optional parameters for the API request
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Accept': 'text/csv',
                'Content-Type': 'application/json'
            }
            
            self.logger.info("Requesting CSV export from RB2B (Website visitors)...")
            response = requests.get(api_url, headers=headers, params=params or {})
            response.raise_for_status()
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rb2b_website_visitors_{timestamp}.csv"
            filepath = os.path.join(self.download_dir, filename)
            
            # Save CSV content
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                f.write(response.text)
            
            self.logger.info(f"Successfully downloaded RB2B website visitors CSV: {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading from RB2B: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading from RB2B: {e}")
            return None
    
    def download_from_heyreach(self, api_key: str, api_url: str, params: Optional[Dict] = None) -> Optional[str]:
        """
        Download CSV from HeyReach API (LinkedIn campaigns)
        
        Args:
            api_key: HeyReach API key
            api_url: HeyReach API endpoint URL
            params: Optional parameters for the API request
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Accept': 'text/csv',
                'Content-Type': 'application/json'
            }
            
            self.logger.info("Requesting CSV export from HeyReach (LinkedIn campaigns)...")
            response = requests.get(api_url, headers=headers, params=params or {})
            response.raise_for_status()
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"heyreach_linkedin_campaigns_{timestamp}.csv"
            filepath = os.path.join(self.download_dir, filename)
            
            # Save CSV content
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                f.write(response.text)
            
            self.logger.info(f"Successfully downloaded HeyReach LinkedIn campaigns CSV: {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading from HeyReach: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading from HeyReach: {e}")
            return None
    
    def download_from_instantly(self, api_key: str, api_url: str, params: Optional[Dict] = None) -> Optional[str]:
        """
        Download CSV from Instantly API (Email campaigns)
        
        Args:
            api_key: Instantly API key
            api_url: Instantly API endpoint URL
            params: Optional parameters for the API request
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Accept': 'text/csv',
                'Content-Type': 'application/json'
            }
            
            self.logger.info("Requesting CSV export from Instantly (Email campaigns)...")
            response = requests.get(api_url, headers=headers, params=params or {})
            response.raise_for_status()
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"instantly_email_campaigns_{timestamp}.csv"
            filepath = os.path.join(self.download_dir, filename)
            
            # Save CSV content
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                f.write(response.text)
            
            self.logger.info(f"Successfully downloaded Instantly email campaigns CSV: {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading from Instantly: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading from Instantly: {e}")
            return None
    
    def validate_csv_file(self, filepath: str) -> bool:
        """
        Validate that the downloaded file is a proper CSV
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            True if valid CSV, False otherwise
        """
        try:
            df = pd.read_csv(filepath)
            if df.empty:
                self.logger.warning(f"CSV file is empty: {filepath}")
                return False
            
            self.logger.info(f"CSV validation successful. Rows: {len(df)}, Columns: {len(df.columns)}")
            return True
            
        except Exception as e:
            self.logger.error(f"CSV validation failed for {filepath}: {e}")
            return False
    
    def get_csv_info(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Get basic information about the CSV file
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            Dictionary with CSV information or None if failed
        """
        try:
            df = pd.read_csv(filepath)
            info = {
                'filepath': filepath,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'file_size': os.path.getsize(filepath),
                'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
            }
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting CSV info for {filepath}: {e}")
            return None