from django.test import TestCase
from ordem_cosmica_api.models import Article, Profile, User
from django.urls import reverse

class OrdemCosmicaAPIMixin:
    def make_author(
        self,
        username='username',
        password='123456',
        email='username@email.com',
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        return Profile.objects.create(
            user = user
        )

    default_user_data = {
        'username': 'DefaultUser',
        'password': 'DefaultPassword123',
        'email':'DefaultEmail@gmail.com'
    }
    
    
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
    
    def get_user_token_pair(self, user_data):
        response = self.client.post(
            reverse('ordem-cosmica-api:token_obtain_pair'),
            data=user_data
        )
        return {
            'access_token': response.data.get('access'),
            'refresh_token': response.data.get('refresh'),
            'response': response
        }
        
    def get_delete_response(self, url, access_token=None): 
        if not access_token:
            return self.client.delete(url)
        else:
            return self.client.delete(
                url,
                HTTP_AUTHORIZATION=f'Bearer {access_token}'
            )
        
    # article
    def get_article_list_url(self):
        return reverse('ordem-cosmica-api:article-list')
    
    def get_article_detail_url(self, pk):
        return reverse('ordem-cosmica-api:article-detail', kwargs={'pk': pk})

    def make_article(
        self,
        author_data=None,
        title='Article Title',
        description='Recipe Description',
        content='Article Content',
    ):
        if author_data is None:
            author_data = {}

        return Article.objects.create(
            author=self.make_author(**author_data),
            title=title,
            description=description,
            content=content
        )

    def make_article_in_batch(self, qtd=10):
        articles = []
        for i in range(qtd):
            kwargs = {
                'title': f'Article Title {i}',
                'author_data': {'username': f'u{i}'}
            }
            article = self.make_article(**kwargs)
            articles.append(article)
        return articles


class OrdemCosmicaAPITestBase(TestCase, OrdemCosmicaAPIMixin):
    def setUp(self) -> None:
        return super().setUp()
