from django.db import models

# Create your models here.

class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100)
    heading0 = models.CharField(max_length = 100, default = "")
    contentHead0 = models.CharField(max_length = 2000, default = "")
    heading1 = models.CharField(max_length = 100, default = "")
    contentHead1 = models.CharField(max_length = 2000, default = "")
    heading2 = models.CharField(max_length = 100, default = "")
    contentHead2 = models.CharField(max_length = 2000, default = "")
    pub_date = models.DateField()
    pub_by = models.CharField(max_length = 26, default = "")
    thumbnail = models.ImageField(upload_to='blog/images', default='')

    def __str__(self):
        return self.title