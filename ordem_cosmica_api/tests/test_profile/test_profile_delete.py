from rest_framework.test import APITestCase
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
class TestOrdemCosmicaAPIProfileDELETE(APITestCase, OrdemCosmicaAPIMixin):
    def test_user_must_send_jwt_to_delete_profile(self):
        profile = self.make_author()
        response = self.get_delete_response(self.get_profile_detail_url(pk=profile.pk))
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )

    def test_user_must_be_owner_to_delete_profile(self):
        user_data_not_owner = {
            'username':'test_user',
            'password':'TestUser123',
            'email':'emailteste@gmail.com'
        }
        self.make_author(username=user_data_not_owner.get('username'), password=user_data_not_owner.get('password'))
        access_token = self.get_user_token_pair(user_data=user_data_not_owner).get('access_token')
        profile = self.make_author()
        response = self.get_delete_response(self.get_profile_detail_url(pk=profile.pk),access_token=access_token)
        self.assertEqual(
            response.status_code,
            403
        )
        self.assertEqual(
            response.data.get('detail'),
            'You do not have permission to perform this action.'
        )

    def test_user_owner_can_delete_profile(self):
        user_data_owner = {
            'username':'notonew',
            'password':'NotOwnerUser123'
        }
        profile = self.make_author(**user_data_owner)
        access_token = self.get_user_token_pair(user_data=user_data_owner).get('access_token')
        response = self.get_delete_response(self.get_profile_detail_url(pk=profile.pk), access_token=access_token)
        self.assertEqual(
            response.status_code,
            204
        )
