#!/usr/bin/env python3
"""
Prospect Overlap Analysis Module

This module analyzes prospects from multiple sources (HeyReach LinkedIn campaigns, 
RB2B website visitors, and Instantly email campaigns) to find overlaps and 
generate comprehensive reports.
"""

import pandas as pd
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
import os
from openai_processor import OpenAIProcessor

class ProspectAnalyzer:
    """
    Analyzes prospects across multiple sources to identify overlaps
    """
    
    def __init__(self, openai_processor: OpenAIProcessor, output_dir: str = "./processed"):
        self.openai_processor = openai_processor
        self.output_dir = output_dir
        self.setup_logging()
        
        # Source labels mapping
        self.source_labels = {
            'heyreach': 'LinkedIn campaigns',
            'rb2b': 'Website visitors', 
            'instantly': 'Email campaign'
        }
        
        # Common fields that might contain prospect identifiers
        self.identifier_fields = [
            'email', 'email_address', 'contact_email', 'work_email',
            'company', 'company_name', 'organization', 'domain',
            'linkedin_url', 'linkedin_profile', 'profile_url',
            'first_name', 'last_name', 'full_name', 'name'
        ]
    
    def setup_logging(self):
        """Setup logging for prospect analysis"""
        self.logger = logging.getLogger(__name__)
    
    def identify_source_from_filename(self, filename: str) -> str:
        """
        Identify the source based on filename
        
        Args:
            filename: CSV filename
            
        Returns:
            Source identifier (heyreach, rb2b, instantly)
        """
        filename_lower = filename.lower()
        
        if 'heyreach' in filename_lower:
            return 'heyreach'
        elif 'rb2b' in filename_lower:
            return 'rb2b'
        elif 'instantly' in filename_lower:
            return 'instantly'
        else:
            # Try to guess from common patterns
            if any(term in filename_lower for term in ['linkedin', 'social']):
                return 'heyreach'
            elif any(term in filename_lower for term in ['website', 'visitor', 'traffic']):
                return 'rb2b'
            elif any(term in filename_lower for term in ['email', 'campaign', 'outreach']):
                return 'instantly'
            else:
                self.logger.warning(f"Could not identify source for {filename}, defaulting to 'unknown'")
                return 'unknown'
    
    def load_and_label_csv(self, filepath: str, source: str = None) -> pd.DataFrame:
        """
        Load CSV and add source labeling
        
        Args:
            filepath: Path to CSV file
            source: Optional source override
            
        Returns:
            DataFrame with source labeling
        """
        try:
            df = pd.read_csv(filepath)
            
            # Determine source if not provided
            if source is None:
                source = self.identify_source_from_filename(os.path.basename(filepath))
            
            # Add source columns
            df['data_source'] = source
            df['source_label'] = self.source_labels.get(source, f'Unknown ({source})')
            df['source_file'] = os.path.basename(filepath)
            
            self.logger.info(f"Loaded {len(df)} records from {filepath} as {self.source_labels.get(source, source)}")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading CSV {filepath}: {e}")
            return pd.DataFrame()
    
    def normalize_identifier(self, value: str) -> str:
        """
        Normalize identifier for comparison
        
        Args:
            value: Raw identifier value
            
        Returns:
            Normalized identifier
        """
        if pd.isna(value) or value == '':
            return ''
        
        # Convert to string and lowercase
        normalized = str(value).lower().strip()
        
        # Remove common prefixes/suffixes for URLs
        normalized = normalized.replace('https://', '').replace('http://', '')
        normalized = normalized.replace('www.', '')
        normalized = normalized.replace('linkedin.com/in/', '')
        
        return normalized
    
    def extract_identifiers(self, df: pd.DataFrame) -> Dict[str, Set[Tuple[str, int]]]:
        """
        Extract all possible identifiers from DataFrame
        
        Args:
            df: DataFrame with prospect data
            
        Returns:
            Dictionary mapping identifier types to sets of (normalized_value, row_index) tuples
        """
        identifiers = {}
        
        for field in self.identifier_fields:
            # Find columns that might contain this identifier type
            matching_columns = [col for col in df.columns if field.lower() in col.lower()]
            
            if matching_columns:
                identifier_set = set()
                for col in matching_columns:
                    for idx, value in df[col].items():
                        normalized = self.normalize_identifier(value)
                        if normalized and len(normalized) > 2:  # Skip very short identifiers
                            identifier_set.add((normalized, idx))
                
                if identifier_set:
                    identifiers[field] = identifier_set
        
        return identifiers
    
    def find_overlaps(self, dataframes: List[pd.DataFrame]) -> Dict:
        """
        Find overlaps between multiple DataFrames
        
        Args:
            dataframes: List of DataFrames to compare
            
        Returns:
            Dictionary with overlap analysis results
        """
        self.logger.info(f"Analyzing overlaps between {len(dataframes)} data sources...")
        
        # Extract identifiers from each DataFrame
        all_identifiers = []
        source_info = []
        
        for i, df in enumerate(dataframes):
            if df.empty:
                continue
                
            identifiers = self.extract_identifiers(df)
            all_identifiers.append(identifiers)
            
            source = df['data_source'].iloc[0] if 'data_source' in df.columns else f'source_{i}'
            source_label = df['source_label'].iloc[0] if 'source_label' in df.columns else f'Source {i+1}'
            
            source_info.append({
                'source': source,
                'label': source_label,
                'total_records': len(df),
                'dataframe_index': i
            })
        
        # Find overlaps for each identifier type
        overlap_results = {
            'sources': source_info,
            'overlaps_by_identifier': {},
            'complete_overlaps': [],  # Prospects that appear in all sources
            'partial_overlaps': [],   # Prospects that appear in 2+ sources
            'summary': {}
        }
        
        for identifier_type in self.identifier_fields:
            # Get identifier sets that have this type
            identifier_sets = []
            source_indices = []
            
            for i, identifiers in enumerate(all_identifiers):
                if identifier_type in identifiers:
                    identifier_sets.append(identifiers[identifier_type])
                    source_indices.append(i)
            
            if len(identifier_sets) < 2:
                continue  # Need at least 2 sources to find overlaps
            
            # Find intersections
            overlaps = self.find_identifier_intersections(
                identifier_sets, source_indices, source_info, identifier_type
            )
            
            if overlaps:
                overlap_results['overlaps_by_identifier'][identifier_type] = overlaps
        
        # Consolidate overlaps to find complete matches
        overlap_results['complete_overlaps'] = self.consolidate_complete_overlaps(
            overlap_results['overlaps_by_identifier'], dataframes, source_info
        )
        
        # Generate summary statistics
        overlap_results['summary'] = self.generate_overlap_summary(overlap_results)
        
        return overlap_results
    
    def find_identifier_intersections(self, identifier_sets: List[Set], source_indices: List[int], 
                                    source_info: List[Dict], identifier_type: str) -> List[Dict]:
        """
        Find intersections between identifier sets
        
        Args:
            identifier_sets: List of identifier sets
            source_indices: Corresponding source indices
            source_info: Source information
            identifier_type: Type of identifier being compared
            
        Returns:
            List of overlap records
        """
        overlaps = []
        
        # Compare all pairs and combinations
        for i in range(len(identifier_sets)):
            for j in range(i + 1, len(identifier_sets)):
                set1, set2 = identifier_sets[i], identifier_sets[j]
                source1_idx, source2_idx = source_indices[i], source_indices[j]
                
                # Find intersection based on normalized values
                intersection = set()
                for val1, row1 in set1:
                    for val2, row2 in set2:
                        if val1 == val2:  # Same normalized identifier
                            intersection.add((val1, row1, row2))
                
                # Record overlaps
                for normalized_id, row1, row2 in intersection:
                    overlaps.append({
                        'identifier_type': identifier_type,
                        'normalized_value': normalized_id,
                        'sources': [
                            {
                                'source': source_info[source1_idx]['source'],
                                'label': source_info[source1_idx]['label'],
                                'row_index': row1
                            },
                            {
                                'source': source_info[source2_idx]['source'],
                                'label': source_info[source2_idx]['label'],
                                'row_index': row2
                            }
                        ]
                    })
        
        return overlaps
    
    def consolidate_complete_overlaps(self, overlaps_by_identifier: Dict, 
                                    dataframes: List[pd.DataFrame], 
                                    source_info: List[Dict]) -> List[Dict]:
        """
        Consolidate overlaps to find prospects that appear in all sources
        
        Args:
            overlaps_by_identifier: Overlaps organized by identifier type
            dataframes: Original DataFrames
            source_info: Source information
            
        Returns:
            List of complete overlap records
        """
        # This is a simplified version - in practice, you'd want more sophisticated
        # matching logic that considers multiple identifier types per prospect
        complete_overlaps = []
        
        # For now, find overlaps that appear in multiple identifier types
        # This suggests the same prospect across sources
        
        return complete_overlaps
    
    def generate_overlap_summary(self, overlap_results: Dict) -> Dict:
        """
        Generate summary statistics for overlaps
        
        Args:
            overlap_results: Complete overlap analysis results
            
        Returns:
            Summary statistics
        """
        summary = {
            'total_sources': len(overlap_results['sources']),
            'sources_analyzed': [info['label'] for info in overlap_results['sources']],
            'total_records_by_source': {
                info['label']: info['total_records'] 
                for info in overlap_results['sources']
            },
            'identifier_types_found': list(overlap_results['overlaps_by_identifier'].keys()),
            'total_overlaps_by_identifier': {
                identifier_type: len(overlaps)
                for identifier_type, overlaps in overlap_results['overlaps_by_identifier'].items()
            },
            'complete_overlaps_count': len(overlap_results['complete_overlaps'])
        }
        
        return summary
    
    def analyze_prospect_overlaps(self, csv_files: List[str]) -> Dict:
        """
        Main method to analyze prospect overlaps across CSV files
        
        Args:
            csv_files: List of CSV file paths
            
        Returns:
            Complete analysis results
        """
        self.logger.info(f"Starting prospect overlap analysis for {len(csv_files)} files...")
        
        # Load and label all CSV files
        dataframes = []
        for csv_file in csv_files:
            df = self.load_and_label_csv(csv_file)
            if not df.empty:
                dataframes.append(df)
        
        if len(dataframes) < 2:
            self.logger.warning("Need at least 2 valid CSV files to analyze overlaps")
            return {'error': 'Insufficient data sources for overlap analysis'}
        
        # Find overlaps
        overlap_results = self.find_overlaps(dataframes)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_filename = f"prospect_overlap_analysis_{timestamp}.json"
        result_filepath = os.path.join(self.output_dir, result_filename)
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        with open(result_filepath, 'w', encoding='utf-8') as f:
            json.dump(overlap_results, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"Overlap analysis saved to: {result_filepath}")
        
        return overlap_results
    
    def generate_openai_overlap_report(self, overlap_results: Dict) -> Optional[Dict]:
        """
        Generate an OpenAI-powered analysis report of the overlaps
        
        Args:
            overlap_results: Results from overlap analysis
            
        Returns:
            OpenAI analysis results
        """
        if not overlap_results or 'error' in overlap_results:
            return None
        
        # Prepare data for OpenAI analysis
        summary = overlap_results.get('summary', {})
        sources = overlap_results.get('sources', [])
        overlaps_by_identifier = overlap_results.get('overlaps_by_identifier', {})
        
        # Create a comprehensive prompt
        prompt = f"""
        Analyze this prospect overlap analysis between different marketing channels:

        DATA SOURCES ANALYZED:
        {chr(10).join([f"- {source['label']}: {source['total_records']} records" for source in sources])}

        OVERLAP FINDINGS:
        {json.dumps(summary, indent=2)}

        DETAILED OVERLAPS BY IDENTIFIER:
        {json.dumps(overlaps_by_identifier, indent=2, default=str)}

        Please provide:
        1. Executive Summary of prospect overlaps
        2. Key insights about multi-channel prospect engagement
        3. Recommendations for coordinated marketing efforts
        4. Identification of high-value prospects appearing across multiple channels
        5. Potential data quality issues or duplicate management strategies
        6. Strategic implications for marketing campaign coordination

        Focus on actionable insights for marketing teams managing LinkedIn campaigns, 
        website visitor tracking, and email campaigns.
        """
        
        # Use OpenAI to analyze the overlaps
        return self.openai_processor.process_csv_with_prompt(
            csv_filepath="overlap_analysis_data",  # Virtual filepath
            prompt=prompt,
            output_dir=self.output_dir
        )
    
    def create_overlap_csv_report(self, overlap_results: Dict) -> Optional[str]:
        """
        Create a CSV report of overlapping prospects
        
        Args:
            overlap_results: Results from overlap analysis
            
        Returns:
            Path to created CSV report
        """
        if not overlap_results or 'error' in overlap_results:
            return None
        
        try:
            # Prepare data for CSV export
            rows = []
            
            for identifier_type, overlaps in overlap_results.get('overlaps_by_identifier', {}).items():
                for overlap in overlaps:
                    row = {
                        'identifier_type': identifier_type,
                        'normalized_value': overlap['normalized_value'],
                        'sources_count': len(overlap['sources']),
                        'sources': ', '.join([s['label'] for s in overlap['sources']]),
                        'source_details': json.dumps(overlap['sources'])
                    }
                    rows.append(row)
            
            if not rows:
                self.logger.warning("No overlaps found to export to CSV")
                return None
            
            # Create DataFrame and save
            df = pd.DataFrame(rows)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = f"prospect_overlaps_{timestamp}.csv"
            csv_filepath = os.path.join(self.output_dir, csv_filename)
            
            df.to_csv(csv_filepath, index=False)
            
            self.logger.info(f"Overlap CSV report saved to: {csv_filepath}")
            return csv_filepath
            
        except Exception as e:
            self.logger.error(f"Error creating CSV report: {e}")
            return None