from django.test import TestCase
from ordem_cosmica_api.models import Article, Profile, User, Comment
from django.urls import reverse

class OrdemCosmicaAPIMixin:
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

    def get_delete_response(self, url, access_token=None): 
        if not access_token:
            return self.client.delete(url)
        else:
            return self.client.delete(
                url,
                HTTP_AUTHORIZATION=f'Bearer {access_token}'
            )
    #token
    def get_token_pair_url(self):
        return reverse('ordem-cosmica-api:token_obtain_pair')
    def get_token_refresh_url(self):
        return reverse('ordem-cosmica-api:token_refresh')
    def get_token_verify_url(self):
        return reverse('ordem-cosmica-api:token_verify')
    def get_user_token_pair(self, user_data):
        response = self.client.post(
            self.get_token_pair_url(),
            data=user_data
        )
        return {
            'access_token': response.data.get('access'),
            'refresh_token': response.data.get('refresh'),
            'response': response
        }
    
    def get_user_new_access_token(self, refresh_token=""):
        response = self.client.post(
            self.get_token_refresh_url(),
            data={'refresh': f'{refresh_token}'}
        )
        return{
            'access_token': response.data.get('access'),
            'response': response
        }
        
    #profile
    def get_profile_list_url(self):
        return reverse('ordem-cosmica-api:profile-list')
    
    def get_profile_detail_url(self,pk):
        return reverse('ordem-cosmica-api:profile-detail', kwargs={'pk':pk})

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
    
    def make_author_in_batch(self, qtd=10):
        authors = []
        for i in range(qtd):
            author = self.make_author(username=f'u{i}')
            authors.append(author)
        return authors
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
        create_author = True,
    ):
        if author_data is None:
            author_data = {}

        return Article.objects.create(
            author=self.make_author(**author_data) if create_author else author_data,
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
    
    # comment
    def get_comment_list_url(self):
        return reverse('ordem-cosmica-api:comment-list')
    def get_comment_detail_url(self, pk):
        return reverse('ordem-cosmica-api:comment-detail', kwargs={'pk':pk})
    def make_comment(
        self,
        author_data=None,
        content='Comment content',
        article_data=None,
        create_author = True,
        create_article = True
    ):
        if author_data is None:
            author_data = {}
        
        if article_data is None:
            article_data = {'author_data':{'username':'article_user'}}

        return Comment.objects.create(
            author=self.make_author(**author_data) if create_author else author_data,
            content=content,
            article=self.make_article(**article_data) if create_article else article_data
        )
    def make_comment_in_batch(self, qtd=10):
        comments = []
        for i in range(qtd):
            kwargs = {
                'content': f'Content {i}',
                'author_data': {'username': f'u{i}'}
            }
            comment = self.make_comment(**kwargs, article_data={'author_data':{'username': f'u{i + qtd * 2}'}})
            comments.append(comment)
        return comments


class OrdemCosmicaAPITestBase(TestCase, OrdemCosmicaAPIMixin):
    def setUp(self) -> None:
        return super().setUp()
