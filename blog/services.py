import random
from blog.models import Post


def get_random_posts():
    posts = list(Post.objects.all())

    if len(posts) > 3:
        posts = random.sample(posts, k=3)

    return posts
