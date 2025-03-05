from rest_framework.test import APITestCase
from django.urls import reverse
from ordem_cosmica_api.tests.test_base import  OrdemCosmicaAPIMixin
from unittest.mock import patch

class TestAPIArticle(APITestCase, OrdemCosmicaAPIMixin):
    def get_article_list_url(self):
        return reverse('ordem-cosmica-api:article-list')
    
    def get_article_detail_url(self, pk):
        return reverse('ordem-cosmica-api:article-detail', kwargs={'pk': pk})
    
    def get_get_response(self, url):
        return self.client.get(url)
    
    def get_post_response(self, url, data=None, access_token=None):
        if not access_token:
            return self.client.post(url, data=data)
        else:
            return self.client.post(
                url,
                data=data,
                HTTP_AUTHORIZATION=f'Bearer {access_token}'
            )
        
    def get_patch_response(self, url, data=None, access_token=None):
        if not access_token:
            return self.client.patch(url, data=data)
        else:
            return self.client.patch(
                url,
                data=data,
                HTTP_AUTHORIZATION=f'Bearer {access_token}'
            )
        
    def get_delete_response(self, url, access_token=None): 
        if not access_token:
            return self.client.delete(url)
        else:
            return self.client.delete(
                url,
                HTTP_AUTHORIZATION=f'Bearer {access_token}'
            )
    
    def test_article_list_returns_empty(self):
        response = self.get_get_response(self.get_article_list_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('count'), 0)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_article_list_returns_status_code_200(self):
        response = self.get_get_response(self.get_article_list_url())
        self.assertEqual(
            response.status_code, 200
        )

    @patch('ordem_cosmica_api.views.OrdemCosmicaAPIPagination.page_size', new=2)
    def test_article_list_returns_correct_pagination(self):
        self.make_article_in_batch(qtd=4)
        response_page1 = self.get_get_response(self.get_article_list_url())
        response_page2 = self.get_get_response(self.get_article_list_url() + '?page=2')
        # 4 articles were created
        self.assertEqual(
            response_page1.data.get('count'), 4
        )
        # 2 articles are shown, because of the pagination
        self.assertEqual(
            len(response_page1.data.get('results')),
            2
        )
        # 2 articles are shown, because of the pagination
        self.assertEqual(
            len(response_page2.data.get('results')),
            2
        )

    def test_user_must_send_jwt_to_post(self):
        response = self.get_post_response(self.get_article_list_url())
        self.assertEqual(
            response.status_code,
            401
        )

    def test_article_detail_return_status_200(self):
        article = self.make_article()
        response = self.get_get_response(self.get_article_detail_url(pk=article.pk))
        self.assertEqual(
            response.status_code,
            200
        )


    def test_user_must_send_jwt_to_post(self):
        response = self.get_post_response(self.get_article_list_url())
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )

    def test_user_must_send_jwt_to_delete(self):
        article = self.make_article()
        response = self.get_delete_response(self.get_article_detail_url(pk=article.pk))
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )

    def test_user_must_send_jwt_to_patch(self):
        article = self.make_article()
        response = self.get_patch_response(self.get_article_detail_url(pk=article.pk))
        self.assertEqual(
            response.status_code,
            401
        )
        self.assertEqual(
            response.data.get('detail'),
            "Authentication credentials were not provided."
        )

    