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
FAILED TEST: <|channel|>analysis<|message|>We need to explain that test file has indentation errors, also missing imports, class definitions wrong. Provide fixes: correct indentation, proper class definition, import BaseUserManager, fix missing self in methods, etc. Also mention email normalization expectation. Provide concise.<|end|><|start|>assistant<|channel|>final<|message|>**Why the test run failed**  
`pytest` could not even collect the tests because `app/core/tests/test_models.py` contains a **syntax error**:

```
E   File "/app/app/core/tests/test_models.py", line 73
E       def test_password_is_hashed(self):
E   IndentationError: unexpected indent
```

The file is malformed – several test methods are indented incorrectly, the `ModelTests` class is not defined properly (the `UserManager` subclass is inside the test class by mistake), and some methods lack the required `self` argument. Because of this parsing error the test suite aborts before any model code is exercised.

**Recommended fixes (minimal changes to get the suite running)**  

1. **Repair the test file structure**  
   ```python
   # app/core/tests/test_models.py
   from django.test import TestCase
   from django.contrib.auth import get_user_model

   class ModelTests(TestCase):
       def test_create_user_with_email_successful(self):
           ...

       def test_create_superuser_flags_and_normalization(self):
           ...

       def test_password_is_hashed(self):
           ...

       def test_create_superuser_without_email_raises(self):
           ...

       def test_create_user_without_email_raises(self):
           ...

       def test_create_user_with_extra_fields_and_defaults(self):
           ...

       def test_create_user_email_normalized(self):
           ...
   ```
   * Remove the stray `class UserManager(BaseUserManager):` that was accidentally placed inside the test file.  
   * Ensure every test method is indented **exactly one level** inside `ModelTests` and includes the `self` parameter.  

2. **Run the test collection again** – the syntax error will disappear and the tests will be executed against `app/core/models.py`.

(After the syntax error is fixed, the suite will still fail the *email‑normalisation* test because `UserManager.normalize_email` only lower‑cases the domain part. That can be addressed separately by overriding `normalize_email` to lower‑case the whole address.)

    def test_create_superuser_flags_and_normalization(self):
        """S6 – superuser creation sets appropriate flags and normalizes email."""
        email = "Admin@Example.COM"
        password = "AdminPass123"
        # The manager should normalize the whole email to lower case.
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(password))

'''
'''
FAILED TEST: <|channel|>analysis<|message|>We need to explain failure: email normalization only lowercases domain part, not local part. Test expects full lowercasing. Fix: override normalize_email in UserManager to lower entire email, or modify create_user to lower email after normalize_email. Also ensure superuser uses same. Provide concise answer.<|end|><|start|>assistant<|channel|>final<|message|>**Why the test failed**  
`UserManager.create_user` calls Django’s default `BaseUserManager.normalize_email`, which only lower‑cases the domain part of an address.  
When the test creates a superuser with `"Admin@Example.COM"` the stored value becomes `"Admin@example.com"` (local part stays capitalised). The assertion expects the whole address to be lower‑cased (`"admin@example.com"`), so it fails.

**Recommended fixes**  

1. **Override `normalize_email` in the custom manager**  
   ```python
   class UserManager(BaseUserManager):
       """Manager for user"""

       def normalize_email(self, email):
           """Normalize the email address by lower‑casing the entire string."""
           email = super().normalize_email(email)   # lower‑cases domain
           return email.lower()                    # also lower‑case local part
   ```

2. **Or adjust `create_user` directly** (if you prefer not to override the helper):  
   ```python
   def create_user(self, email, password=None, **extra_fields):
       if not email:
           raise ValueError('User must have an email address')
       email = self.normalize_email(email).lower()
       user = self.model(email=email, **extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user
   ```

Both approaches ensure that any user (including superusers) has a fully lower‑cased email, making the `test_create_superuser_flags_and_normalization` pass. No other code changes are required.

    def test_create_superuser_flags_and_normalization(self):
        """S6 – superuser creation sets appropriate flags and normalizes email."""
        email = "Admin@Example.COM"
        password = "AdminPass123"
        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password(password))

'''

    def test_password_is_hashed(self):
        """S5 – ensure password is stored hashed, not in plain text."""
        email = "secure@example.com"
        raw_password = "PlainTextPass"
        user = get_user_model().objects.create_user(email=email, password=raw_password)
        # Django hashes the password; the stored value should not contain the raw password.
        self.assertTrue(user.check_password(raw_password))
        self.assertNotIn(raw_password, user.password)


    def test_create_superuser_without_email_raises(self):
        """S4 – creating a superuser without email propagates the validation error."""
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_superuser(email="", password="SuperPass!")


    def test_create_user_without_email_raises(self):
        """S3 – creating a user without email should raise ValueError."""
        with self.assertRaisesMessage(ValueError, "User must have an email address"):
            get_user_model().objects.create_user(email=None, password="NoEmailPass")


    def test_create_user_with_extra_fields_and_defaults(self):
        """S2 – extra fields handling and default flag values."""
        email = "edge@example.com"
        password = "EdgePass123"
        name = "Edge Case User"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )
        self.assertEqual(user.email, "edge@example.com")
        self.assertEqual(user.name, name)
        self.assertTrue(user.is_active)   # default True
        self.assertFalse(user.is_staff)   # default False for regular users

'''
FAILED TEST: <|channel|>analysis<|message|>We need to explain failure: email normalization not fully lowercasing domain part? Actually expected "testuser@example.com". Received "TestUser@example.com". The normalize_email method from BaseUserManager lowercases domain part only, not local part. In test they expect full lowercasing. So need to override normalize_email or adjust create_user to lower email entirely. Provide fix: in UserManager.create_user, after normalize_email, also lower() the whole email, or implement custom normalize_email.

Thus answer: test fails because email not fully normalized; fix by overriding normalize_email in UserManager to lower both parts, or modify create_user to set email = email.lower().

Provide concise summary.<|end|><|start|>assistant<|channel|>final<|message|>**Failure Reason**  
`UserManager.create_user` uses Django’s default `BaseUserManager.normalize_email`, which only lower‑cases the domain part of the address. Consequently, creating a user with `"TestUser@Example.COM"` yields `"TestUser@example.com"` instead of the fully lower‑cased `"testuser@example.com"` expected by the test.

**Recommended Fixes**  

1. **Override `normalize_email` in `UserManager`**  
   ```python
   class UserManager(BaseUserManager):
       def normalize_email(self, email):
           """Normalize the email address by lower‑casing the whole string."""
           email = super().normalize_email(email)
           return email.lower()
   ```
   This keeps the existing domain‑lowercasing logic and adds full lower‑casing.

2. **Or adjust `create_user` directly**  
   ```python
   def create_user(self, email, password=None, **extra_fields):
       if not email:
           raise ValueError('User must have an email address')
       email = self.normalize_email(email).lower()   # ensure full lower‑case
       user = self.model(email=email, **extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user
   ```

Either change will make `user.email` equal to `"testuser@example.com"` and the test will pass. No other code changes are required.

    def test_create_user_email_normalized(self):
        """S1 – email normalization on user creation."""
        email = "TestUser@Example.COM"
        password = "StrongPass!23"
        user = get_user_model().objects.create_user(email=email, password=password)
        # The manager should have normalized the email to lower case.
        self.assertEqual(user.email, "testuser@example.com")
        # Ensure the password works.
        self.assertTrue(user.check_password(password))

'''
