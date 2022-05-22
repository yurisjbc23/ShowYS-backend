from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    code = models.AutoField(primary_key=True)
    user_author_code = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(blank=True, null=True, max_length=1000)
    location = models.CharField(blank=True, null=True, max_length=50)
    is_active = models.BooleanField(default = True)                                          
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'Post'

class Image(models.Model):
    code = models.AutoField(primary_key=True)
    post_code = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='posts', max_length=255, blank=False, null=False)                                          
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'Image'

class Hashtag(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, unique=True)                                        
    def __str__(self):
        return self.name
    class Meta:  
        db_table = 'Hashtag'

class PostHashtag(models.Model):
    code = models.AutoField(primary_key=True)
    post_code = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag_code = models.ForeignKey(Hashtag, on_delete=models.CASCADE)                                  
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'PostHashtag'

class Comment(models.Model):
    code = models.AutoField(primary_key=True)
    user_author_code = models.ForeignKey(User, on_delete=models.CASCADE)
    post_code = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.CharField(blank=False, null=False, max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)                               
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'Comment'


class Like(models.Model):
    code = models.AutoField(primary_key=True)
    user_author_code = models.ForeignKey(User, on_delete=models.CASCADE)
    post_code = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)                               
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'Like'

class Favorite(models.Model):
    code = models.AutoField(primary_key=True)
    user_author_code = models.ForeignKey(User, on_delete=models.CASCADE)
    post_code = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)                               
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'Favorite'


class Notification(models.Model):
    type_choices = [
        ('CO','Comment'),
        ('LI','Like'),
        ('FO','Follower'),
    ]
    code = models.AutoField(primary_key=True)
    user_author_code = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=type_choices)
    created_date = models.DateTimeField(auto_now_add=True)                               
    def __str__(self):
        return str(self.code)
    class Meta:  
        db_table = 'Notification'

