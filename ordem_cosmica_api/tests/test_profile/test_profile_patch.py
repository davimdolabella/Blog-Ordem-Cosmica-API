from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
from ordem_cosmica_api import models
class TestOrdemCosmicaAPIProfilePATCH(APITestCase, OrdemCosmicaAPIMixin):
    def test_user_must_send_jwt_to_patch_profile(self):
        profile = self.make_author()
        response = self.get_patch_response(self.get_profile_detail_url(pk=profile.pk))
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )
    def test_user_must_be_owner_to_patch_profile(self):
        user_data_not_owner = {
            'username':'test_user',
            'password':'TestUser123',
            'email':'emailteste@gmail.com'
        }
        self.make_author(username=user_data_not_owner.get('username'), password=user_data_not_owner.get('password'))
        access_token = self.get_user_token_pair(user_data=user_data_not_owner).get('access_token')
        profile = self.make_author()
        patch_profile_data = {
            'email':'newemail@gmail.com'
        }
        response = self.get_patch_response(self.get_profile_detail_url(pk=profile.pk), data=patch_profile_data,access_token=access_token)
        self.assertEqual(
            response.status_code,
            403
        )
        self.assertEqual(
            response.data.get('detail'),
            'You do not have permission to perform this action.'
        )

    def test_user_owner_can_patch_profile(self):
        user_data_owner = {
            'username':'test_user',
            'password':'TestUser123',
            'email':'emailteste@gmail.com'
        }
        profile = self.make_author(**user_data_owner)
        access_token = self.get_user_token_pair(user_data=user_data_owner).get('access_token')
        patch_profile_data = {
            'email':'newemail@gmail.com'
        }
        response = self.get_patch_response(self.get_profile_detail_url(pk=profile.pk), data=patch_profile_data,access_token=access_token)
        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            models.User.objects.get(username=response.data.get('user')).email,
            'newemail@gmail.com'
        )

    def test_user_cannot_patch_username_with_username_already_in_use(self):
        profile1_data = {
            'username':'Username1',
            'email':'user1@gmail.com',
            'password':'useR1'
        }
        profile2_data = {
            'username':'Username2',
            'email':'user2@gmail.com',
            'password':'useR2'
        }
        profile1 = self.make_author(**profile1_data)
        self.make_author(**profile2_data)
        access_token = self.get_user_token_pair(user_data=profile1_data).get('access_token')
        profile1_data_patch = {
            'username': 'Username2'
        }
        response = self.get_patch_response(self.get_profile_detail_url(profile1.pk), data=profile1_data_patch, access_token=access_token)
        self.assertEqual(
            response.status_code,
            400
        )
        self.assertIn(
            'This username is already in use.',
            response.data.get('username')
        )