import requests
import pandas as pd
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
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
    
    def get_date_range_params(self, days_back: int = 7) -> Dict[str, str]:
        """
        Generate date range parameters for the last N days
        
        Args:
            days_back: Number of days to go back (default: 7)
            
        Returns:
            Dictionary with date range parameters
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        return {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'date_from': start_date.strftime('%Y-%m-%d'),
            'date_to': end_date.strftime('%Y-%m-%d')
        }
    
    def download_from_rb2b(self, api_key: str, api_url: str, client_name: str = "unknown", 
                          days_back: int = 7, params: Optional[Dict] = None) -> Optional[str]:
        """
        Download CSV from RB2B API (Website visitors)
        
        Args:
            api_key: RB2B API key
            api_url: RB2B API endpoint URL
            client_name: Name of the client
            days_back: Number of days to go back for data (default: 7)
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
            
            # Add date range parameters
            date_params = self.get_date_range_params(days_back)
            final_params = {**(params or {}), **date_params}
            
            self.logger.info(f"Requesting CSV export from RB2B (Website visitors) for client '{client_name}' - last {days_back} days...")
            response = requests.get(api_url, headers=headers, params=final_params)
            response.raise_for_status()
            
            # Generate filename with timestamp and client name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{client_name}_rb2b_website_visitors_{timestamp}.csv"
            filepath = os.path.join(self.download_dir, filename)
            
            # Save CSV content
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                f.write(response.text)
            
            self.logger.info(f"Successfully downloaded RB2B website visitors CSV for client '{client_name}': {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading from RB2B: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading from RB2B: {e}")
            return None
    
    def download_from_heyreach(self, api_key: str, api_url: str, client_name: str = "unknown",
                              days_back: int = 7, params: Optional[Dict] = None) -> Optional[str]:
        """
        Download CSV from HeyReach API (LinkedIn campaigns)
        
        Args:
            api_key: HeyReach API key
            api_url: HeyReach API endpoint URL
            client_name: Name of the client
            days_back: Number of days to go back for data (default: 7)
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
            
            # Add date range parameters
            date_params = self.get_date_range_params(days_back)
            final_params = {**(params or {}), **date_params}
            
            self.logger.info(f"Requesting CSV export from HeyReach (LinkedIn campaigns) for client '{client_name}' - last {days_back} days...")
            response = requests.get(api_url, headers=headers, params=final_params)
            response.raise_for_status()
            
            # Generate filename with timestamp and client name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{client_name}_heyreach_linkedin_campaigns_{timestamp}.csv"
            filepath = os.path.join(self.download_dir, filename)
            
            # Save CSV content
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                f.write(response.text)
            
            self.logger.info(f"Successfully downloaded HeyReach LinkedIn campaigns CSV for client '{client_name}': {filepath}")
            return filepath
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading from HeyReach: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error downloading from HeyReach: {e}")
            return None
    
    def download_from_instantly(self, api_key: str, api_url: str, client_name: str = "unknown",
                               days_back: int = 7, params: Optional[Dict] = None) -> Optional[str]:
        """
        Download CSV from Instantly API (Email campaigns)
        
        Args:
            api_key: Instantly API key
            api_url: Instantly API endpoint URL
            client_name: Name of the client
            days_back: Number of days to go back for data (default: 7)
            params: Optional parameters for the API request
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            headers = {
                'Authorization': f'Basic {api_key}',  # Instantly uses Basic auth
                'Accept': 'text/csv',
                'Content-Type': 'application/json'
            }
            
            # Add date range parameters
            date_params = self.get_date_range_params(days_back)
            final_params = {**(params or {}), **date_params}
            
            self.logger.info(f"Requesting CSV export from Instantly (Email campaigns) for client '{client_name}' - last {days_back} days...")
            response = requests.get(api_url, headers=headers, params=final_params)
            response.raise_for_status()
            
            # Generate filename with timestamp and client name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{client_name}_instantly_email_campaigns_{timestamp}.csv"
            filepath = os.path.join(self.download_dir, filename)
            
            # Save CSV content
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                f.write(response.text)
            
            self.logger.info(f"Successfully downloaded Instantly email campaigns CSV for client '{client_name}': {filepath}")
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
    
    def download_all_clients(self, client_configs: List[Dict], sources: List[str] = None, days_back: int = 7) -> List[str]:
        """
        Download CSVs from all configured clients
        
        Args:
            client_configs: List of client configuration dictionaries
            sources: List of sources to download from
            days_back: Number of days to go back for data
            
        Returns:
            List of downloaded file paths
        """
        if sources is None:
            sources = ['rb2b', 'heyreach', 'instantly']
        
        downloaded_files = []
        
        for client_config in client_configs:
            client_name = client_config.get('name', 'unknown')
            self.logger.info(f"Processing client: {client_name}")
            
            # Download from RB2B
            if 'rb2b' in sources and client_config.get('rb2b_api_key') and client_config.get('rb2b_api_url'):
                file_path = self.download_from_rb2b(
                    api_key=client_config['rb2b_api_key'],
                    api_url=client_config['rb2b_api_url'],
                    client_name=client_name,
                    days_back=days_back
                )
                if file_path and self.validate_csv_file(file_path):
                    downloaded_files.append(file_path)
            
            # Download from HeyReach
            if 'heyreach' in sources and client_config.get('heyreach_api_key') and client_config.get('heyreach_api_url'):
                file_path = self.download_from_heyreach(
                    api_key=client_config['heyreach_api_key'],
                    api_url=client_config['heyreach_api_url'],
                    client_name=client_name,
                    days_back=days_back
                )
                if file_path and self.validate_csv_file(file_path):
                    downloaded_files.append(file_path)
            
            # Download from Instantly
            if 'instantly' in sources and client_config.get('instantly_api_key') and client_config.get('instantly_api_url'):
                file_path = self.download_from_instantly(
                    api_key=client_config['instantly_api_key'],
                    api_url=client_config['instantly_api_url'],
                    client_name=client_name,
                    days_back=days_back
                )
                if file_path and self.validate_csv_file(file_path):
                    downloaded_files.append(file_path)
        
        return downloaded_files