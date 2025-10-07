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
FAILED TEST: ## Test Failure Analysis

### Failure Reason
**Syntax Error: IndentationError** in `app/core/tests/test_models.py` at line 81

The test file has multiple syntax errors preventing it from being parsed:

1. **Line 24** (`test_create_user_with_empty_string_password`): Missing `email` parameter in `create_user()` call
2. **Line 27**: Incomplete triple-quote string comment block
3. **Line 81**: Indentation error due to malformed code above

### Recommended Fixes

**Fix the `test_create_user_with_empty_string_password` method (lines 20-28):**

```python
def test_create_user_with_empty_string_password(self):
    """Test creating a user with empty string password"""
    email = 'test@example.com'
    password = ''
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
    )
    self.assertEqual(user.email, email)
    self.assertFalse(user.check_password(''))
    self.assertFalse(user.check_password('anypassword'))
    self.assertFalse(user.has_usable_password())
```

**Key changes:**
- Add missing `email = 'test@example.com'` variable
- Add `email=email,` parameter to `create_user()`
- Remove incomplete triple-quote comment block
- Fix assertion logic (empty passwords should set unusable password)

    def test_create_user_with_empty_string_password(self):
        """Test creating a user with empty string password"""
        email = 'test@example.com'
        password = ''
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(''))
        self.assertFalse(user.check_password('anypassword'))
        self.assertTrue(user.has_usable_password())

'''
'''
FAILED TEST: ## Test Failure Analysis

### Failed Test
`test_create_user_with_empty_string_password` in `app/core/tests/test_models.py`

### Failure Reason
The test expects that when a user is created with an empty string password (`''`), calling `user.check_password('')` should return `False`. However, it's returning `True`.

**Root Cause:** Django's `set_password()` method, when given an empty string, creates a valid (but empty) password hash. This means `check_password('')` will return `True` because the empty string matches the hashed empty password.

### Recommended Fix

**Option 1: Fix the test expectation** (if empty passwords should be allowed)
```python
self.assertTrue(user.check_password(''))  # Change to assertTrue
```

**Option 2: Fix the model to reject empty passwords** (if empty passwords should not be allowed)
In `app/core/models.py`, modify `create_user`:
```python
def create_user(self, email, password=None, **extra_fields):
    """Create a new user"""
    if not email:
        raise ValueError('User must have an email address')
    if password == '':
        raise ValueError('Password cannot be empty')
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
```

**Recommendation:** Choose Option 2 to enforce password validation, as allowing empty string passwords is a security concern.

    def test_create_user_with_empty_string_password(self):
        """Test creating a user with empty string password"""
        email = 'test@example.com'
        password = ''
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertFalse(user.check_password(''))
        self.assertFalse(user.check_password('anypassword'))
        self.assertTrue(user.has_usable_password())

'''

    def test_create_user_with_duplicate_email(self):
        """Test creating a user with duplicate email raises IntegrityError"""
        email = 'test@example.com'
        get_user_model().objects.create_user(
            email=email,
            password='testpass123',
        )
        with self.assertRaises(Exception) as context:
            get_user_model().objects.create_user(
                email=email,
                password='testpass456',
            )
        self.assertTrue(
            'UNIQUE constraint' in str(context.exception) or
            'duplicate key' in str(context.exception).lower() or
            'already exists' in str(context.exception).lower()
        )


    def test_create_user_with_maximum_email_length(self):
        """Test creating a user with email at maximum allowed length"""
        email = 'a' * 243 + '@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(len(user.email), 255)
        self.assertTrue(user.check_password(password))


    def test_user_default_field_values(self):
        """Test that default values for user fields are correctly applied"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)


    def test_create_user_with_none_password(self):
        """Test creating a user with None password sets unusable password"""
        email = 'test@example.com'
        user = get_user_model().objects.create_user(
            email=email,
            password=None,
        )
        self.assertEqual(user.email, email)
        self.assertFalse(user.check_password(''))
        self.assertFalse(user.check_password('anypassword'))
        self.assertFalse(user.has_usable_password())


    def test_create_superuser_with_elevated_permissions(self):
        """Test creating a superuser with elevated permissions"""
        email = 'admin@example.com'
        password = 'adminpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


    def test_create_user_with_extra_fields(self):
        """Test creating a user with extra fields like name"""
        email = 'test@example.com'
        password = 'testpass123'
        name = 'Test User'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))


    def test_create_user_with_email_normalization(self):
        """Test email is normalized for new users"""
        email = 'Test@EXAMPLE.COM'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, 'Test@example.com')
        self.assertTrue(user.check_password(password))


    def test_create_user_without_email_raises_error(self):
        """Test creating a user without an email raises ValueError"""
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(
                email='',
                password='testpass123',
            )
        self.assertEqual(str(context.exception), 'User must have an email address')
        
        with self.assertRaises(ValueError) as context:
            get_user_model().objects.create_user(
                email=None,
                password='testpass123',
            )
        self.assertEqual(str(context.exception), 'User must have an email address')

