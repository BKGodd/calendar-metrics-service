from django.test import TestCase
from .models import User
from django.utils import timezone
from django.urls import reverse


def create_model(id=1, name='test', email='test@gmail.com', created=timezone.now()):
    return User(id=id, name=name, email=email, created=created)


# Testing our model
class ModelTesting(TestCase):
    """Simple class to test the User model."""
    
    def test_user_model(self):
        user = create_model()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.name, 'test')


# Testing our view and URLs
class ViewTesting(TestCase):
    """Simple class to test the view."""

    def test_list_view(self):
        url = reverse("root")
        data = {'name': 'brandon', 'email': 'brandon@gmail.com', 'created': timezone.now()}
        # Send test data to database, then retrieve
        self.client.post(url, data=data)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], 'brandon')
        
