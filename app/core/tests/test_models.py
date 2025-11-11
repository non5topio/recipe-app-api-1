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

    def test_user_default_field_values(self):
        """Test that user fields have correct default values"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


    def test_create_user_with_none_password(self):
        """Test creating a user with None password sets unusable password"""
        email = 'test@example.com'
        user = get_user_model().objects.create_user(
            email=email,
            password=None,
        )
        self.assertEqual(user.email, email)
        self.assertFalse(user.has_usable_password())
        self.assertFalse(user.check_password('anypassword'))


    
