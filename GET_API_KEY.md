# 🔑 How to Get OpenAI API Key for Stock Pitch AI

## 📝 Step 1: Create OpenAI Account
1. **Visit OpenAI**: Go to https://openai.com/
2. **Sign Up**: Click "Sign up" in the top right corner
3. **Create Account**: 
   - Use your email address
   - Create a strong password
   - Verify your email when prompted
4. **Phone Verification**: You'll need to verify your phone number

## 🚀 Step 2: Access API Platform
1. **Login**: Go to https://platform.openai.com/
2. **Navigate to API**: Once logged in, you'll see the API dashboard
3. **Go to API Keys**: 
   - Click on your profile picture (top right)
   - Select "View API keys" 
   - Or go directly to: https://platform.openai.com/api-keys

## 🔐 Step 3: Create Your API Key
1. **Create Key**: Click the green "Create new secret key" button
2. **Name Your Key**: Give it a descriptive name like "Stock-Pitch-AI"
3. **Copy Immediately**: 
   - ⚠️ **IMPORTANT**: Copy the key RIGHT NOW!
   - You will NEVER see this key again once you close the dialog
   - It starts with `sk-` followed by a long string of characters
4. **Store Safely**: Save it in a secure location (password manager recommended)

## 💳 Step 4: Set Up Billing (Required)
1. **Go to Billing**: Visit https://platform.openai.com/account/billing
2. **Add Payment Method**: 
   - Click "Add payment method"
   - Enter your credit/debit card details
3. **Set Usage Limits** (Recommended):
   - Set a monthly limit of $20-50 for safety
   - This prevents unexpected charges
4. **Initial Credit**: OpenAI sometimes provides $5-18 in free credits for new accounts

## 🎯 Step 5: Use in Stock Pitch AI

### Method 1: Direct Input (Easiest)
1. **Start the App**: Run `streamlit run app.py`
2. **Select Premium Mode**: In the sidebar, choose "Premium (OpenAI GPT-4)"
3. **Enter API Key**: Paste your API key in the text input field
4. **Start Analyzing**: Enter a stock symbol and generate your pitch!

### Method 2: Environment File (More Secure)
1. **Create .env file**: In your project folder, create a file named `.env`
2. **Add your key**: Write `OPENAI_API_KEY=sk-your-actual-key-here`
3. **Start the app**: The app will automatically detect and use your key
4. **Select Premium**: Choose "Premium (OpenAI GPT-4)" mode

## 💰 Cost Information (Current Pricing)

### GPT-4 Pricing:
- **Per Stock Analysis**: ~$0.10-0.25 per comprehensive analysis
- **Monthly Budget**: $20-50 should handle 100-500+ analyses
- **Pay-per-use**: Only charged for what you actually use

### Usage Examples:
- **Light User** (5-10 stocks/month): $2-5/month
- **Regular User** (20-50 stocks/month): $5-15/month  
- **Heavy User** (100+ stocks/month): $15-50/month

### Free Alternative:
- **$0 Cost**: Use the Free Mode (no API key needed)
- **Still Powerful**: DCF analysis, WACC calculation, recommendations
- **Upgrade Anytime**: Switch to Premium mode when ready

## 🔒 Security Best Practices

### ✅ Do's:
- Store API key in a password manager
- Use environment variables (`.env` file)
- Set monthly spending limits
- Monitor usage regularly at https://platform.openai.com/usage

### ❌ Don'ts:
- Never share your API key with anyone
- Never commit API keys to GitHub/Git
- Don't use the same key for multiple projects
- Don't ignore unusual usage spikes

## 🆘 Troubleshooting

### Common Issues:
1. **"Invalid API Key"**: 
   - Double-check you copied the entire key (starts with `sk-`)
   - Make sure no extra spaces before/after the key

2. **"Insufficient Credits"**: 
   - Add a payment method to your OpenAI account
   - Check your billing limits

3. **"Rate Limit Exceeded"**: 
   - Wait a few minutes and try again
   - You're making requests too quickly

4. **Still Having Issues?**: 
   - Use Free Mode while troubleshooting
   - Check OpenAI Status: https://status.openai.com/

## 🎉 Ready to Go!

Once you have your API key:
1. ✅ **Start the app**: `streamlit run app.py`
2. ✅ **Select Premium mode** in the sidebar
3. ✅ **Enter your API key**
4. ✅ **Analyze any stock** (try AAPL, MSFT, GOOGL)
5. ✅ **Get AI-powered insights** in your PowerPoint presentation!

**Need help?** The Free Mode works great without any API key and includes all the core financial analysis features!
