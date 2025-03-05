# from rest_framework.test import APITestCase
# from django.urls import reverse
# from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
# from unittest.mock import patch
# from django.core.files.uploadedfile import SimpleUploadedFile
# class TestAPIArticle(APITestCase, OrdemCosmicaAPIMixin):
#     def test_article_list_returns_empty(self):
#         response = self.get_get_response(self.get_article_list_url())
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data.get('count'), 0)
#         self.assertEqual(len(response.data.get('results')), 0)

#     def test_article_list_returns_status_code_200(self):
#         response = self.get_get_response(self.get_article_list_url())
#         self.assertEqual(
#             response.status_code, 200
#         )

#     @patch('ordem_cosmica_api.views.OrdemCosmicaAPIPagination.page_size', new=2)
#     def test_article_list_returns_correct_pagination(self):
#         self.make_article_in_batch(qtd=4)
#         response_page1 = self.get_get_response(self.get_article_list_url())
#         response_page2 = self.get_get_response(self.get_article_list_url() + '?page=2')
#         # 4 articles were created
#         self.assertEqual(
#             response_page1.data.get('count'), 4
#         )
#         # 2 articles are shown, because of the pagination
#         self.assertEqual(
#             len(response_page1.data.get('results')),
#             2
#         )
#         # 2 articles are shown, because of the pagination
#         self.assertEqual(
#             len(response_page2.data.get('results')),
#             2
#         )

#     def test_article_detail_return_status_200(self):
#         article = self.make_article()
#         response = self.get_get_response(self.get_article_detail_url(pk=article.pk))
#         self.assertEqual(
#             response.status_code,
#             200
#         )

#     def test_user_must_send_jwt_to_post(self):
#         response = self.get_post_response(self.get_article_list_url())
#         self.assertEqual(
#             response.status_code,
#             401
#         )
#         self.assertEqual(
#             response.data.get('detail'),
#             "Authentication credentials were not provided."
#         )

#     def test_user_must_send_jwt_to_delete(self):
#         article = self.make_article()
#         response = self.get_delete_response(self.get_article_detail_url(pk=article.pk))
#         self.assertEqual(
#             response.status_code,
#             401
#         )
#         self.assertEqual(
#             response.data.get('detail'),
#             "Authentication credentials were not provided."
#         )

#     def test_user_must_send_jwt_to_patch(self):
#         article = self.make_article()
#         response = self.get_patch_response(self.get_article_detail_url(pk=article.pk))
#         self.assertEqual(
#             response.status_code,
#             401
#         )
#         self.assertEqual(
#             response.data.get('detail'),
#             "Authentication credentials were not provided."
#         )

#     def test_user_can_post_with_correct_jwt_token(self):
#         user_data = {
#             'username':'test_user',
#             'password':'TestUser123'
#         }
#         user = self.make_author(username=user_data.get('username'), password=user_data.get('password'))
#         article_data = {
#             'title':'Um Título',
#             'description': 'Uma descrição',
#             'content':'Um conteúdo',
#             'user': user
#         }
#         access_token = self.get_user_token_pair(user_data=user_data).get('access_token')
#         response = self.get_post_response(self.get_article_list_url(),data=article_data,access_token=access_token)
#         self.assertEqual(
#             response.status_code,
#             201 #created 
#         )

#     def test_user_must_be_owner_to_delete(self):
#         user_data_not_owner = {
#             'username':'notonew',
#             'password':'NotOwnerUser123'
#         }
#         self.make_author(username=user_data_not_owner.get('username'), password=user_data_not_owner.get('password'))
#         access_token = self.get_user_token_pair(user_data=user_data_not_owner).get('access_token')
#         article = self.make_article()
#         response = self.get_delete_response(self.get_article_detail_url(pk=article.pk),access_token=access_token)
#         self.assertEqual(
#             response.status_code,
#             403
#         )
#         self.assertEqual(
#             response.data.get('detail'),
#             'You do not have permission to perform this action.'
#         )

#     def test_user_must_be_owner_to_patch(self):
#         user_data_not_owner = {
#             'username':'notonew',
#             'password':'NotOwnerUser123'
#         }
#         self.make_author(username=user_data_not_owner.get('username'), password=user_data_not_owner.get('password'))
#         access_token = self.get_user_token_pair(user_data=user_data_not_owner).get('access_token')
#         article = self.make_article()
#         patch_article_data = {
#             'title':'New Title'
#         }
#         response = self.get_patch_response(self.get_article_detail_url(pk=article.pk), data=patch_article_data,access_token=access_token)
#         self.assertEqual(
#             response.status_code,
#             403
#         )
#         self.assertEqual(
#             response.data.get('detail'),
#             'You do not have permission to perform this action.'
#         )

#     def test_user_owner_can_patch(self):
#         user_data_owner = {
#             'username':'notonew',
#             'password':'NotOwnerUser123'
#         }
#         article = self.make_article(author_data=user_data_owner, title='Old Title')
#         access_token = self.get_user_token_pair(user_data=user_data_owner).get('access_token')
#         patch_article_data = {
#             'title':'New Title'
#         }
#         response = self.get_patch_response(self.get_article_detail_url(pk=article.pk), data=patch_article_data,access_token=access_token)
#         self.assertEqual(
#             response.status_code,
#             200
#         )
#         self.assertEqual(
#             response.data.get('title'),
#             'New Title'
#         )

#     def test_user_owner_can_delete(self):
#         user_data_owner = {
#             'username':'notonew',
#             'password':'NotOwnerUser123'
#         }
#         article = self.make_article(author_data=user_data_owner)
#         access_token = self.get_user_token_pair(user_data=user_data_owner).get('access_token')
#         response = self.get_delete_response(self.get_article_detail_url(pk=article.pk), access_token=access_token)
#         self.assertEqual(
#             response.status_code,
#             204
#         )

#     def test_article_fields_are_required(self):
#         data = {}
#         self.make_author(username=self.default_user_data.get('username'), password=self.default_user_data.get('password'))
#         access_token = self.get_user_token_pair(user_data=self.default_user_data).get('access_token')
#         response = self.get_post_response(self.get_article_list_url(), data, access_token=access_token)
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('title', response.data)
#         self.assertIn('description', response.data)
#         self.assertIn('content', response.data)

#     def test_article_field_length_validation_on_post(self):
#         article_data = {
#             'title': 'A' * 61, 
#             'description': 'B' * 151, 
#             'content': 'Conteúdo válido'
#         }
#         self.make_author(username=self.default_user_data.get('username'), password=self.default_user_data.get('password'))
#         access_token = self.get_user_token_pair(user_data=self.default_user_data).get('access_token')
#         response = self.get_post_response(self.get_article_list_url(), data=article_data, access_token=access_token)

#         self.assertEqual(response.status_code, 400)
#         self.assertIn('title', response.data)
#         self.assertIn('description', response.data)

#     def test_article_field_length_validation_on_patch(self):
#         article_data = {
#             'title': 'A' * 61, 
#             'description': 'B' * 151, 
#         }
#         article = self.make_article(author_data=self.default_user_data)
#         access_token = self.get_user_token_pair(user_data=self.default_user_data).get('access_token')
#         response = self.get_patch_response(self.get_article_detail_url(pk=article.pk), data=article_data, access_token=access_token)
#         print(response.data)
#         self.assertEqual(response.status_code, 400)
#         self.assertIn('title', response.data)
#         self.assertIn('description', response.data)

    