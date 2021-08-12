from django.db import models

class Product(models.Model):
    pr_id = models.AutoField(primary_key=True, db_column='pr_id')
    pr_title = models.CharField(max_length=200, db_column='pr_title', verbose_name='Title')
    pr_image = models.CharField(max_length=200, db_column='pr_image', verbose_name='Image')
    pr_likes = models.PositiveIntegerField(default=0, db_column='pr_likes', verbose_name='Likes')
    pr_catal = models.PositiveIntegerField(default=1, db_column='pr_catal')




