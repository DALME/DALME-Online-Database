from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from dalme_app.models import (Attribute, Attribute_type, Attribute_DATE,
    Content_type, Source, Profile)

class UserManagementTestCase(TestCase):
    def setUp(self):
        password = make_password('testUserPassword')
        user = User.objects.create(
            username='test_user',
            first_name='Test',
            last_name='User',
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.profile.full_name = 'Test User'
        user.profile.dam_usergroup = 3
        user.profile.wiki_username = 'test_user'
        user.profile.wiki_groups = ['bureaucrat','administrator']
        user.profile.wp_role = 'administrator'
        user.save()

    def test_profile_properties(self):
        """
        Test basic user creation. Make sure the new user is associated with a
        profile, and that that profile doesn't have any userid fields from
        external databases
        """
        user = User.objects.get(username='test_user')
        # User has associated profile
        self.assertTrue(hasattr(user, 'profile'))
        # User has data assigned to profile
        self.assertEqual(user.profile.full_name,'Test User')
        # User does not have userids set
        self.assertEqual(user.profile.wp_userid, None)
        self.assertEqual(user.profile.wiki_userid, None)
        self.assertEqual(user.profile.dam_userid, None)

    def PullEmpty(self):
        """
        Tests the process of pulling a profile against what should be a
        database with no account for this user.
        """
        user = User.objects.get(username='test_user')
        # Make sure profile starts with empty userids
        self.assertEqual(user.profile.wp_userid, None)
        self.assertEqual(user.profile.wiki_userid, None)
        self.assertEqual(user.profile.dam_userid, None)
        # Run function to pull userids, which should not match
        user.profile.pull_ids()
        # Make sure profile still has no userids
        self.assertEqual(user.profile.wp_userid, None)
        self.assertEqual(user.profile.wiki_userid, None)
        self.assertEqual(user.profile.dam_userid, None)

    def CreateAccounts(self):
        """
        Tests the process of creating new accounts on remote databases
        """
        user = User.objects.get(username='test_user')
        self.assertEqual(user.profile.dam_usergroup,3)
        # Make sure we're starting from a blank slate
        self.assertEqual(user.profile.wp_userid, None)
        self.assertEqual(user.profile.wiki_userid, None)
        self.assertEqual(user.profile.dam_userid, None)
        # Run the function to create accounts
        user.profile.create_accounts()
        # Check that the ids are no longer empty
        self.assertNotEqual(user.profile.wp_userid, None)
        self.assertNotEqual(user.profile.wiki_userid, None)
        self.assertNotEqual(user.profile.dam_userid, None)

    def PushPermissions(self):
        """
        Tests function to push permissions to test account
        """
        user = User.objects.get(username='test_user')
        user.profile.push_permissions()

    def DeleteAccounts(self):
        """
        Cleans up created external accounts
        """
        user = User.objects.get(username='test_user')
        user.profile.delete_external_accounts()
        # Pull userids
        user.profile.pull_ids()
        # Make sure userids are now empty
        self.assertEqual(user.profile.wp_userid, None)
        self.assertEqual(user.profile.wiki_userid, None)
        self.assertEqual(user.profile.dam_userid, None)

    def test_users_CRUD(self):
        self.PullEmpty()
        self.CreateAccounts()
        self.PushPermissions()
        self.DeleteAccounts()

class BasicViewsTestCase(TestCase):
    def test_load_login_page(self):
        c = Client()
        response = c.get(reverse('dashboard'), follow=True)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Please Sign In")

class AttributeTestCase(TestCase):
    def setUp(self):
        testDate = Attribute_type.objects.create(
            name='Test date type',
            short_name='test_DATE',
            description='An attribute type to test DATE attribute data',
            data_type='DATE'
        )
        testContentType = Content_type.objects.create(
            content_class=1,
            name="Test content type",
            short_name='test',
            description='A content type to test functionality'
        )
        testSource = Source.objects.create(
            type=testContentType,
            name="Test Source",
            short_name="test_source"
        )
        testAttribute = Attribute.objects.create(
            attribute_type=testDate,
            content_id=testSource.pk
        )
        testAttributeDate = Attribute_DATE.objects.create(
            attribute_id=testAttribute,
            value="October 23, 2077",
            value_day=27,
            value_month=10,
            value_year=2077
        )

    def test_attribute_get_data(self):
        testSource = Source.objects.get(name="Test Source")
        self.assertEqual(testSource.get_attributes()[0].get_data().value, "October 23, 2077")
