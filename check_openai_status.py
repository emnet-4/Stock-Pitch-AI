#!/usr/bin/env python3
"""
Check OpenAI API status and account info
"""

import openai
import sys

def check_openai_status():
    """Check OpenAI API status with your key"""
    
    # Get API key from user
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    try:
        print("🔍 Testing OpenAI API connection...")
        
        # Initialize client
        client = openai.OpenAI(api_key=api_key)
        
        # Test different models to see what's available
        models_to_test = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4o",
            "gpt-4o-mini"
        ]
        
        for model in models_to_test:
            try:
                print(f"\n🧪 Testing model: {model}")
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": "Hello, just testing if this model works. Respond with 'YES' if you can process this."}
                    ],
                    max_tokens=10
                )
                
                print(f"✅ {model}: WORKS - Response: {response.choices[0].message.content}")
                
            except Exception as e:
                print(f"❌ {model}: FAILED - {str(e)}")
        
        print("\n" + "="*50)
        print("📊 API KEY STATUS:")
        print(f"Key: {api_key[:8]}...")
        
        # Try to get account info
        try:
            # This might not work with the current API, but let's try
            usage = client.usage.retrieve()
            print(f"Usage info available: {usage}")
        except:
            print("Usage info not accessible via API")
        
    except Exception as e:
        print(f"❌ Failed to connect to OpenAI: {str(e)}")
        
        # Check specific error types
        if "quota" in str(e).lower():
            print("\n💡 QUOTA ISSUE DETECTED:")
            print("- Your free trial credits may be exhausted")
            print("- Go to https://platform.openai.com/account/billing")
            print("- Check your usage and available credits")
            print("- Add a payment method if needed")
        
        elif "404" in str(e) or "model" in str(e).lower():
            print("\n💡 MODEL ISSUE DETECTED:")
            print("- The model you're trying to use isn't available")
            print("- Try gpt-3.5-turbo or gpt-4o-mini")
        
        elif "auth" in str(e).lower() or "401" in str(e):
            print("\n💡 AUTHENTICATION ISSUE:")
            print("- Check if your API key is correct")
            print("- Make sure it starts with 'sk-'")

if __name__ == "__main__":
    print("🔧 OpenAI API Status Checker")
    print("="*50)
    check_openai_status()
