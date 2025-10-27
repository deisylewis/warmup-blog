#!/usr/bin/env python3
"""
Prospect Overlap Analysis Script

This script specifically analyzes prospect overlaps across HeyReach (LinkedIn campaigns),
RB2B (Website visitors), and Instantly (Email campaigns) data sources.

Usage:
    python3 overlap_analyzer.py [csv_files...]
    python3 overlap_analyzer.py --auto-download
    python3 overlap_analyzer.py --directory ./csv-folder
"""

import sys
import os
import argparse
import glob
from datetime import datetime
from dotenv import load_dotenv

from csv_downloader import CSVDownloader
from openai_processor import OpenAIProcessor
from prospect_analyzer import ProspectAnalyzer

def main():
    """Main entry point for overlap analysis"""
    parser = argparse.ArgumentParser(
        description="Analyze prospect overlaps across LinkedIn campaigns, Website visitors, and Email campaigns"
    )
    
    parser.add_argument(
        'csv_files',
        nargs='*',
        help='CSV files to analyze'
    )
    
    parser.add_argument(
        '--auto-download',
        action='store_true',
        help='Automatically download CSVs from all sources before analysis'
    )
    
    parser.add_argument(
        '--directory',
        type=str,
        help='Directory containing CSV files to analyze'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./processed',
        help='Output directory for results (default: ./processed)'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Validate OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("❌ Error: OPENAI_API_KEY is required for analysis")
        print("Please set your OpenAI API key in the .env file")
        sys.exit(1)
    
    # Initialize components
    processor = OpenAIProcessor(
        api_key=openai_api_key,
        model=os.getenv('OPENAI_MODEL', 'gpt-4'),
        max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
    )
    
    analyzer = ProspectAnalyzer(
        openai_processor=processor,
        output_dir=args.output_dir
    )
    
    # Determine CSV files to analyze
    csv_files = []
    
    if args.auto_download:
        print("🔄 Auto-downloading CSVs from all sources...")
        
        # Initialize downloader
        downloader = CSVDownloader(download_dir=os.getenv('DOWNLOAD_DIR', './downloads'))
        
        # Download from all sources
        sources = ['rb2b', 'heyreach', 'instantly']
        for source in sources:
            api_key_var = f'{source.upper()}_API_KEY'
            api_url_var = f'{source.upper()}_API_URL'
            
            api_key = os.getenv(api_key_var)
            api_url = os.getenv(api_url_var)
            
            if api_key and api_url:
                print(f"📥 Downloading from {source}...")
                if source == 'rb2b':
                    file_path = downloader.download_from_rb2b(api_key, api_url)
                elif source == 'heyreach':
                    file_path = downloader.download_from_heyreach(api_key, api_url)
                elif source == 'instantly':
                    file_path = downloader.download_from_instantly(api_key, api_url)
                
                if file_path and downloader.validate_csv_file(file_path):
                    csv_files.append(file_path)
                    print(f"✅ Successfully downloaded: {file_path}")
                else:
                    print(f"⚠️ Failed to download from {source}")
            else:
                print(f"⚠️ Skipping {source} - missing API credentials")
    
    elif args.directory:
        print(f"📁 Looking for CSV files in: {args.directory}")
        csv_pattern = os.path.join(args.directory, "*.csv")
        csv_files = glob.glob(csv_pattern)
        print(f"Found {len(csv_files)} CSV files")
    
    elif args.csv_files:
        csv_files = args.csv_files
        print(f"📋 Analyzing {len(csv_files)} specified CSV files")
    
    else:
        print("❌ Error: No CSV files specified")
        print("Use --auto-download, --directory, or specify CSV files directly")
        sys.exit(1)
    
    if not csv_files:
        print("❌ No valid CSV files found for analysis")
        sys.exit(1)
    
    # Display files to be analyzed
    print(f"\n📊 Files to analyze:")
    for i, file in enumerate(csv_files, 1):
        print(f"   {i}. {os.path.basename(file)}")
    
    # Perform overlap analysis
    print(f"\n🔍 Starting prospect overlap analysis...")
    start_time = datetime.now()
    
    try:
        # Analyze overlaps
        overlap_results = analyzer.analyze_prospect_overlaps(csv_files)
        
        if 'error' in overlap_results:
            print(f"❌ Analysis failed: {overlap_results['error']}")
            sys.exit(1)
        
        # Generate OpenAI report
        print("🤖 Generating OpenAI-powered analysis report...")
        openai_report = analyzer.generate_openai_overlap_report(overlap_results)
        
        # Create CSV report
        print("📄 Creating CSV overlap report...")
        csv_report_path = analyzer.create_overlap_csv_report(overlap_results)
        
        # Calculate duration
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Display results
        print(f"\n🎯 Prospect Overlap Analysis Complete! ({duration:.2f} seconds)")
        print("=" * 60)
        
        summary = overlap_results.get('summary', {})
        
        print(f"📊 DATA SOURCES ANALYZED:")
        for source, count in summary.get('total_records_by_source', {}).items():
            print(f"   • {source}: {count:,} records")
        
        print(f"\n🔍 OVERLAPS DISCOVERED:")
        total_overlaps = 0
        for identifier_type, count in summary.get('total_overlaps_by_identifier', {}).items():
            print(f"   • {identifier_type}: {count:,} overlaps")
            total_overlaps += count
        
        if total_overlaps == 0:
            print("   ⚠️ No overlaps found between the data sources")
            print("   This could indicate:")
            print("     - Different prospect pools across channels")
            print("     - Data format inconsistencies")
            print("     - Need for data normalization")
        else:
            print(f"\n🎉 TOTAL OVERLAPS: {total_overlaps:,}")
            
            # Show most common overlap types
            overlap_counts = summary.get('total_overlaps_by_identifier', {})
            if overlap_counts:
                top_overlap = max(overlap_counts.items(), key=lambda x: x[1])
                print(f"   Most common overlap type: {top_overlap[0]} ({top_overlap[1]:,} matches)")
        
        print(f"\n📁 RESULTS SAVED:")
        print(f"   • Full analysis: {args.output_dir}/prospect_overlap_analysis_*.json")
        if csv_report_path:
            print(f"   • CSV report: {csv_report_path}")
        if openai_report:
            print(f"   • OpenAI analysis: {args.output_dir}/openai_analysis_*.json")
        
        print(f"\n💡 NEXT STEPS:")
        print(f"   1. Review the detailed overlap report for prospect coordination")
        print(f"   2. Use overlapping prospects for multi-channel campaigns")
        print(f"   3. Identify high-value prospects appearing across all channels")
        print(f"   4. Coordinate messaging to avoid prospect fatigue")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()