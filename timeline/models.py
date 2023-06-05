from django.db import models
from accounts.models import User

class Post(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.PROTECT,to_field='UserID',related_name='timeline_userid')
    name = models.ForeignKey(User, on_delete=models.PROTECT,to_field='name',related_name='timeline_posts',unique=True)
    parent_post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    context = models.CharField(max_length=512)
    created_at = models.DateField(auto_now=False)
    
    def __str__(self):
        return self.title
    

    
# Create your models here.
