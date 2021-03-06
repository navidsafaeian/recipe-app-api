from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    '''Setup function is run before every test: create a super user, 
    log him in and create a normal user'''
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='password123',
            name='Test User Full Name'
        )
    
    def test_users_listed(self):
        """Test that users are listed on the user page.
        We have to make changes to django admin to accomodate
        ou custom user model."""

        # These urls are listed in django admin docs (following in details)
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        # AssertContains checks if certain value is present in a dict.
        # Also checks if the http respose is OK (200)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """Test that the user edit page works"""

        # We have to include fieldssets to UserAdmin for this to work
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


'''Note for core_user_changelist: Reversing admin URLs.
Each ModelAdmin instance provides an set of named URLs:
{{ app_label }}_{{ model_name }}_changelist 
{{ app_label }}_{{ model_name }}_add
{{ app_label }}_{{ model_name }}_history, object_id
{{ app_label }}_{{ model_name }}_delete, object_id
The UserAdmin provides a named URL:
{{ app_label }}_{{ model_name }}'''

