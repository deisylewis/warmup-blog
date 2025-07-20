#!/usr/bin/env python3
"""
Webhook Receiver for RB2B and HeyReach
This Flask application receives webhook data from RB2B and HeyReach,
saves it as CSV files, and triggers the OpenAI processing pipeline.
"""

from flask import Flask, request, jsonify
import json
import csv
import os
import logging
import pandas as pd
from datetime import datetime
import hashlib
import hmac
from typing import Dict, Any, List
import threading
import time
from main import CSVProcessingApp

class WebhookReceiver:
    """Webhook receiver and processor"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_logging()
        self.setup_routes()
        self.csv_processor = CSVProcessingApp()
        
        # Webhook security (optional)
        self.rb2b_secret = os.getenv('RB2B_WEBHOOK_SECRET', '')
        self.heyreach_secret = os.getenv('HEYREACH_WEBHOOK_SECRET', '')
        
        # Directories
        self.webhook_data_dir = os.getenv('WEBHOOK_DATA_DIR', './webhook_data')
        os.makedirs(self.webhook_data_dir, exist_ok=True)
        
    def setup_logging(self):
        """Setup logging for webhook receiver"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('webhook_receiver.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_routes(self):
        """Setup Flask routes for webhooks"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'webhook_receiver'
            })
        
        @self.app.route('/webhook/rb2b', methods=['POST'])
        def rb2b_webhook():
            """RB2B webhook endpoint"""
            return self.handle_rb2b_webhook()
        
        @self.app.route('/webhook/heyreach', methods=['POST'])
        def heyreach_webhook():
            """HeyReach webhook endpoint"""
            return self.handle_heyreach_webhook()
        
        @self.app.route('/webhook/instantly', methods=['POST'])
        def instantly_webhook():
            """Instantly webhook endpoint (if they add webhook support)"""
            return self.handle_instantly_webhook()
        
        @self.app.route('/webhook/test', methods=['POST'])
        def test_webhook():
            """Test webhook endpoint for debugging"""
            return self.handle_test_webhook()
        
        @self.app.route('/trigger-analysis', methods=['POST'])
        def trigger_analysis():
            """Manually trigger analysis of webhook data"""
            return self.trigger_manual_analysis()
    
    def verify_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """Verify webhook signature for security"""
        if not secret or not signature:
            return True  # Skip verification if no secret configured
        
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def handle_rb2b_webhook(self):
        """Handle RB2B webhook data"""
        try:
            # Get client name from headers or use default
            client_name = request.headers.get('X-Client-Name', 'unknown_client')
            
            # Verify signature if configured
            signature = request.headers.get('X-RB2B-Signature', '')
            if not self.verify_signature(request.data, signature, self.rb2b_secret):
                self.logger.warning("RB2B webhook signature verification failed")
                return jsonify({'error': 'Invalid signature'}), 401
            
            # Get JSON data
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            self.logger.info(f"Received RB2B webhook data for client: {client_name}")
            
            # Process and save as CSV
            csv_file = self.save_rb2b_data_as_csv(data, client_name)
            
            if csv_file:
                # Trigger processing in background
                threading.Thread(
                    target=self.process_webhook_data,
                    args=([csv_file], 'rb2b', client_name),
                    daemon=True
                ).start()
                
                return jsonify({
                    'status': 'success',
                    'message': 'RB2B data received and processing started',
                    'file': csv_file,
                    'client': client_name
                })
            else:
                return jsonify({'error': 'Failed to save data'}), 500
                
        except Exception as e:
            self.logger.error(f"Error handling RB2B webhook: {e}")
            return jsonify({'error': str(e)}), 500
    
    def handle_heyreach_webhook(self):
        """Handle HeyReach webhook data"""
        try:
            # Get client name from headers or use default
            client_name = request.headers.get('X-Client-Name', 'unknown_client')
            
            # Verify signature if configured
            signature = request.headers.get('X-HeyReach-Signature', '')
            if not self.verify_signature(request.data, signature, self.heyreach_secret):
                self.logger.warning("HeyReach webhook signature verification failed")
                return jsonify({'error': 'Invalid signature'}), 401
            
            # Get JSON data
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            self.logger.info(f"Received HeyReach webhook data for client: {client_name}")
            
            # Process and save as CSV
            csv_file = self.save_heyreach_data_as_csv(data, client_name)
            
            if csv_file:
                # Trigger processing in background
                threading.Thread(
                    target=self.process_webhook_data,
                    args=([csv_file], 'heyreach', client_name),
                    daemon=True
                ).start()
                
                return jsonify({
                    'status': 'success',
                    'message': 'HeyReach data received and processing started',
                    'file': csv_file,
                    'client': client_name
                })
            else:
                return jsonify({'error': 'Failed to save data'}), 500
                
        except Exception as e:
            self.logger.error(f"Error handling HeyReach webhook: {e}")
            return jsonify({'error': str(e)}), 500
    
    def handle_instantly_webhook(self):
        """Handle Instantly webhook data"""
        try:
            client_name = request.headers.get('X-Client-Name', 'unknown_client')
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            self.logger.info(f"Received Instantly webhook data for client: {client_name}")
            
            csv_file = self.save_instantly_data_as_csv(data, client_name)
            
            if csv_file:
                threading.Thread(
                    target=self.process_webhook_data,
                    args=([csv_file], 'instantly', client_name),
                    daemon=True
                ).start()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Instantly data received and processing started',
                    'file': csv_file,
                    'client': client_name
                })
            else:
                return jsonify({'error': 'Failed to save data'}), 500
                
        except Exception as e:
            self.logger.error(f"Error handling Instantly webhook: {e}")
            return jsonify({'error': str(e)}), 500
    
    def handle_test_webhook(self):
        """Handle test webhook for debugging"""
        try:
            data = request.get_json() or {}
            headers = dict(request.headers)
            
            self.logger.info("Received test webhook data")
            self.logger.info(f"Headers: {headers}")
            self.logger.info(f"Data: {json.dumps(data, indent=2)}")
            
            return jsonify({
                'status': 'success',
                'message': 'Test webhook received successfully',
                'received_data': data,
                'received_headers': headers
            })
            
        except Exception as e:
            self.logger.error(f"Error handling test webhook: {e}")
            return jsonify({'error': str(e)}), 500
    
    def save_rb2b_data_as_csv(self, data: Dict[Any, Any], client_name: str) -> str:
        """Convert RB2B webhook data to CSV format"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{client_name}_rb2b_website_visitors_{timestamp}.csv"
            filepath = os.path.join(self.webhook_data_dir, filename)
            
            # Handle different data structures
            if isinstance(data, dict):
                if 'visitors' in data:
                    # Data has visitors array
                    df = pd.DataFrame(data['visitors'])
                elif 'data' in data:
                    # Data has data array
                    df = pd.DataFrame(data['data'])
                else:
                    # Single record or direct data
                    df = pd.DataFrame([data])
            elif isinstance(data, list):
                # Array of records
                df = pd.DataFrame(data)
            else:
                self.logger.error("Unexpected data format from RB2B webhook")
                return None
            
            # Add source and client labels
            df['source'] = 'Website visitors'
            df['client_name'] = client_name
            df['webhook_timestamp'] = datetime.now().isoformat()
            
            # Save as CSV
            df.to_csv(filepath, index=False)
            self.logger.info(f"Saved RB2B data to: {filepath}")
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving RB2B data as CSV: {e}")
            return None
    
    def save_heyreach_data_as_csv(self, data: Dict[Any, Any], client_name: str) -> str:
        """Convert HeyReach webhook data to CSV format"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{client_name}_heyreach_linkedin_campaigns_{timestamp}.csv"
            filepath = os.path.join(self.webhook_data_dir, filename)
            
            # Handle different data structures
            if isinstance(data, dict):
                if 'campaigns' in data:
                    df = pd.DataFrame(data['campaigns'])
                elif 'leads' in data:
                    df = pd.DataFrame(data['leads'])
                elif 'data' in data:
                    df = pd.DataFrame(data['data'])
                else:
                    df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                self.logger.error("Unexpected data format from HeyReach webhook")
                return None
            
            # Add source and client labels
            df['source'] = 'LinkedIn campaigns'
            df['client_name'] = client_name
            df['webhook_timestamp'] = datetime.now().isoformat()
            
            # Save as CSV
            df.to_csv(filepath, index=False)
            self.logger.info(f"Saved HeyReach data to: {filepath}")
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving HeyReach data as CSV: {e}")
            return None
    
    def save_instantly_data_as_csv(self, data: Dict[Any, Any], client_name: str) -> str:
        """Convert Instantly webhook data to CSV format"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{client_name}_instantly_email_campaigns_{timestamp}.csv"
            filepath = os.path.join(self.webhook_data_dir, filename)
            
            # Handle different data structures
            if isinstance(data, dict):
                if 'campaigns' in data:
                    df = pd.DataFrame(data['campaigns'])
                elif 'leads' in data:
                    df = pd.DataFrame(data['leads'])
                elif 'data' in data:
                    df = pd.DataFrame(data['data'])
                else:
                    df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                self.logger.error("Unexpected data format from Instantly webhook")
                return None
            
            # Add source and client labels
            df['source'] = 'Email campaigns'
            df['client_name'] = client_name
            df['webhook_timestamp'] = datetime.now().isoformat()
            
            # Save as CSV
            df.to_csv(filepath, index=False)
            self.logger.info(f"Saved Instantly data to: {filepath}")
            
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving Instantly data as CSV: {e}")
            return None
    
    def process_webhook_data(self, csv_files: List[str], source: str, client_name: str):
        """Process webhook data using the existing OpenAI pipeline"""
        try:
            self.logger.info(f"Processing webhook data from {source} for client {client_name}")
            
            # Use the existing CSV processor
            result = self.csv_processor.run_full_pipeline(
                sources=[source],
                analysis_type="overlaps"  # Always run overlap analysis
            )
            
            if result['success']:
                self.logger.info(f"Successfully processed webhook data for {client_name}")
            else:
                self.logger.error(f"Failed to process webhook data for {client_name}")
                
        except Exception as e:
            self.logger.error(f"Error processing webhook data: {e}")
    
    def trigger_manual_analysis(self):
        """Manually trigger analysis of all webhook data"""
        try:
            # Find all CSV files in webhook data directory
            csv_files = []
            for file in os.listdir(self.webhook_data_dir):
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(self.webhook_data_dir, file))
            
            if not csv_files:
                return jsonify({'message': 'No CSV files found to analyze'}), 200
            
            # Run overlap analysis
            threading.Thread(
                target=self.process_webhook_data,
                args=(csv_files, 'all', 'manual_trigger'),
                daemon=True
            ).start()
            
            return jsonify({
                'status': 'success',
                'message': f'Analysis started for {len(csv_files)} CSV files',
                'files': csv_files
            })
            
        except Exception as e:
            self.logger.error(f"Error triggering manual analysis: {e}")
            return jsonify({'error': str(e)}), 500
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the webhook receiver"""
        self.logger.info(f"Starting webhook receiver on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Main function to run the webhook receiver"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Webhook Receiver for RB2B and HeyReach')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    receiver = WebhookReceiver()
    receiver.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()