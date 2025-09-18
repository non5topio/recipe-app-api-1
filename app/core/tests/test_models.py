from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user=get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser_without_email_raises_value_error(self):
        """S5 - Ensure create_superuser propagates missing‑email error."""
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_superuser(
                email=None,
                password="SuperNoEmail",
            )


    def test_create_user_without_email_raises_value_error(self):
        """S4 - Ensure create_user validates presence of email."""
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_user(
                email=None,
                password="NoEmailPass",
            )


    def test_create_superuser_without_email_raises(self):
        """S5 – superuser creation without email propagates ValueError."""
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_superuser(email=None, password="SuperNoEmail")


    def test_create_user_without_email_raises(self):
        """S4 – creating a user without email raises ValueError."""
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_user(email=None, password="NoEmailPass")


    def test_create_superuser_flags_and_email(self):
        """S3 – superuser creation sets flags and normalizes email."""
        email = "Admin@EXAMPLE.COM"
        password = "AdminPass!9"
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, "Admin@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(password))


    def test_create_user_with_extra_fields(self):
        """S2 – extra fields are saved correctly."""
        email = "extra@example.com"
        password = "Pass1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name="Jane Doe",
            is_active=False,
        )
        self.assertEqual(user.email, "extra@example.com")
        self.assertEqual(user.name, "Jane Doe")
        self.assertFalse(user.is_active)
        self.assertTrue(user.check_password(password))


    def test_user_email_is_normalized(self):
        """S1 – email normalization on user creation."""
        email = "Test@EXAMPLE.COM"
        password = "StrongPass!23"
        user = get_user_model().objects.create_user(email=email, password=password)
        # Local part should stay as provided, domain should be lower‑cased
        self.assertEqual(user.email, "Test@example.com")
        self.assertTrue(user.check_password(password))

