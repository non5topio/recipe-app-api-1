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
'''
FAILED TEST: The test run failed due to an **IndentationError** in the `test_models.py` file. The method `test_create_user_without_email_raises_value_error` is incorrectly indented, likely due to inconsistent spacing or mixing of tabs and spaces.

**Recommended Fix:**  
Correct the indentation of the `test_create_user_without_email_raises_value_error` method to align with the other test methods (typically 4 spaces under the `ModelTests` class).

    def test_create_user_with_empty_password_does_not_set_password(self):
        email = 'test@example.com'
        password = ''
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertFalse(user.check_password(password))

'''
'''
FAILED TEST: The test run failed due to an **IndentationError** in the `test_models.py` file. The method `test_create_user_without_email_raises_value_error` is incorrectly indented, likely due to inconsistent spacing or mixing of tabs and spaces.

**Recommended Fix:**  
Correct the indentation of the `test_create_user_without_email_raises_value_error` method to align with the other test methods (typically 4 spaces under the `ModelTests` class).

    def test_create_superuser_sets_staff_and_superuser_flags(self):
        user = get_user_model().objects.create_superuser(email='admin@example.com', password='adminpass123')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

'''
'''
FAILED TEST: The test run failed due to an **IndentationError** in the `test_models.py` file. The test method `test_create_user_without_email_raises_value_error` has an unexpected indent, likely due to inconsistent or incorrect spacing.

**Recommended Fix:**  
Correct the indentation of the `test_create_user_without_email_raises_value_error` method to align with the other test methods in the class (typically 4 spaces).

    def test_create_user_email_strips_whitespace(self):
        email = ' test@example.com '
        user = get_user_model().objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, 'test@example.com')

'''
'''
FAILED TEST: The test `test_create_user_email_normalized` failed because the email normalization logic is not functioning as expected. The test expects the email `'Test@Example.Com'` to be normalized to `'test@example.com'`, but it is instead being normalized to `'Test@example.com'`.

**Recommended Fix:**
Ensure that the `normalize_email` method in `UserManager` fully lowercases the email address. By default, Django's `normalize_email` should handle this, but verify that no custom logic is interfering with the normalization process.

    def test_create_user_email_normalized(self):
        email = 'Test@Example.Com'
        user = get_user_model().objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, 'test@example.com')

'''

    def test_create_user_without_email_raises_value_error(self):
        with self.assertRaises(ValueError) as cm:
            get_user_model().objects.create_user(email=None, password='testpass123')
        self.assertEqual(str(cm.exception), 'User must have an email address')

