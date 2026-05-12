#!/usr/bin/env python3
"""
OTP Flow Test Script — Supabase Edge Functions için

Simulates OTP request + verify flow without needing Deno/Supabase.
Tests: rate limiting, OTP generation, mock SMS, OTP verification, production mode.

Usage:
  python test_otp_flow.py
"""

import json
import unittest

class MockOtpService:
    """Simulates supabase/functions/auth/otp-request + otp-verify logic"""

    def __init__(self, node_env="development"):
        self.node_env = node_env
        self.rate_limit_map = {}
        self.generated_otps = {}

    def request_otp(self, phone_number):
        if not phone_number or not isinstance(phone_number, str):
            return {"status": 400, "error": "phone_number is required"}

        now = 1000000
        limit = self.rate_limit_map.get(phone_number)
        if limit and limit["reset_time"] > now and limit["count"] >= 3:
            return {"status": 429, "error": "Too many OTP requests. Try again later."}

        otp = "123456" if self.node_env == "development" else str(100000 + hash(phone_number) % 900000)
        self.generated_otps[phone_number] = otp

        if limit and limit["reset_time"] > now:
            limit["count"] += 1
        else:
            self.rate_limit_map[phone_number] = {"count": 1, "reset_time": now + 3600000}

        return {
            "status": 200, "success": True,
            "message": "OTP sent successfully",
            "otp": otp,
            "log": f"[MOCK SMS → {phone_number}]: KiraLog OTP Kodunuz: {otp}"
        }

    def verify_otp(self, phone_number, otp, user_type="tenant",
                   full_name="Test User", email="test@example.com", tc_id_hash="test_hash"):
        if not all([phone_number, otp, user_type, full_name, email, tc_id_hash]):
            return {"status": 400, "error": "All fields are required"}

        # Critical: correct OTP logic — only accept "123456" in dev mode
        is_dev = self.node_env == "development"
        is_valid_otp = otp == "123456" if is_dev else True  # prod: no storage yet

        if not is_valid_otp:
            return {"status": 401, "error": "Invalid or expired OTP"}

        user_id = f"user_{hash(phone_number) % 100000}"
        return {"status": 200, "success": True, "user_id": user_id, "message": "OTP verified successfully"}


class TestOtpFlow(unittest.TestCase):

    def setUp(self):
        self.service = MockOtpService(node_env="development")

    def test_01_request_success(self):
        r = self.service.request_otp("+905551234567")
        self.assertEqual(r["status"], 200)
        self.assertEqual(r["otp"], "123456")

    def test_02_request_missing_phone(self):
        r = self.service.request_otp("")
        self.assertEqual(r["status"], 400)

    def test_03_rate_limiting(self):
        phone = "+905559999999"
        for i in range(3):
            self.assertEqual(self.service.request_otp(phone)["status"], 200)
        r = self.service.request_otp(phone)
        self.assertEqual(r["status"], 429)

    def test_04_verify_success(self):
        r = self.service.verify_otp("+905551234567", "123456")
        self.assertEqual(r["status"], 200)
        self.assertIn("user_", r["user_id"])

    def test_05_verify_wrong_otp(self):
        r = self.service.verify_otp("+905551234567", "999999")
        self.assertEqual(r["status"], 401)
        self.assertIn("Invalid", r["error"])

    def test_06_production_bypass(self):
        prod = MockOtpService(node_env="production")
        r = prod.verify_otp("+905551234567", "any_otp")
        self.assertEqual(r["status"], 200)

    def test_07_missing_fields(self):
        r = self.service.verify_otp("", "123456", "", "", "", "")
        self.assertEqual(r["status"], 400)

    def test_08_multiple_users(self):
        for phone in ["+90555111111", "+90555222222", "+90555333333"]:
            r1 = self.service.request_otp(phone)
            self.assertEqual(r1["status"], 200)
            r2 = self.service.verify_otp(phone, "123456")
            self.assertEqual(r2["status"], 200)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOtpFlow)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'='*50}")
    print(f"Tests: {result.testsRun}, Failures: {len(result.failures)}, Errors: {len(result.errors)}")
    print("PASS" if result.wasSuccessful() else "FAIL")
