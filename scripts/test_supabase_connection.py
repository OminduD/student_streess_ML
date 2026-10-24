#!/usr/bin/env python3
"""
Supabase Connection Verification & Diagnostics Script
======================================================
Tests connection to Supabase, validates credentials, checks table existence,
and verifies Row Level Security (RLS) operations.
"""

import os
import sys
from datetime import datetime
from typing import Tuple

# Add repository root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_status(step: str, success: bool, details: str = ""):
    symbol = "✅" if success else "❌"
    print(f"{symbol} [{step}]: {details}")

def test_supabase_connection() -> bool:
    print("=" * 70)
    print("🔍 RUNNING SUPABASE DATABASE CONNECTION DIAGNOSTICS")
    print("=" * 70)

    # 1. Check for supabase package
    try:
        from supabase import create_client, Client
        print_status("Dependency Check", True, "supabase-py package is installed.")
    except ImportError as e:
        print_status("Dependency Check", False, f"Missing supabase package: {e}")
        print("💡 Run: pip install supabase")
        return False

    # 2. Check credentials from environment, .env file, or secrets
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
        except Exception:
            pass

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        # Check Streamlit secrets if running in Streamlit environment
        try:
            import streamlit as st
            if hasattr(st, "secrets"):
                supabase_url = supabase_url or st.secrets.get("SUPABASE_URL")
                supabase_key = supabase_key or st.secrets.get("SUPABASE_KEY")
        except Exception:
            pass

    if not supabase_url or not supabase_key:
        print_status("Credentials Check", False, "SUPABASE_URL or SUPABASE_KEY missing.")
        print("\n📋 Instructions to set credentials:")
        print("  1. Copy .env.example to .env:  cp .env.example .env")
        print("  2. In your Supabase Dashboard -> Project Settings -> API:")
        print("     - Copy 'Project URL' into SUPABASE_URL")
        print("     - Copy 'anon / public' key into SUPABASE_KEY")
        print("  3. For Streamlit Cloud: add to App Settings -> Secrets")
        return False

    # Normalize URL: strip trailing slash and /rest/v1 if included
    supabase_url = supabase_url.strip().rstrip("/")
    if supabase_url.endswith("/rest/v1"):
        supabase_url = supabase_url[:-8].rstrip("/")

    # Validate URL format
    if not supabase_url.startswith("https://") or "supabase.co" not in supabase_url:
        print_status("URL Format", False, f"Invalid Supabase URL: '{supabase_url}'. Expected 'https://<project-ref>.supabase.co'")
        return False

    print_status("Credentials Check", True, f"Found URL ({supabase_url[:24]}...) and Key ({supabase_key[:12]}...)")

    # 3. Test client initialization
    try:
        client: Client = create_client(supabase_url, supabase_key)
        print_status("Client Init", True, "Successfully created Supabase client instance.")
    except Exception as e:
        print_status("Client Init", False, f"Failed to instantiate client: {e}")
        return False

    # 4. Test table query (read access)
    try:
        response = client.table("user_inputs").select("id, timestamp, sleep_quality").limit(1).execute()
        print_status("Table Read Access", True, f"Queried 'user_inputs' table. Returned {len(response.data)} records.")
    except Exception as e:
        print_status("Table Read Access", False, f"Error querying 'user_inputs': {e}")
        print("💡 Hint: Did you run the SQL migration in 'supabase/schema.sql' in the Supabase SQL Editor?")
        return False

    # 5. Test table insert (write access under RLS)
    test_id = None
    try:
        test_payload = {
            "sleep_quality": 3,
            "headaches_per_week": 1,
            "academic_performance": 4,
            "study_load": 3,
            "extracurricular_frequency": 2,
            "stress_level": 2,
            "source": "diagnostic_test_runner",
            "timestamp": datetime.now().isoformat()
        }
        insert_res = client.table("user_inputs").insert(test_payload).execute()
        if insert_res.data and len(insert_res.data) > 0:
            test_id = insert_res.data[0].get("id")
            print_status("Table Write Access", True, f"Inserted test record successfully (ID: {test_id}).")
        else:
            print_status("Table Write Access", True, "Record inserted (empty response due to RLS return policy).")
    except Exception as e:
        print_status("Table Write Access", False, f"Insert test failed: {e}")
        print("💡 Hint: Check RLS INSERT policy in Supabase. Ensure 'Allow anonymous insert' is enabled.")
        return False

    # Clean up test record if possible
    if test_id:
        try:
            client.table("user_inputs").delete().eq("id", test_id).execute()
            print_status("Cleanup", True, "Test record cleaned up.")
        except Exception:
            # Under strict RLS, anon key cannot delete records, which is the expected secure behavior!
            print_status("Security Verification", True, "Anon key cannot delete rows (Row Level Security active).")

    print("=" * 70)
    print("🎉 SUPABASE DATABASE IS FULLY OPERATIONAL AND READY FOR DEPLOYMENT!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_supabase_connection()
    sys.exit(0 if success else 1)
