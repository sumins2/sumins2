from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')
    img = models.TextField()
    def __str__(self):
        return self.title

class comment(models.Model):
    post_that_i_wrote_a_comment = models.ForeignKey(post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')

    class Meta :
        ordering = ('-pk',)

   