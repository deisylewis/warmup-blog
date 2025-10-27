# 🚀 Railway Deployment Guide

## 📋 **Step-by-Step Deployment**

### **Step 1: Create Railway Account**
1. Go to: https://railway.app
2. Click **"Start a New Project"**
3. Sign up with **GitHub** (recommended)

### **Step 2: Deploy from GitHub**
1. **Connect your GitHub** account to Railway
2. **Create a new repository** on GitHub with your code
3. **Push all files** to your GitHub repository
4. In Railway, click **"Deploy from GitHub repo"**
5. **Select your repository**

### **Step 3: Configure Environment Variables**
In Railway dashboard, go to **Variables** tab and add:

```env
OPENAI_API_KEY=your_openai_api_key_here
CLIENT1_NAME=your_client_name
CLIENT1_INSTANTLY_API_KEY=OWJmMWQ1MGUtOWFhNC00MTg3LWJkYWUtMDYyNDg2MDI4Y2IwOlZvWWZ5VndrYmJ4RA==
CLIENT1_INSTANTLY_API_URL=https://api.instantly.ai/v1/exports
WEBHOOK_DATA_DIR=./webhook_data
```

### **Step 4: Deploy**
1. Railway will **automatically deploy** your app
2. Wait for deployment to complete (2-3 minutes)
3. Railway will provide a **public URL** like: `https://your-app-name.railway.app`

### **Step 5: Get Your Webhook URLs**
After deployment, your webhook URLs will be:

```
HeyReach: https://your-app-name.railway.app/webhook/heyreach
Test:     https://your-app-name.railway.app/webhook/test
Health:   https://your-app-name.railway.app/health
```

## 🔄 **Alternative: Quick Deploy (Without GitHub)**

If you don't want to use GitHub, I can help you deploy using Railway CLI:

### **Option A: Railway CLI**
```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login to Railway
railway login

# Deploy from current directory
railway up
```

### **Option B: Zip Upload**
1. **Download all files** as a zip
2. Go to **Railway dashboard**
3. Click **"Deploy from template"**
4. **Upload zip file**

## ✅ **After Deployment**

### **Test Your Deployment:**
```bash
# Test health endpoint
curl https://your-app-name.railway.app/health

# Test webhook
curl -X POST https://your-app-name.railway.app/webhook/test \
  -H "Content-Type: application/json" \
  -H "X-Client-Name: test" \
  -d '{"test": "data"}'
```

### **Update HeyReach:**
Replace your webhook.site URL with:
```
https://your-app-name.railway.app/webhook/heyreach
```

## 📊 **What You'll Get:**

- ✅ **Permanent webhook URL** (no expiration)
- ✅ **Automatic scaling** and uptime
- ✅ **Free tier** (500 hours/month)
- ✅ **HTTPS** by default
- ✅ **Automatic deployments** when you update code

## 🔧 **Files Ready for Deployment:**

All these files are configured and ready:
- ✅ `webhook_receiver.py` - Main webhook server
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Deployment configuration
- ✅ `railway.json` - Railway settings
- ✅ `runtime.txt` - Python version

## 🚀 **Ready to Deploy!**

Choose your preferred method:
1. **GitHub + Railway** (recommended - easiest updates)
2. **Railway CLI** (command line)
3. **Zip upload** (simplest one-time)

Let me know which method you'd like to use!