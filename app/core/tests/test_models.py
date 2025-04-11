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