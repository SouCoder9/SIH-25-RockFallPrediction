#!/usr/bin/env python3
"""
Test script to verify that environment variables are loading correctly.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

print("🔍 Environment Variable Test")
print("=" * 50)

# Test Twilio environment variables
twilio_vars = [
    "TWILIO_ACCOUNT_SID",
    "TWILIO_AUTH_TOKEN", 
    "TWILIO_FROM_NUMBER",
    "ALERT_TO_NUMBER"
]

for var in twilio_vars:
    value = os.getenv(var)
    if value:
        # Hide sensitive values
        if "TOKEN" in var or "SID" in var:
            display_value = value[:8] + "..." if len(value) > 8 else value
        else:
            display_value = value
        print(f"✅ {var}: {display_value}")
    else:
        print(f"❌ {var}: Not set")

print("\n📱 Twilio Configuration Status:")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_FROM_NUMBER")

if (account_sid and auth_token and from_number and 
    account_sid != "your_account_sid_here" and 
    auth_token != "your_auth_token_here" and
    from_number != "+1234567890"):
    print("✅ Twilio appears to be properly configured!")
else:
    print("⚠️  Twilio is using placeholder values - update .env file with real credentials")
    print("   The app will work fine without SMS functionality!")

print("\n🚀 Environment test complete!")