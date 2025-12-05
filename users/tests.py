from django.test import TestCase

from .models import CustomUser

# Create your tests here.
# You can add tests for your CustomUser model and any other functionality here.
class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))