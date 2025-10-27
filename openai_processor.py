import openai
import pandas as pd
import json
import logging
from typing import Optional, Dict, Any, List
import os
from datetime import datetime

class OpenAIProcessor:
    """
    A class to process CSV data using OpenAI API
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4", max_tokens: int = 2000):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        self.logger = logging.getLogger(__name__)
    
    def process_csv_with_prompt(self, csv_filepath: str, prompt: str, output_dir: str = "./processed") -> Optional[Dict[str, Any]]:
        """
        Process CSV data with a custom OpenAI prompt
        
        Args:
            csv_filepath: Path to the CSV file
            prompt: Custom prompt for OpenAI processing
            output_dir: Directory to save processed results
            
        Returns:
            Dictionary with processing results or None if failed
        """
        try:
            # Ensure output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Read CSV data
            df = pd.read_csv(csv_filepath)
            self.logger.info(f"Processing CSV with {len(df)} rows using OpenAI...")
            
            # Convert CSV to string format for OpenAI
            csv_preview = df.head(10).to_string(index=False)
            csv_summary = f"CSV File: {csv_filepath}\nRows: {len(df)}\nColumns: {df.columns.tolist()}\n\nPreview (first 10 rows):\n{csv_preview}"
            
            # Prepare the full prompt
            full_prompt = f"{prompt}\n\nCSV Data:\n{csv_summary}"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analyst assistant. Analyze the provided CSV data and respond according to the user's request."},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            # Extract response
            ai_response = response.choices[0].message.content
            
            # Save results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_filename = f"openai_analysis_{timestamp}.json"
            result_filepath = os.path.join(output_dir, result_filename)
            
            result_data = {
                'timestamp': timestamp,
                'source_csv': csv_filepath,
                'prompt': prompt,
                'csv_info': {
                    'rows': len(df),
                    'columns': df.columns.tolist(),
                    'file_size': os.path.getsize(csv_filepath)
                },
                'openai_response': ai_response,
                'model_used': self.model,
                'tokens_used': response.usage.total_tokens if response.usage else None
            }
            
            # Save to JSON file
            with open(result_filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"OpenAI analysis saved to: {result_filepath}")
            return result_data
            
        except Exception as e:
            self.logger.error(f"Error processing CSV with OpenAI: {e}")
            return None
    
    def analyze_csv_insights(self, csv_filepath: str, output_dir: str = "./processed") -> Optional[Dict[str, Any]]:
        """
        Perform automated insights analysis on CSV data
        
        Args:
            csv_filepath: Path to the CSV file
            output_dir: Directory to save processed results
            
        Returns:
            Dictionary with analysis results or None if failed
        """
        default_prompt = """
        Please analyze this CSV data and provide:
        1. A summary of the data structure and content
        2. Key insights and patterns you observe
        3. Data quality assessment (missing values, duplicates, etc.)
        4. Recommendations for data improvement or next steps
        5. Any anomalies or interesting findings
        
        Format your response in a clear, structured manner with bullet points and sections.
        """
        
        return self.process_csv_with_prompt(csv_filepath, default_prompt, output_dir)
    
    def generate_data_summary(self, csv_filepath: str, output_dir: str = "./processed") -> Optional[Dict[str, Any]]:
        """
        Generate a comprehensive data summary using OpenAI
        
        Args:
            csv_filepath: Path to the CSV file
            output_dir: Directory to save processed results
            
        Returns:
            Dictionary with summary results or None if failed
        """
        summary_prompt = """
        Create a comprehensive executive summary of this CSV data including:
        1. Dataset overview (what type of data this appears to be)
        2. Key statistics and metrics
        3. Main trends or patterns
        4. Business implications (if applicable)
        5. Data completeness and quality notes
        
        Present this as a professional business report summary.
        """
        
        return self.process_csv_with_prompt(csv_filepath, summary_prompt, output_dir)
    
    def process_multiple_csvs(self, csv_filepaths: List[str], prompt: str, output_dir: str = "./processed") -> List[Dict[str, Any]]:
        """
        Process multiple CSV files with the same prompt
        
        Args:
            csv_filepaths: List of paths to CSV files
            prompt: Prompt to use for all files
            output_dir: Directory to save processed results
            
        Returns:
            List of processing results
        """
        results = []
        for csv_path in csv_filepaths:
            self.logger.info(f"Processing {csv_path}...")
            result = self.process_csv_with_prompt(csv_path, prompt, output_dir)
            if result:
                results.append(result)
        
        return results
    
    def compare_csvs(self, csv_filepaths: List[str], output_dir: str = "./processed") -> Optional[Dict[str, Any]]:
        """
        Compare multiple CSV files using OpenAI
        
        Args:
            csv_filepaths: List of paths to CSV files to compare
            output_dir: Directory to save comparison results
            
        Returns:
            Dictionary with comparison results or None if failed
        """
        try:
            if len(csv_filepaths) < 2:
                self.logger.error("At least 2 CSV files are required for comparison")
                return None
            
            # Read and summarize each CSV
            csv_summaries = []
            for i, csv_path in enumerate(csv_filepaths):
                df = pd.read_csv(csv_path)
                summary = f"File {i+1}: {os.path.basename(csv_path)}\nRows: {len(df)}\nColumns: {df.columns.tolist()}\nSample data:\n{df.head(3).to_string(index=False)}\n"
                csv_summaries.append(summary)
            
            # Create comparison prompt
            comparison_prompt = f"""
            Compare these {len(csv_filepaths)} CSV files and provide:
            1. Similarities and differences in structure
            2. Data overlap or unique elements
            3. Quality comparison
            4. Recommendations for data consolidation or analysis
            5. Key insights from the comparison
            
            CSV Files to Compare:
            {chr(10).join(csv_summaries)}
            """
            
            # Process with OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analyst expert in comparing and analyzing datasets."},
                    {"role": "user", "content": comparison_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Save comparison results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_filename = f"csv_comparison_{timestamp}.json"
            result_filepath = os.path.join(output_dir, result_filename)
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            result_data = {
                'timestamp': timestamp,
                'compared_files': csv_filepaths,
                'comparison_analysis': ai_response,
                'model_used': self.model,
                'tokens_used': response.usage.total_tokens if response.usage else None
            }
            
            with open(result_filepath, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"CSV comparison saved to: {result_filepath}")
            return result_data
            
        except Exception as e:
            self.logger.error(f"Error comparing CSVs with OpenAI: {e}")
            return None