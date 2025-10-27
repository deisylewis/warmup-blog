# 🎯 Webhook Setup Guide

## 📡 Webhook URLs for RB2B and HeyReach

Here are the **exact webhook URLs** you need to add in RB2B and HeyReach:

### 🌐 **Your Webhook Server URLs**

Replace `YOUR_SERVER_IP` with your server's IP address or domain:

```
RB2B Webhook URL:     http://YOUR_SERVER_IP:5000/webhook/rb2b
HeyReach Webhook URL: http://YOUR_SERVER_IP:5000/webhook/heyreach
Test Webhook URL:     http://YOUR_SERVER_IP:5000/webhook/test
```

**Example URLs:**
```
http://123.45.67.89:5000/webhook/rb2b
http://123.45.67.89:5000/webhook/heyreach
http://myserver.com:5000/webhook/rb2b
http://myserver.com:5000/webhook/heyreach
```

## 🚀 **Quick Start**

### 1. **Start the Webhook Server**
```bash
# Install Flask dependency
source venv/bin/activate
pip install flask>=2.3.0

# Start the webhook receiver
python webhook_receiver.py

# Or with custom port
python webhook_receiver.py --port 8080
```

### 2. **Test the Webhook Server**
```bash
# Test if server is running
curl http://localhost:5000/health

# Should return: {"status": "healthy", "timestamp": "...", "service": "webhook_receiver"}
```

### 3. **Test Webhook Reception**
```bash
# Test webhook endpoint
curl -X POST http://localhost:5000/webhook/test \
  -H "Content-Type: application/json" \
  -H "X-Client-Name: test_client" \
  -d '{"test": "data", "name": "John Doe", "email": "john@example.com"}'
```

## 🔧 **Webhook Configuration in RB2B**

### **Step 1: Login to RB2B Dashboard**
1. Go to your RB2B account settings
2. Navigate to **Integrations** or **Webhooks** section

### **Step 2: Add Webhook**
- **Webhook URL**: `http://YOUR_SERVER_IP:5000/webhook/rb2b`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Events**: Select all visitor tracking events
- **Custom Headers** (add this):
  ```
  X-Client-Name: YOUR_CLIENT_NAME
  ```

### **Step 3: Optional Security**
If RB2B supports webhook signatures:
- **Secret Key**: Add to your `.env` as `RB2B_WEBHOOK_SECRET=your_secret_here`

## 🔧 **Webhook Configuration in HeyReach**

### **Step 1: Login to HeyReach Dashboard**
1. Go to your HeyReach account settings
2. Navigate to **Integrations**, **API**, or **Webhooks** section

### **Step 2: Add Webhook**
- **Webhook URL**: `http://YOUR_SERVER_IP:5000/webhook/heyreach`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Events**: Select campaign and lead events
- **Custom Headers** (add this):
  ```
  X-Client-Name: YOUR_CLIENT_NAME
  ```

### **Step 3: Optional Security**
If HeyReach supports webhook signatures:
- **Secret Key**: Add to your `.env` as `HEYREACH_WEBHOOK_SECRET=your_secret_here`

## 📋 **Required Headers**

When configuring webhooks, make sure to include this custom header:

```
X-Client-Name: your_actual_client_name
```

**Examples:**
- `X-Client-Name: acme_corp`
- `X-Client-Name: tech_startup`
- `X-Client-Name: client_001`

This header tells the webhook receiver which client the data belongs to.

## 🔒 **Security Configuration (Optional)**

Add these to your `.env` file for webhook security:

```env
# Webhook Security (optional)
RB2B_WEBHOOK_SECRET=your_rb2b_secret_key
HEYREACH_WEBHOOK_SECRET=your_heyreach_secret_key
WEBHOOK_DATA_DIR=./webhook_data
```

## 🧪 **Testing Your Webhooks**

### **Test RB2B Webhook**
```bash
curl -X POST http://YOUR_SERVER_IP:5000/webhook/rb2b \
  -H "Content-Type: application/json" \
  -H "X-Client-Name: test_client" \
  -d '{
    "visitors": [
      {
        "email": "visitor@example.com",
        "company": "Example Corp",
        "visit_date": "2024-01-15",
        "page_views": 5
      }
    ]
  }'
```

### **Test HeyReach Webhook**
```bash
curl -X POST http://YOUR_SERVER_IP:5000/webhook/heyreach \
  -H "Content-Type: application/json" \
  -H "X-Client-Name: test_client" \
  -d '{
    "campaigns": [
      {
        "email": "lead@example.com",
        "linkedin_profile": "https://linkedin.com/in/lead",
        "campaign_name": "Q1 Outreach",
        "status": "replied"
      }
    ]
  }'
```

## 📊 **What Happens When Webhooks Are Received**

1. **Data Reception**: Webhook receives JSON data from RB2B/HeyReach
2. **CSV Conversion**: Data is automatically converted to CSV format
3. **Client Tagging**: Files are tagged with client name: `{client}_rb2b_website_visitors_{timestamp}.csv`
4. **Source Labeling**: 
   - RB2B → "Website visitors"
   - HeyReach → "LinkedIn campaigns"
   - Instantly → "Email campaigns"
5. **Auto-Processing**: OpenAI overlap analysis starts automatically
6. **Logging**: All activity is logged to `webhook_receiver.log`

## 🔍 **Monitoring Webhooks**

### **Check Server Status**
```bash
curl http://YOUR_SERVER_IP:5000/health
```

### **View Logs**
```bash
tail -f webhook_receiver.log
```

### **Check Received Files**
```bash
ls -la webhook_data/
```

### **Manual Analysis Trigger**
```bash
curl -X POST http://YOUR_SERVER_IP:5000/trigger-analysis
```

## 🌐 **Production Deployment**

### **Using a Reverse Proxy (Recommended)**
```nginx
# Nginx configuration
server {
    listen 80;
    server_name your-domain.com;
    
    location /webhook/ {
        proxy_pass http://localhost:5000/webhook/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **Using HTTPS (Recommended)**
```bash
# Use Let's Encrypt for SSL
sudo certbot --nginx -d your-domain.com
```

### **Process Management**
```bash
# Using systemd service
sudo nano /etc/systemd/system/webhook-receiver.service

[Unit]
Description=Webhook Receiver
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/your/app
ExecStart=/path/to/your/app/venv/bin/python webhook_receiver.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable webhook-receiver
sudo systemctl start webhook-receiver
```

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **Connection Refused**
   - Make sure webhook server is running
   - Check if port 5000 is accessible
   - Verify firewall settings

2. **No Data Received**
   - Check webhook URL in RB2B/HeyReach
   - Verify X-Client-Name header is set
   - Check webhook_receiver.log for errors

3. **Processing Fails**
   - Ensure OpenAI API key is configured
   - Check CSV data format
   - Review error logs

### **Debug Commands:**
```bash
# Check if server is running
ps aux | grep webhook_receiver

# Check port usage
netstat -tlnp | grep 5000

# Test webhook locally
curl -X POST localhost:5000/webhook/test -d '{"test": true}'
```

## 📞 **Support**

If you encounter issues:
1. Check the logs: `webhook_receiver.log`
2. Test with the `/webhook/test` endpoint first
3. Verify your server is accessible from the internet
4. Ensure all dependencies are installed

---

**Ready to receive webhooks!** 🎉

Your webhook URLs are:
- **RB2B**: `http://YOUR_SERVER_IP:5000/webhook/rb2b`
- **HeyReach**: `http://YOUR_SERVER_IP:5000/webhook/heyreach`