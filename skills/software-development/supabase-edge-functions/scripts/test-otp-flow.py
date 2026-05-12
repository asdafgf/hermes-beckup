#!/usr/bin/env python3
"""
KiraLog OTP Flow Test
Simulates the entire OTP flow without needing Deno or Supabase.
Tests: rate limiting, OTP generation, mock SMS, OTP verification.

Run: python scripts/test-otp-flow.py
"""

import json
import unittest


class MockOtpService:
    """Simulates supabase/functions/auth/otp-request/index.ts + otp-verify/index.ts logic"""

    def __init__(self, node_env="development"):
        self.node_env = node_env
        self.rate_limit_map = {}
        self.generated_otps = {}

    def request_otp(self, phone_number):
        """Simulate OTP request endpoint"""
        if not phone_number or not isinstance(phone_number, str):
            return {"status": 400, "error": "phone_number is required"}

        now = 1000000  # fake timestamp
        limit = self.rate_limit_map.get(phone_number)
        if limit and limit["reset_time"] > now and limit["count"] >= 3:
            return {"status": 429, "error": "Too many OTP requests. Try again later."}

        otp = "123456" if self.node_env == "development" else str(100000 + hash(phone_number) % 900000)
        self.generated_otps[phone_number] = otp

        if limit and limit["reset_time"] > now:
            limit["count"] += 1
        else:
            self.rate_limit_map[phone_number] = {"count": 1, "reset_time": now + 3600000}

        sms_log = f"[MOCK SMS → {phone_number}]: KiraLog OTP Kodunuz: {otp}"
        return {"status": 200, "success": True, "message": "OTP sent successfully", "otp": otp, "log": sms_log}

    def verify_otp(self, phone_number, otp, user_type="tenant", full_name="Test User",
                   email="test@example.com", tc_id_hash="test_hash_123"):
        """Simulate OTP verify endpoint"""
        if not all([phone_number, otp, user_type, full_name, email, tc_id_hash]):
            return {"status": 400, "error": "All fields are required"}

        # explicit guard: dev accepts ONLY "123456", production passes through (no storage yet)
        if self.node_env == "development":
            if otp != "123456":
                return {"status": 401, "error": "Invalid or expired OTP"}

        user_id = f"user_{hash(phone_number) % 100000}"
        return {"status": 200, "success": True, "user_id": user_id, "message": "OTP verified successfully"}


class TestOtpFlow(unittest.TestCase):

    def setUp(self):
        self.service = MockOtpService(node_env="development")

    def test_01_otp_request_success(self):
        result = self.service.request_otp("+905551234567")
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["otp"], "123456")
        self.assertIn("MOCK SMS", result["log"])

    def test_02_otp_request_missing_phone(self):
        result = self.service.request_otp("")
        self.assertEqual(result["status"], 400)

    def test_03_rate_limiting(self):
        phone = "+905559999999"
        for i in range(3):
            self.assertEqual(self.service.request_otp(phone)["status"], 200)
        self.assertEqual(self.service.request_otp(phone)["status"], 429)

    def test_04_otp_verify_success(self):
        self.service.request_otp("+905551234567")
        result = self.service.verify_otp("+905551234567", "123456")
        self.assertEqual(result["status"], 200)
        self.assertIn("user_", result["user_id"])

    def test_05_otp_verify_wrong_otp_dev(self):
        """Dev mode: wrong OTP must be rejected — only "123456" is valid"""
        result = self.service.verify_otp("+905551234567", "999999")
        self.assertEqual(result["status"], 401)

    def test_06_production_mode_bypass(self):
        """Production: no OTP storage yet, passes through"""
        prod = MockOtpService(node_env="production")
        self.assertEqual(prod.request_otp("+905551234567")["status"], 200)
        self.assertEqual(prod.verify_otp("+905551234567", "999999")["status"], 200)

    def test_07_verify_missing_fields(self):
        result = self.service.verify_otp("", "123456", "", "", "", "")
        self.assertEqual(result["status"], 400)

    def test_08_multiple_users(self):
        phones = ["+90555111111", "+90555222222", "+90555333333"]
        for phone in phones:
            self.assertEqual(self.service.request_otp(phone)["status"], 200)
            self.assertEqual(self.service.verify_otp(phone, "123456")["status"], 200)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOtpFlow)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    exit(0 if result.wasSuccessful() else 1)
