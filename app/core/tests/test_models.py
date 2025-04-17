from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError


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

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.COM','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email,'test123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123') 

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_password_is_hashed(self):
        """Test that the user password is set and stored hashed."""
        email = 'hashed@example.com'
        plain_password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=plain_password,
        )
        # Retrieve the user again to ensure we get the stored value
        saved_user = get_user_model().objects.get(email=email)
        # Check the password attribute is not the plain text
        self.assertNotEqual(saved_user.password, plain_password)
        # Check it looks like a Django hashed password (starts with algorithm)
        self.assertTrue(saved_user.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')))
        # Also verify check_password still works
        self.assertTrue(saved_user.check_password(plain_password))


    def test_create_user_with_non_boolean_is_active_raises_error(self):
        """Test creating user with non-boolean is_active raises ValidationError."""
        email = 'nonbool@example.com'
        password = 'testpass123'
        with self.assertRaises(ValidationError):
            # Pass a string instead of a boolean for is_active
            user = get_user_model().objects.create_user(
                email=email,
                password=password,
                is_active='not-a-boolean'
            )
            # Validation might happen on full_clean called by save or explicitly
            user.full_clean()
            user.save() # Ensure save is attempted if full_clean doesn't raise


    def test_create_user_with_none_email_raises_error(self):
        """Test creating user with None email raises ValueError."""
        with self.assertRaisesRegex(ValueError, 'User must have an email address'):
            get_user_model().objects.create_user(email=None, password='test123')


    def test_create_superuser_missing_password_raises_error(self):
        """Test calling create_superuser without password raises TypeError."""
        with self.assertRaises(TypeError):
            # Call create_superuser missing the password argument
            get_user_model().objects.create_superuser(email='test@example.com')


    def test_email_normalization_with_whitespace(self):
        """Test email normalization strips leading/trailing whitespace."""
        email_with_space = "  test@example.com  "
        expected_email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email_with_space,
            password=password,
        )
        self.assertEqual(user.email, expected_email)



    # def test_create_user_with_custom_is_active_flag(self):
    #     """Test creating a user with custom is_active flag"""
    #     email = 'inactive@example.com'
    #     password = 'ValidPass123'
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #         is_active=False
    #     )
    #     self.assertEqual(user.email, email)
    #     self.assertTrue(user.check_password(password))
    #     self.assertFalse(user.is_active)
    #     self.assertFalse(user.is_staff)  # Verify default value for is_staff


    # def test_create_user_with_unicode_special_characters_in_name(self):
    #     """Test creating a user with a name containing Unicode and special characters"""
    #     email = 'unicode@example.com'
    #     password = 'ValidPass123'
    #     name = '测试用户@#€'
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #         name=name
    #     )
    #     self.assertEqual(user.name, name)
    #     self.assertTrue(user.check_password(password))


    # def test_create_users_with_duplicate_email(self):
    #     """Test that creating multiple users with the same email raises an IntegrityError"""
    #     email = 'duplicate@example.com'
    #     password1 = 'ValidPass123'
    #     name1 = 'User One'
    #     password2 = 'AnotherPass456'
    #     name2 = 'User Two'
        
    #     # Create first user
    #     user1 = get_user_model().objects.create_user(
    #         email=email,
    #         password=password1,
    #         name=name1
    #     )
    #     self.assertEqual(user1.email, email)
    #     self.assertTrue(user1.check_password(password1))
        
    #     # Attempt to create second user with the same email
    #     with self.assertRaises(IntegrityError):
    #         get_user_model().objects.create_user(
    #             email=email,
    #             password=password2,
    #             name=name2
    #         )


    # def test_create_user_with_empty_password(self):
    #     """Test creating a user with empty password"""
    #     email = 'test@example.com'
    #     password = None
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #     )
    #     self.assertEqual(user.email, email)
    #     self.assertFalse(user.has_usable_password())


    # def test_create_user_with_max_length_name(self):
    #     """Test creating a user with a name exactly 255 characters long"""
    #     email = 'test@example.com'
    #     password = 'ValidPass123'
    #     name = 'a' * 255
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #         name=name
    #     )
    #     self.assertEqual(user.name, name)
    #     self.assertEqual(len(user.name), 255)
    #     self.assertTrue(user.check_password(password))


    # def test_create_user_with_max_length_email(self):
    #     """Test creating a user with an email exactly 255 characters long"""
    #     email_local_part = 'a' * 243
    #     email = f"{email_local_part}@example.com"  # Total length = 243 + 12 = 255
    #     password = 'ValidPass123'
    #     name = 'Test User'
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #         name=name
    #     )
    #     self.assertEqual(user.email, email)
    #     self.assertTrue(user.check_password(password))
    #     self.assertEqual(user.name, name)

    # def test_create_user_default_flags(self):
    #     """Test default flags for a newly created standard user."""
    #     email = 'defaultflags@example.com'
    #     password = 'testpass123'
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #     )
    #     self.assertTrue(user.is_active)
    #     self.assertFalse(user.is_staff)
    #     self.assertFalse(user.is_superuser) # Also check superuser default


    # def test_create_user_invalid_email_raises_error(self):
    #     """Test creating user with an invalid email format raises ValidationError"""
    #     with self.assertRaises(ValidationError):
    #         user = get_user_model().objects.create_user(
    #             email='invalid-email',
    #             password='password123'
    #         )
    #         # EmailField validation happens during full_clean or save
    #         user.full_clean() # Explicitly call full_clean


    # def test_create_user_email_too_long_raises_error(self):
    #     """Test creating user with email > 255 chars raises ValidationError"""
    #     long_email = 'a' * 245 + '@example.com' # 245 + 1 + 7 + 3 = 256 chars
    #     self.assertTrue(len(long_email) > 255)
    #     with self.assertRaises(ValidationError):
    #          # Validation likely occurs during full_clean called by save() or model clean()
    #          user = get_user_model().objects.create_user(
    #              email=long_email,
    #              password='password123',
    #              name='Test Name'
    #          )
    #          user.full_clean() # Explicitly call full_clean to trigger validation


    # def test_create_superuser_with_none_password(self):
    #     """Test creating a superuser with None password"""
    #     email = 'super_none_pass@example.com'
    #     user = get_user_model().objects.create_superuser(
    #         email,
    #         None,
    #     )
    #     self.assertTrue(user.is_superuser)
    #     self.assertTrue(user.is_staff)
    #     self.assertFalse(user.has_usable_password())


    # def test_create_superuser_with_none_email_raises_error(self):
    #     """Test creating superuser with None email raises ValueError"""
    #     with self.assertRaisesRegex(ValueError, 'User must have an email address'):
    #         get_user_model().objects.create_superuser(email=None, password='test123')


    # def test_create_user_with_none_email_raises_error(self):
    #     """Test creating user with None email raises ValueError"""
    #     with self.assertRaisesRegex(ValueError, 'User must have an email address'):
    #         get_user_model().objects.create_user(email=None, password='test123')


    # def test_create_users_with_duplicate_email(self):
    #     """Test that creating multiple users with the same email raises an IntegrityError"""
    #     email = 'duplicate@example.com'
    #     password1 = 'ValidPass123'
    #     name1 = 'User One'
    #     password2 = 'AnotherPass456'
    #     name2 = 'User Two'
        
    #     # Create first user
    #     user1 = get_user_model().objects.create_user(
    #         email=email,
    #         password=password1,
    #         name=name1
    #     )
    #     self.assertEqual(user1.email, email)
    #     self.assertTrue(user1.check_password(password1))
        
    #     # Attempt to create second user with the same email
    #     with self.assertRaises(IntegrityError):
    #         get_user_model().objects.create_user(
    #             email=email,
    #             password=password2,
    #             name=name2
    #         )


    # def test_create_user_with_max_length_name(self):
    #     """Test creating a user with a name exactly 255 characters long"""
    #     email = 'test@example.com'
    #     password = 'ValidPass123'
    #     name = 'a' * 255
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #         name=name
    #     )
    #     self.assertEqual(user.name, name)
    #     self.assertEqual(len(user.name), 255)
    #     self.assertTrue(user.check_password(password))


    # def test_create_user_with_max_length_email(self):
    #     """Test creating a user with an email exactly 255 characters long"""
    #     email_local_part = 'a' * 243
    #     email = f"{email_local_part}@example.com"  # Total length = 243 + 12 = 255
    #     password = 'ValidPass123'
    #     name = 'Test User'
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #         name=name
    #     )
    #     self.assertEqual(user.email, email)
    #     self.assertTrue(user.check_password(password))
    #     self.assertEqual(user.name, name)

    # def test_create_user_with_unicode_special_characters_in_name(self):
    #     """Test creating a user with a name containing Unicode and special characters"""
    #     email = 'unicode@example.com'
    #     password = 'ValidPass123'
    #     name = '测试用户@#€'
    #     user = get_user_model().objects.create_user(
    #         email=email,
    #         password=password,
    #         name=name
    #     )
    #     self.assertEqual(user.name, name)
    #     self.assertTrue(user.check_password(password))



    # def test_create_user_without_name_raises_error(self):
    #     """Test creating a user without a name raises an IntegrityError or validation error"""
    #     email = 'test@example.com'
    #     password = 'ValidPass123'
    #     with self.assertRaises((IntegrityError, ValidationError)):
    #         get_user_model().objects.create_user(
    #             email=email,
    #             password=password,
    #             name=None
    #         )