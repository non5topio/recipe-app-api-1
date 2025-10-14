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
FAILED TEST: The test run failed due to an **IndentationError** in the `test_models.py` file. Specifically, the method `test_create_user_without_email_raises_error` has an **unexpected indent**, likely due to inconsistent or incorrect spacing.

**Recommended Fix:**  
Correct the indentation of the `test_create_user_without_email_raises_error` method to align with the other test methods in the class (typically 4 spaces).

    def test_create_user_with_empty_name(self):
        user = get_user_model().objects.create_user(email='test@example.com', password='testpass123', name='')
        self.assertEqual(user.name, '')

'''
'''
FAILED TEST: The test run failed due to an **IndentationError** in the `test_models.py` file. The method `test_create_user_without_email_raises_error` is incorrectly indented, likely due to inconsistent spacing.

**Recommended Fix:**  
Correct the indentation of the `test_create_user_without_email_raises_error` method to align with the other test methods (typically 4 spaces).

    def test_create_user_with_max_length_email(self):
        email = 'a' * 254 + '@example.com'
        user = get_user_model().objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, email)

'''
'''
FAILED TEST: The test run failed due to an **IndentationError** in the test file `app/core/tests/test_models.py`. Specifically, the method `test_create_user_without_email_raises_error` has an **unexpected indent**, likely due to inconsistent or incorrect spacing.

**Recommended Fix:**  
Correct the indentation of the `test_create_user_without_email_raises_error` method to align with the other test methods in the class (typically 4 spaces).

    def test_create_superuser_with_staff_and_superuser_flags(self):
        user = get_user_model().objects.create_superuser(email='admin@example.com', password='adminpass123')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

'''
'''
FAILED TEST: The test `test_user_email_normalization` failed because the email normalization is not working as expected. The test expects the email to be normalized to lowercase (`test@example.com`), but the actual result is `Test@example.com`.

**Recommended Fix:**
Ensure that the `normalize_email` method in `UserManager` is correctly converting the email to lowercase. By default, Django's `BaseUserManager.normalize_email` already does this, but if it's overridden elsewhere, it should be verified and corrected.

    def test_user_email_normalization(self):
        email = 'Test@Example.Com'
        user = get_user_model().objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, 'test@example.com')

'''

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError) as cm:
            get_user_model().objects.create_user(email=None, password='testpass123')
        self.assertEqual(str(cm.exception), 'User must have an email address')

