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


    def test_create_superuser(self):
        """Test creating a superuser with staff and superuser permissions"""
        email = 'admin@example.com'
        password = 'adminpass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(password))


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
        """Test that email is normalized when creating a user"""
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
# FAILED TEST: ## Test Failure Analysis

### Failure Reason
**Syntax Error** preventing test file from being parsed and executed.

### Root Cause
Line 110 in `test_models.py` contains invalid Python syntax - markdown-formatted text that cannot be parsed as Python code:
```
**Syntax Error** in the test file preventing test collection and execution.
```

This appears to be documentation/analysis text that was accidentally pasted into the Python source file.

### Issues Found
1. **Line 110**: Markdown text (`**Syntax Error**...`) is not valid Python syntax
2. **Line 3**: Backtick-wrapped text `\`test_create_user_with_whitespace_email_raises_error\`` is also invalid Python syntax
3. Multiple test methods are incomplete (missing required arguments for `create_user()` calls)

### Recommended Fixes
1. **Remove lines 110 onwards** - delete all the markdown/documentation text that was accidentally included in the Python file
2. **Remove or fix line 3** - delete the backtick-wrapped text
3. **Complete all test methods** by adding missing variable definitions and required arguments:
   - Add `email` and `password` parameters where missing
   - Ensure all `create_user()` and `create_superuser()` calls have required arguments
4. **Uncomment and properly implement** the whitespace email test if needed, or remove the commented block entirely

#     def test_create_superuser_preserves_is_active_default(self):
#         """Test creating a superuser preserves is_active default value"""
#         email = 'superadmin@example.com'
#         password = 'superpass123'
#         user = get_user_model().objects.create_superuser(
#             email=email,
#             password=password,
#         )
#         self.assertEqual(user.email, email)
#         self.assertTrue(user.is_staff)
#         self.assertTrue(user.is_superuser)
#         self.assertTrue(user.is_active)
#         self.assertTrue(user.check_password(password))

# FAILED TEST: ## Test Failure Analysis

### Failure Reason
**Syntax Error** in the test file preventing test collection and execution.

### Root Cause
Line 105 in `test_models.py` contains invalid Python syntax:
```python
`test_create_user_with_whitespace_email_raises_error`
```

This appears to be a markdown-formatted test name (using backticks) that was accidentally left in the Python code, likely from documentation or comments.

### Issues Found
1. **Line 105**: Backtick-wrapped text is not valid Python syntax
2. **Multiple incomplete test methods**: Several tests are missing required arguments:
   - `test_user_default_field_values` - missing `email` and `password` in `create_user()`
   - `test_create_user_with_none_password` - missing `email` variable definition
   - `test_create_superuser` - missing `email` and `password` in `create_superuser()`
   - `test_create_user_with_extra_fields` - missing `email` and `password` variables
   - `test_create_user_with_email_normalization` - missing `password` in `create_user()`
   - `test_create_user_with_none_email_raises_error` - missing `password` in `create_user()`
   - `test_create_user_with_empty_string_password` - missing `email` variable definition
   - `test_create_user_with_max_name_length` - missing `email` and `password` in `create_user()`
   - `test_create_user_with_max_email_length` - missing `password` in `create_user()`

### Recommended Fixes
1. **Remove line 105** entirely (the backtick-wrapped text)
2. **Complete all test methods** by adding missing variable definitions and required arguments to `create_user()` calls
3. If the whitespace email test is needed, uncomment it properly (it's currently in a comment block)

#     def test_create_user_with_none_email_raises_error(self):
#         """Test creating a user with None as email raises ValueError"""
#         with self.assertRaises(ValueError) as context:
#             get_user_model().objects.create_user(
#                 email=None,
#                 password='testpass123',
#             )
#         self.assertEqual(str(context.exception), 'User must have an email address')

# FAILED TEST: ## Test Failure Analysis

### Failed Test
`test_create_user_with_whitespace_email_raises_error`

### Root Cause
The test expects a `ValueError` to be raised when creating a user with a whitespace-only email (`'   '`), but the current implementation in `models.py` only checks if the email is falsy (`if not email`). A whitespace-only string is truthy in Python, so it passes the validation check and no error is raised.

### Issue in Code
In `app/core/models.py`, the `create_user` method:
```python
if not email:
    raise ValueError('User must have an email address')
```

This check only catches empty strings (`''`) and `None`, but not whitespace-only strings like `'   '`.

### Recommended Fix
Update the validation in `UserManager.create_user()` to strip whitespace before checking:

```python
def create_user(self, email, password=None, **extra_fields):
    """Create a new user"""
    if not email or not email.strip():
        raise ValueError('User must have an email address')
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
```

This will ensure that whitespace-only emails are properly rejected.

#     def test_create_user_with_whitespace_email_raises_error(self):
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
        self.assertFalse(user.check_password('anypassword'))


    def test_create_user_with_max_name_length(self):
        """Test creating a user with maximum allowed name length (255 characters)"""
        email = 'test@example.com'
        password = 'testpass123'
        name = 'a' * 255
        self.assertEqual(len(name), 255)
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
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


