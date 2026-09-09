import unittest
import time
from fastapi import HTTPException

from backend.auth import (
    hash_password, verify_password, create_access_token,
    decode_access_token, validate_email_format, extract_token_from_header
)
from backend.database import init_db, get_user_by_email
from backend.models import UserSignUpRequest, UserSignInRequest, UserRole
from backend.routes import sign_up, sign_in, get_current_user_profile

class TestAuthenticationSecurity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_email_validation(self):
        self.assertTrue(validate_email_format("citizen@gmail.com"))
        self.assertTrue(validate_email_format("rajesh.sharma@gov.in"))
        self.assertTrue(validate_email_format("officer.up@nic.in"))
        self.assertFalse(validate_email_format("not-an-email"))
        self.assertFalse(validate_email_format("user@"))
        self.assertFalse(validate_email_format("@gmail.com"))
        self.assertFalse(validate_email_format(""))

    def test_password_hashing_and_verification(self):
        password = "SecurePassword123!"
        h1, s1 = hash_password(password)
        h2, s2 = hash_password(password)

        # Unique salts per hash
        self.assertNotEqual(s1, s2)
        self.assertNotEqual(h1, h2)

        # Correct password verification
        self.assertTrue(verify_password(password, s1, h1))
        self.assertTrue(verify_password(password, s2, h2))

        # Incorrect password verification
        self.assertFalse(verify_password("WrongPassword456", s1, h1))
        self.assertFalse(verify_password("", s1, h1))

    def test_signed_token_creation_and_validation(self):
        user_id = "USR-TEST-001"
        email = "test.token@gmail.com"
        role = "CITIZEN_FARMER"

        token = create_access_token(user_id=user_id, email=email, role=role, expires_in_hours=2)
        self.assertIsInstance(token, str)
        self.assertEqual(len(token.split('.')), 3)

        payload = decode_access_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["sub"], user_id)
        self.assertEqual(payload["email"], email)
        self.assertEqual(payload["role"], role)

        # Tampered token should fail
        tampered_token = token[:-5] + "XXXXX"
        self.assertIsNone(decode_access_token(tampered_token))

        # Expired token should fail
        expired_token = create_access_token(user_id=user_id, email=email, role=role, expires_in_hours=-1)
        self.assertIsNone(decode_access_token(expired_token))

    def test_demo_accounts_seeded_and_sign_in(self):
        # Demo citizen account should be able to sign in
        req = UserSignInRequest(email="citizen@gmail.com", password="Bhoomi@2026")
        auth_res = sign_in(req)
        self.assertIsNotNone(auth_res.access_token)
        self.assertEqual(auth_res.user.email, "citizen@gmail.com")
        self.assertEqual(auth_res.user.role, UserRole.CITIZEN_FARMER)

        # Demo officer account
        officer_res = sign_in(UserSignInRequest(email="officer@gmail.com", password="Bhoomi@2026"))
        self.assertEqual(officer_res.user.role, UserRole.REVENUE_OFFICER)

    def test_user_signup_and_signin_flow(self):
        test_email = f"farmer_{int(time.time())}_{id(self)}@gmail.com"
        password = "FarmerSecret@2026"
        full_name = "Ramesh Chand Yadav"

        # 1. Sign Up
        signup_req = UserSignUpRequest(
            email=test_email,
            password=password,
            full_name=full_name,
            role=UserRole.CITIZEN_FARMER,
            phone="+91 98111 22334"
        )
        signup_res = sign_up(signup_req)
        self.assertIsNotNone(signup_res.access_token)
        self.assertEqual(signup_res.user.email, test_email)
        self.assertEqual(signup_res.user.full_name, full_name)

        # 2. Duplicate Signup Rejection
        with self.assertRaises(HTTPException) as cm:
            sign_up(signup_req)
        self.assertEqual(cm.exception.status_code, 400)
        self.assertIn("already exists", cm.exception.detail.lower())

        # 3. Sign In with valid credentials
        signin_res = sign_in(UserSignInRequest(email=test_email, password=password))
        self.assertIsNotNone(signin_res.access_token)
        self.assertEqual(signin_res.user.id, signup_res.user.id)

        # 4. Sign In with wrong password
        with self.assertRaises(HTTPException) as cm:
            sign_in(UserSignInRequest(email=test_email, password="WrongPassword999"))
        self.assertEqual(cm.exception.status_code, 401)

        # 5. Access profile via token payload
        token_payload = decode_access_token(signin_res.access_token)
        self.assertIsNotNone(token_payload)
        user_profile = get_current_user_profile(token_payload)
        self.assertEqual(user_profile.email, test_email)
        self.assertEqual(user_profile.full_name, full_name)

        # 6. Invalid email rejection on signup
        with self.assertRaises(HTTPException) as cm:
            sign_up(UserSignUpRequest(
                email="invalid-email-address",
                password="validPassword123",
                full_name="Invalid Test"
            ))
        self.assertEqual(cm.exception.status_code, 400)

if __name__ == "__main__":
    unittest.main()
