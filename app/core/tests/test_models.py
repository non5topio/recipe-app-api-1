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

    def test_user_password_is_hashed(self):
        """
        S6: Ensure that passwords are stored using Django's hashing mechanism.
        """
        email = "secure@example.com"
        raw_password = "PlainTextPass!"
        user = get_user_model().objects.create_user(email=email, password=raw_password)
        # The raw password should not be stored directly
        self.assertNotEqual(user.password, raw_password)
        # Django's default hash starts with the algorithm name, e.g., 'pbkdf2_sha256$'
        self.assertTrue(user.password.startswith('pbkdf2_sha256$'))
        # The check_password method should validate the raw password correctly
        self.assertTrue(user.check_password(raw_password))


    def test_create_superuser_without_email_raises_error(self):
        """
        S5: Creating a superuser with a missing email should raise the same ValueError.
        """
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_superuser(email=None, password="superpass")


    def test_create_user_without_email_raises_error(self):
        """
        S4: Creating a user with an empty email should raise ValueError.
        """
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_user(email="", password="anypass")


    def test_user_creation_with_extra_fields(self):
        """
        S3: Pass extra fields (name) to create_user and ensure they are saved.
        """
        email = "extra@example.com"
        password = "extraPass!23"
        name = "Extra Field User"
        user = get_user_model().objects.create_user(email=email, password=password, name=name)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))


    def test_user_default_boolean_fields(self):
        """
        S2: Verify default values for is_active, is_staff and is_superuser on a normal user.
        """
        email = "regular@example.com"
        password = "pwd12345"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        # is_superuser comes from PermissionsMixin; default should be False
        self.assertFalse(user.is_superuser)


    def test_user_email_normalization(self):
        """
        S1: Email normalization should strip surrounding whitespace and lower‑case the domain part.
        """
        raw_email = "  TestUser@EXAMPLE.COM  "
        password = "somepassword123"
        user = get_user_model().objects.create_user(email=raw_email, password=password)
        # Expected: local part unchanged, domain lower‑cased, whitespace removed
        self.assertEqual(user.email, "TestUser@example.com")
        self.assertTrue(user.check_password(password))

