from django.test import TestCase

from users.models import User


class UserTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            is_staff=True,
            is_superuser=True,
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
