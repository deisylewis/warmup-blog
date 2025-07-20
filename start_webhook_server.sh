#!/bin/bash

# Webhook Server Startup Script

echo "🚀 Starting Webhook Receiver for RB2B and HeyReach..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
pip install flask>=2.3.0 > /dev/null 2>&1

# Get server IP
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || hostname -I | awk '{print $1}')

echo "📡 Your Webhook URLs:"
echo "   RB2B:     http://$SERVER_IP:5000/webhook/rb2b"
echo "   HeyReach: http://$SERVER_IP:5000/webhook/heyreach"
echo "   Test:     http://$SERVER_IP:5000/webhook/test"
echo "   Health:   http://$SERVER_IP:5000/health"
echo ""

echo "🔧 Add these URLs to your RB2B and HeyReach webhook configurations"
echo "📋 Don't forget to add the X-Client-Name header!"
echo ""

echo "🎯 Starting webhook receiver on port 5000..."
echo "   Press Ctrl+C to stop"
echo ""

# Start the webhook receiver
python3 webhook_receiver.py --host 0.0.0.0 --port 5000