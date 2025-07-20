#!/usr/bin/env python3
"""
CSV Download and OpenAI Processing Application

This application downloads CSV files from RB2B and HeyReach APIs,
then processes them using OpenAI for analysis and insights.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv
from typing import List, Optional, Dict
import json
from datetime import datetime

from csv_downloader import CSVDownloader
from openai_processor import OpenAIProcessor
from prospect_analyzer import ProspectAnalyzer

class CSVProcessingApp:
    """Main application class for CSV download and OpenAI processing"""
    
    def __init__(self):
        self.setup_logging()
        self.load_environment()
        self.setup_components()
    
    def setup_logging(self):
        """Setup application logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_environment(self):
        """Load environment variables from .env file"""
        load_dotenv()
        
        # Required environment variables
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Optional settings with defaults
        self.download_dir = os.getenv('DOWNLOAD_DIR', './downloads')
        self.processed_dir = os.getenv('PROCESSED_DIR', './processed')
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.openai_max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
        
        # Load client configurations
        self.client_configs = self.load_client_configs()
        
        # Validate required keys
        if not self.openai_api_key:
            self.logger.error("OPENAI_API_KEY is required")
            sys.exit(1)
        
        if not self.client_configs:
            self.logger.warning("No client configurations found")
    
    def load_client_configs(self) -> List[Dict]:
        """Load client configurations from environment variables"""
        client_configs = []
        
        # Look for client configurations (CLIENT1_, CLIENT2_, etc.)
        client_num = 1
        while True:
            client_prefix = f'CLIENT{client_num}_'
            client_name = os.getenv(f'{client_prefix}NAME')
            
            if not client_name:
                break  # No more clients
            
            client_config = {
                'name': client_name,
                'rb2b_api_key': os.getenv(f'{client_prefix}RB2B_API_KEY'),
                'rb2b_api_url': os.getenv(f'{client_prefix}RB2B_API_URL'),
                'heyreach_api_key': os.getenv(f'{client_prefix}HEYREACH_API_KEY'),
                'heyreach_api_url': os.getenv(f'{client_prefix}HEYREACH_API_URL'),
                'instantly_api_key': os.getenv(f'{client_prefix}INSTANTLY_API_KEY'),
                'instantly_api_url': os.getenv(f'{client_prefix}INSTANTLY_API_URL'),
            }
            
            # Only add client if at least one API is configured
            if any([client_config['rb2b_api_key'], client_config['heyreach_api_key'], client_config['instantly_api_key']]):
                client_configs.append(client_config)
                self.logger.info(f"Loaded configuration for client: {client_name}")
            
            client_num += 1
        
        return client_configs
    
    def setup_components(self):
        """Initialize downloader, processor, and analyzer components"""
        self.downloader = CSVDownloader(download_dir=self.download_dir)
        self.processor = OpenAIProcessor(
            api_key=self.openai_api_key,
            model=self.openai_model,
            max_tokens=self.openai_max_tokens
        )
        self.analyzer = ProspectAnalyzer(
            openai_processor=self.processor,
            output_dir=self.processed_dir
        )
    
    def download_csvs(self, sources: List[str] = None, days_back: int = 7) -> List[str]:
        """
        Download CSV files from specified sources for all clients
        
        Args:
            sources: List of sources to download from ('rb2b', 'heyreach', 'instantly', or all)
            days_back: Number of days to go back for data (default: 7)
            
        Returns:
            List of downloaded file paths
        """
        if sources is None:
            sources = ['rb2b', 'heyreach', 'instantly']
        
        self.logger.info(f"Starting CSV downloads for {len(self.client_configs)} clients - last {days_back} days")
        
        # Download from all clients using the new method
        downloaded_files = self.downloader.download_all_clients(
            client_configs=self.client_configs,
            sources=sources,
            days_back=days_back
        )
        
        self.logger.info(f"Downloaded {len(downloaded_files)} CSV files total")
        return downloaded_files
    
    def process_with_openai(self, csv_files: List[str], prompt: str = None, analysis_type: str = "insights") -> List[dict]:
        """
        Process CSV files with OpenAI
        
        Args:
            csv_files: List of CSV file paths to process
            prompt: Custom prompt for OpenAI (optional)
            analysis_type: Type of analysis ('insights', 'summary', 'custom', 'compare')
            
        Returns:
            List of processing results
        """
        if not csv_files:
            self.logger.warning("No CSV files to process")
            return []
        
        results = []
        
        if analysis_type == "compare" and len(csv_files) > 1:
            # Compare multiple CSV files
            self.logger.info(f"Comparing {len(csv_files)} CSV files...")
            comparison_result = self.processor.compare_csvs(csv_files, self.processed_dir)
            if comparison_result:
                results.append(comparison_result)
        else:
            # Process each file individually
            for csv_file in csv_files:
                self.logger.info(f"Processing {csv_file} with OpenAI...")
                
                if analysis_type == "insights":
                    result = self.processor.analyze_csv_insights(csv_file, self.processed_dir)
                elif analysis_type == "summary":
                    result = self.processor.generate_data_summary(csv_file, self.processed_dir)
                elif analysis_type == "custom" and prompt:
                    result = self.processor.process_csv_with_prompt(csv_file, prompt, self.processed_dir)
                else:
                    self.logger.warning(f"Unknown analysis type or missing prompt: {analysis_type}")
                    continue
                
                if result:
                    results.append(result)
        
        return results
    
    def analyze_prospect_overlaps(self, csv_files: List[str]) -> Dict:
        """
        Analyze prospect overlaps across CSV files from different sources
        
        Args:
            csv_files: List of CSV file paths to analyze
            
        Returns:
            Dictionary with overlap analysis results
        """
        self.logger.info("Starting prospect overlap analysis...")
        
        # Perform overlap analysis
        overlap_results = self.analyzer.analyze_prospect_overlaps(csv_files)
        
        if 'error' not in overlap_results:
            # Generate OpenAI-powered analysis report
            self.logger.info("Generating OpenAI overlap analysis report...")
            openai_report = self.analyzer.generate_openai_overlap_report(overlap_results)
            
            # Create CSV report of overlaps
            csv_report_path = self.analyzer.create_overlap_csv_report(overlap_results)
            
            # Add additional results
            overlap_results['openai_analysis'] = openai_report
            overlap_results['csv_report_path'] = csv_report_path
        
        return overlap_results
    
    def run_full_pipeline(self, sources: List[str] = None, prompt: str = None, analysis_type: str = "insights", days_back: int = 7) -> dict:
        """
        Run the complete pipeline: download CSVs and process with OpenAI
        
        Args:
            sources: List of sources to download from
            prompt: Custom prompt for OpenAI processing
            analysis_type: Type of analysis to perform
            days_back: Number of days to go back for data
            
        Returns:
            Dictionary with pipeline results
        """
        self.logger.info("Starting full CSV processing pipeline...")
        
        pipeline_start = datetime.now()
        
        # Step 1: Download CSVs
        downloaded_files = self.download_csvs(sources, days_back)
        
        if not downloaded_files:
            self.logger.error("No CSV files were downloaded successfully")
            return {
                'success': False,
                'error': 'No CSV files downloaded',
                'downloaded_files': [],
                'processing_results': []
            }
        
        # Step 2: Process with OpenAI
        processing_results = self.process_with_openai(downloaded_files, prompt, analysis_type)
        
        pipeline_end = datetime.now()
        pipeline_duration = (pipeline_end - pipeline_start).total_seconds()
        
        # Create pipeline summary
        pipeline_result = {
            'success': True,
            'pipeline_duration_seconds': pipeline_duration,
            'downloaded_files': downloaded_files,
            'processing_results': processing_results,
            'summary': {
                'files_downloaded': len(downloaded_files),
                'files_processed': len(processing_results),
                'analysis_type': analysis_type,
                'timestamp': pipeline_start.isoformat()
            }
        }
        
        # Save pipeline summary
        summary_filename = f"pipeline_summary_{pipeline_start.strftime('%Y%m%d_%H%M%S')}.json"
        summary_filepath = os.path.join(self.processed_dir, summary_filename)
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
        
        with open(summary_filepath, 'w', encoding='utf-8') as f:
            json.dump(pipeline_result, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Pipeline completed in {pipeline_duration:.2f} seconds")
        self.logger.info(f"Pipeline summary saved to: {summary_filepath}")
        
        return pipeline_result

def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Download CSVs from RB2B and HeyReach, then process with OpenAI"
    )
    
    parser.add_argument(
        '--sources',
        nargs='+',
        choices=['rb2b', 'heyreach', 'instantly'],
        default=['rb2b', 'heyreach', 'instantly'],
        help='Sources to download from (default: all)'
    )
    
    parser.add_argument(
        '--analysis-type',
        choices=['insights', 'summary', 'custom', 'compare', 'overlaps'],
        default='insights',
        help='Type of OpenAI analysis to perform (default: insights)'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        help='Custom prompt for OpenAI processing (required for custom analysis)'
    )
    
    parser.add_argument(
        '--download-only',
        action='store_true',
        help='Only download CSVs, skip OpenAI processing'
    )
    
    parser.add_argument(
        '--process-existing',
        type=str,
        help='Process existing CSV files (provide directory path)'
    )
    
    parser.add_argument(
        '--days-back',
        type=int,
        default=7,
        help='Number of days to go back for data download (default: 7)'
    )
    
    args = parser.parse_args()
    
    # Initialize the application
    app = CSVProcessingApp()
    
    try:
        if args.process_existing:
            # Process existing CSV files
            import glob
            csv_files = glob.glob(os.path.join(args.process_existing, "*.csv"))
            if not csv_files:
                print(f"No CSV files found in {args.process_existing}")
                sys.exit(1)
            
            print(f"Found {len(csv_files)} CSV files to process")
            results = app.process_with_openai(csv_files, args.prompt, args.analysis_type)
            print(f"Processed {len(results)} files successfully")
            
        elif args.download_only:
            # Only download CSVs
            downloaded_files = app.download_csvs(args.sources, args.days_back)
            print(f"Downloaded {len(downloaded_files)} CSV files:")
            for file in downloaded_files:
                print(f"  - {file}")
        
        else:
            # Run full pipeline
            if args.analysis_type == 'custom' and not args.prompt:
                print("Error: --prompt is required for custom analysis type")
                sys.exit(1)
            
            if args.analysis_type == 'overlaps':
                # Special handling for overlap analysis
                print("Running prospect overlap analysis pipeline...")
                downloaded_files = app.download_csvs(args.sources, args.days_back)
                
                if not downloaded_files:
                    print("No CSV files were downloaded successfully")
                    sys.exit(1)
                
                overlap_results = app.analyze_prospect_overlaps(downloaded_files)
                
                if 'error' in overlap_results:
                    print(f"Overlap analysis failed: {overlap_results['error']}")
                    sys.exit(1)
                
                # Display results
                summary = overlap_results.get('summary', {})
                print(f"\n🎯 Prospect Overlap Analysis Complete!")
                print(f"📊 Sources analyzed: {', '.join(summary.get('sources_analyzed', []))}")
                print(f"📈 Total records by source:")
                for source, count in summary.get('total_records_by_source', {}).items():
                    print(f"   - {source}: {count} records")
                
                print(f"🔍 Overlaps found by identifier type:")
                for identifier_type, count in summary.get('total_overlaps_by_identifier', {}).items():
                    print(f"   - {identifier_type}: {count} overlaps")
                
                if overlap_results.get('csv_report_path'):
                    print(f"📋 CSV report saved: {overlap_results['csv_report_path']}")
                
                print(f"📁 Full analysis saved in: {app.processed_dir}")
                
            else:
                # Regular pipeline
                result = app.run_full_pipeline(args.sources, args.prompt, args.analysis_type, args.days_back)
                
                if result['success']:
                    print(f"Pipeline completed successfully!")
                    print(f"Downloaded files: {result['summary']['files_downloaded']}")
                    print(f"Processed files: {result['summary']['files_processed']}")
                    print(f"Duration: {result['pipeline_duration_seconds']:.2f} seconds")
                else:
                    print(f"Pipeline failed: {result.get('error', 'Unknown error')}")
                    sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()