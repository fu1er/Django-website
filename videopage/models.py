from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    describe = models.TextField()
    followers = models.CharField(max_length=200)
    photo = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Videoinfo(models.Model):
    video_name = models.CharField(max_length = 200)
    video_view = models.CharField(max_length = 200)
    publish_date = models.CharField(max_length = 200)
    likes = models.CharField(max_length = 200)
    coins = models.CharField(max_length = 200)
    collects = models.CharField(max_length = 200)
    brief = models.CharField(max_length = 500)
    comment = models.CharField(max_length = 1000)
    url = models.CharField(max_length = 200)
    cover = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self):
        return self.video_name