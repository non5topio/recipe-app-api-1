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

    def test_create_user_with_duplicate_email_raises_error(self):
        """Test creating a user with duplicate email address raises IntegrityError"""
        email = 'test@example.com'
        get_user_model().objects.create_user(
            email=email,
            password='pass123',
        )
        with self.assertRaises(Exception) as context:
            get_user_model().objects.create_user(
                email=email,
                password='pass456',
            )
        self.assertTrue('UNIQUE constraint' in str(context.exception) or 'duplicate key' in str(context.exception).lower())


    def test_create_superuser(self):
        """Test creating a superuser with correct permissions"""
        email = 'admin@example.com'
        password = 'adminpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(password))


    def test_create_user_with_extra_fields(self):
        """Test creating a user with extra fields (name)"""
        email = 'test@example.com'
        password = 'testpass123'
        name = 'John Doe'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """Test email normalization during user creation"""
        email = 'Test@EXAMPLE.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='testpass123',
        )
        self.assertEqual(user.email, 'Test@example.com')


    def test_create_user_with_none_email_raises_error(self):
        """Test creating a user with None as email raises ValueError"""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(
                email=None,
                password='testpass123',
            )
        self.assertEqual(str(context.exception), 'User must have an email address')


    def test_create_user_without_email_raises_error(self):
        """Test creating a user without an email address raises ValueError"""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(
                email='',
                password='testpass123',
            )
        self.assertEqual(str(context.exception), 'User must have an email address')

    def test_create_superuser_with_none_password(self):
        """Test creating a superuser with None password"""
        email = 'admin@example.com'
        password = None
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertFalse(user.has_usable_password())
        self.assertFalse(user.check_password('anypassword'))

# FAILED TEST:
# ## Test Failure Analysis
# 
# ### Failed Test
# `test_create_user_with_whitespace_only_email_raises_error`
# 
# ### Root Cause
# The test expects a `ValueError` to be raised when creating a user with a whitespace-only email (`'   '`), but the current implementation in `models.py` does not raise this error.
# 
# **Issue in `UserManager.create_user()`:**
# ```python
# if not email:
#     raise ValueError('User must have an email address')
# ```
# 
# The condition `if not email:` only catches `None`, `''` (empty string), but **NOT** whitespace-only strings like `'   '`, because a string with spaces is truthy in Python.
# 
# ### Recommended Fix
# 
# Update the validation in `app/core/models.py` to strip whitespace before checking:
# 
# ```python
# def create_user(self, email, password=None, **extra_fields):
#     """Create a new user"""
#     if not email or not email.strip():
#         raise ValueError('User must have an email address')
#     user = self.model(email=self.normalize_email(email), **extra_fields)
#     user.set_password(password)
#     user.save(using=self._db)
#     return user
# ```
# 
# This ensures that whitespace-only emails are properly rejected, making the test pass.

#     def test_create_user_with_whitespace_only_email_raises_error(self):
#         """Test creating a user with whitespace-only email raises ValueError"""
#         with self.assertRaises(ValueError) as context:
#             get_user_model().objects.create_user(
#                 email='   ',
#                 password='testpass123',
#             )
#         self.assertEqual(str(context.exception), 'User must have an email address')


    def test_create_user_with_empty_string_password(self):
        """Test creating a user with empty string password"""
        email = 'test@example.com'
        password = ''
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.has_usable_password())
        self.assertTrue(user.check_password(''))
        self.assertFalse(user.check_password('anyotherpassword'))


    def test_create_user_with_special_chars_email(self):
        """Test creating a user with email containing special characters and international domain"""
        email = 'test+filter@sub-domain.EXAMPLE.co.uk'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, 'test+filter@sub-domain.example.co.uk')
        self.assertTrue(user.check_password(password))


    def test_create_user_with_max_name_length(self):
        """Test creating a user with maximum allowed name length (255 characters)"""
        email = 'test@example.com'
        password = 'testpass123'
        name = 'A' * 255
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertEqual(len(user.name), 255)
        self.assertTrue(user.check_password(password))


    def test_create_user_with_max_email_length(self):
        """Test creating a user with maximum allowed email length (255 characters)"""
        email = 'a' * 243 + '@example.com'
        password = 'testpass123'
        self.assertEqual(len(email), 255)
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))
        self.assertEqual(len(user.email), 255)




    
