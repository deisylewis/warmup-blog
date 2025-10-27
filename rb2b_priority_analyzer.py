#!/usr/bin/env python3
"""
RB2B Priority Overlap Analyzer
Focuses on RB2B website visitors as the primary source and finds overlaps 
with HeyReach and Instantly data.
"""

import pandas as pd
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import os
from google_sheets_integration import GoogleSheetsRB2BIntegration

class RB2BPriorityAnalyzer:
    """
    Overlap analyzer that prioritizes RB2B website visitors
    """
    
    def __init__(self):
        self.setup_logging()
        self.rb2b_integration = GoogleSheetsRB2BIntegration()
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def analyze_rb2b_priority_overlaps(self, rb2b_sheets_url: str, webhook_data_dir: str = "webhook_data") -> Dict:
        """
        Analyze overlaps with RB2B as the priority source
        
        Args:
            rb2b_sheets_url: Google Sheets URL for RB2B data
            webhook_data_dir: Directory containing HeyReach/Instantly data
            
        Returns:
            Analysis results
        """
        try:
            self.logger.info("🎯 Starting RB2B Priority Overlap Analysis...")
            
            # Step 1: Get RB2B data from Google Sheets
            self.logger.info("📥 Downloading RB2B website visitor data...")
            rb2b_file = self.rb2b_integration.download_rb2b_data_from_sheets(rb2b_sheets_url, "rb2b_priority")
            
            if not rb2b_file:
                self.logger.error("❌ Failed to download RB2B data")
                return {"success": False, "error": "Cannot access RB2B data"}
            
            # Load RB2B data
            rb2b_df = pd.read_csv(rb2b_file)
            self.logger.info(f"📊 Loaded {len(rb2b_df)} RB2B website visitors")
            
            # Step 2: Load HeyReach and Instantly data from webhook directory
            other_data = self.load_webhook_data(webhook_data_dir)
            
            if not other_data:
                self.logger.warning("⚠️ No HeyReach/Instantly data found for comparison")
                return {
                    "success": True,
                    "rb2b_visitors": len(rb2b_df),
                    "overlaps": [],
                    "message": "RB2B data loaded but no other sources to compare"
                }
            
            # Step 3: Find overlaps with RB2B as priority
            overlaps = self.find_rb2b_priority_overlaps(rb2b_df, other_data)
            
            # Step 4: Generate priority report
            report = self.generate_rb2b_priority_report(rb2b_df, overlaps)
            
            # Step 5: Save results
            self.save_priority_results(report)
            
            self.logger.info("✅ RB2B Priority Analysis Complete!")
            
            return {
                "success": True,
                "rb2b_visitors": len(rb2b_df),
                "total_overlaps": len(overlaps),
                "high_priority_prospects": len([o for o in overlaps if o.get('priority') == 'HIGH']),
                "report": report
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error in RB2B priority analysis: {e}")
            return {"success": False, "error": str(e)}
    
    def load_webhook_data(self, webhook_data_dir: str) -> List[Dict]:
        """
        Load HeyReach and Instantly data from webhook directory
        
        Args:
            webhook_data_dir: Directory path
            
        Returns:
            List of data sources with their DataFrames
        """
        data_sources = []
        
        if not os.path.exists(webhook_data_dir):
            self.logger.warning(f"Webhook data directory not found: {webhook_data_dir}")
            return data_sources
        
        for filename in os.listdir(webhook_data_dir):
            if filename.endswith('.csv') and not filename.startswith('rb2b_priority'):
                filepath = os.path.join(webhook_data_dir, filename)
                
                try:
                    df = pd.read_csv(filepath)
                    
                    # Determine source type
                    source_type = "Unknown"
                    if 'heyreach' in filename.lower() or 'linkedin' in filename.lower():
                        source_type = "LinkedIn campaigns"
                    elif 'instantly' in filename.lower() or 'email' in filename.lower():
                        source_type = "Email campaigns"
                    
                    data_sources.append({
                        'filename': filename,
                        'source_type': source_type,
                        'data': df,
                        'count': len(df)
                    })
                    
                    self.logger.info(f"📁 Loaded {len(df)} records from {source_type}: {filename}")
                    
                except Exception as e:
                    self.logger.error(f"Error loading {filename}: {e}")
        
        return data_sources
    
    def find_rb2b_priority_overlaps(self, rb2b_df: pd.DataFrame, other_sources: List[Dict]) -> List[Dict]:
        """
        Find overlaps with RB2B visitors as the primary source
        
        Args:
            rb2b_df: RB2B website visitors DataFrame
            other_sources: List of other data sources
            
        Returns:
            List of overlap records
        """
        overlaps = []
        
        for _, rb2b_row in rb2b_df.iterrows():
            rb2b_identifiers = self.extract_rb2b_identifiers(rb2b_row)
            
            overlap_record = {
                'rb2b_visitor': rb2b_row.to_dict(),
                'rb2b_identifiers': rb2b_identifiers,
                'matches': [],
                'priority': 'LOW'
            }
            
            # Check against all other sources
            for source in other_sources:
                source_matches = self.find_matches_in_source(rb2b_identifiers, source)
                if source_matches:
                    overlap_record['matches'].extend(source_matches)
            
            # Only include if there are matches
            if overlap_record['matches']:
                # Determine priority based on match quality and quantity
                overlap_record['priority'] = self.calculate_priority(overlap_record)
                overlaps.append(overlap_record)
        
        # Sort by priority (HIGH first)
        overlaps.sort(key=lambda x: x['priority'], reverse=True)
        
        return overlaps
    
    def extract_rb2b_identifiers(self, row: pd.Series) -> Dict[str, str]:
        """
        Extract identifiers from RB2B visitor record
        
        Args:
            row: RB2B data row
            
        Returns:
            Dictionary of normalized identifiers
        """
        identifiers = {}
        
        # Email
        email_fields = ['email', 'Email', 'email_address', 'Email Address']
        for field in email_fields:
            if field in row and pd.notna(row[field]):
                identifiers['email'] = str(row[field]).lower().strip()
                break
        
        # Company
        company_fields = ['company', 'Company', 'company_name', 'Company Name']
        for field in company_fields:
            if field in row and pd.notna(row[field]):
                identifiers['company'] = str(row[field]).lower().strip()
                break
        
        # Name
        name_fields = ['name', 'Name', 'full_name', 'Full Name']
        for field in name_fields:
            if field in row and pd.notna(row[field]):
                identifiers['name'] = str(row[field]).lower().strip()
                break
        
        # LinkedIn URL
        linkedin_fields = ['linkedin_url', 'LinkedIn', 'linkedin', 'LinkedIn URL']
        for field in linkedin_fields:
            if field in row and pd.notna(row[field]):
                linkedin_url = str(row[field]).strip()
                if 'linkedin.com' in linkedin_url.lower():
                    identifiers['linkedin'] = linkedin_url.lower()
                break
        
        return identifiers
    
    def find_matches_in_source(self, rb2b_identifiers: Dict[str, str], source: Dict) -> List[Dict]:
        """
        Find matches for RB2B visitor in a specific source
        
        Args:
            rb2b_identifiers: RB2B visitor identifiers
            source: Source data dictionary
            
        Returns:
            List of matches found
        """
        matches = []
        
        for _, row in source['data'].iterrows():
            match_types = []
            match_confidence = 0
            
            # Check email match (highest confidence)
            if 'email' in rb2b_identifiers:
                email_fields = ['email', 'lead_email', 'sender_email', 'Email']
                for field in email_fields:
                    if field in row and pd.notna(row[field]):
                        if rb2b_identifiers['email'] == str(row[field]).lower().strip():
                            match_types.append('email')
                            match_confidence += 10
                        break
            
            # Check name match (medium confidence)
            if 'name' in rb2b_identifiers:
                name_fields = ['name', 'full_name', 'lead_full_name', 'sender_full_name']
                for field in name_fields:
                    if field in row and pd.notna(row[field]):
                        if rb2b_identifiers['name'] == str(row[field]).lower().strip():
                            match_types.append('name')
                            match_confidence += 5
                        break
            
            # Check company match (lower confidence)
            if 'company' in rb2b_identifiers:
                company_fields = ['company', 'company_name', 'lead_company_name']
                for field in company_fields:
                    if field in row and pd.notna(row[field]):
                        if rb2b_identifiers['company'] == str(row[field]).lower().strip():
                            match_types.append('company')
                            match_confidence += 3
                        break
            
            # Check LinkedIn match (high confidence)
            if 'linkedin' in rb2b_identifiers:
                linkedin_fields = ['linkedin_url', 'profile_url', 'lead_profile_url']
                for field in linkedin_fields:
                    if field in row and pd.notna(row[field]):
                        if rb2b_identifiers['linkedin'] == str(row[field]).lower().strip():
                            match_types.append('linkedin')
                            match_confidence += 8
                        break
            
            # If we found matches, record them
            if match_types:
                matches.append({
                    'source_type': source['source_type'],
                    'source_filename': source['filename'],
                    'match_types': match_types,
                    'match_confidence': match_confidence,
                    'matched_record': row.to_dict()
                })
        
        return matches
    
    def calculate_priority(self, overlap_record: Dict) -> str:
        """
        Calculate priority level for an overlap
        
        Args:
            overlap_record: Overlap record
            
        Returns:
            Priority level (HIGH, MEDIUM, LOW)
        """
        total_confidence = sum(match['match_confidence'] for match in overlap_record['matches'])
        match_count = len(overlap_record['matches'])
        
        # High priority: Email match or multiple high-confidence matches
        if any('email' in match['match_types'] for match in overlap_record['matches']):
            return 'HIGH'
        elif total_confidence >= 15 or match_count >= 3:
            return 'HIGH'
        elif total_confidence >= 8 or match_count >= 2:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_rb2b_priority_report(self, rb2b_df: pd.DataFrame, overlaps: List[Dict]) -> Dict:
        """
        Generate priority analysis report
        
        Args:
            rb2b_df: RB2B DataFrame
            overlaps: List of overlaps
            
        Returns:
            Report dictionary
        """
        high_priority = [o for o in overlaps if o['priority'] == 'HIGH']
        medium_priority = [o for o in overlaps if o['priority'] == 'MEDIUM']
        low_priority = [o for o in overlaps if o['priority'] == 'LOW']
        
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_rb2b_visitors': len(rb2b_df),
                'visitors_with_overlaps': len(overlaps),
                'overlap_percentage': round((len(overlaps) / len(rb2b_df)) * 100, 2) if len(rb2b_df) > 0 else 0,
                'high_priority_overlaps': len(high_priority),
                'medium_priority_overlaps': len(medium_priority),
                'low_priority_overlaps': len(low_priority)
            },
            'high_priority_prospects': high_priority[:10],  # Top 10 for report
            'recommendations': self.generate_recommendations(high_priority, medium_priority)
        }
        
        return report
    
    def generate_recommendations(self, high_priority: List[Dict], medium_priority: List[Dict]) -> List[str]:
        """
        Generate actionable recommendations
        
        Args:
            high_priority: High priority overlaps
            medium_priority: Medium priority overlaps
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if high_priority:
            recommendations.append(f"🎯 IMMEDIATE ACTION: {len(high_priority)} high-priority website visitors are also in your outreach campaigns. Coordinate messaging to avoid prospect fatigue.")
            
            email_matches = sum(1 for o in high_priority if any('email' in m['match_types'] for m in o['matches']))
            if email_matches:
                recommendations.append(f"📧 {email_matches} visitors have exact email matches - perfect for personalized follow-up campaigns.")
        
        if medium_priority:
            recommendations.append(f"📊 REVIEW: {len(medium_priority)} medium-priority overlaps may represent the same prospects with different contact information.")
        
        if not high_priority and not medium_priority:
            recommendations.append("💡 No significant overlaps found. Consider expanding your outreach to include website visitors who haven't been contacted yet.")
        
        return recommendations
    
    def save_priority_results(self, report: Dict):
        """
        Save priority analysis results
        
        Args:
            report: Analysis report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON report
        os.makedirs("processed", exist_ok=True)
        json_filename = f"processed/rb2b_priority_analysis_{timestamp}.json"
        
        with open(json_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        self.logger.info(f"💾 Saved priority analysis: {json_filename}")

def main():
    """Main function to run RB2B priority analysis"""
    
    # Your RB2B Google Sheets URL
    rb2b_sheets_url = "https://docs.google.com/spreadsheets/d/1jPwTgvGwQEG9llkpKgWu8PNYXY-OaUMUvNYGxIWUe0I/edit?gid=0#gid=0"
    
    analyzer = RB2BPriorityAnalyzer()
    
    print("🎯 Starting RB2B Priority Overlap Analysis...")
    print("=" * 60)
    
    result = analyzer.analyze_rb2b_priority_overlaps(rb2b_sheets_url)
    
    if result['success']:
        print(f"✅ Analysis Complete!")
        print(f"📊 RB2B Website Visitors: {result['rb2b_visitors']}")
        print(f"🔍 Total Overlaps Found: {result.get('total_overlaps', 0)}")
        print(f"🎯 High Priority Prospects: {result.get('high_priority_prospects', 0)}")
        
        if result.get('report'):
            recommendations = result['report'].get('recommendations', [])
            if recommendations:
                print("\n💡 RECOMMENDATIONS:")
                for rec in recommendations:
                    print(f"   {rec}")
    else:
        print(f"❌ Analysis Failed: {result.get('error', 'Unknown error')}")
        print("\n🔧 To fix Google Sheets access:")
        print("   1. Open your Google Sheet")
        print("   2. Click 'Share' button")
        print("   3. Change to 'Anyone with the link can view'")
        print("   4. Copy the new link and try again")

if __name__ == "__main__":
    main()