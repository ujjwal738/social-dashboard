import facebook
from django.conf import settings

def fetch_facebook_posts():
    graph = facebook.GraphAPI(access_token=settings.FACEBOOK_USER_ACCESS_TOKEN, version="3.1")
    posts = graph.get_connections(id='me', connection_name='posts')
    return posts.get('data', [])
