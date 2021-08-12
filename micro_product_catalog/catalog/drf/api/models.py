from django.db import models

class Catalog(models.Model):
    ct_id = models.AutoField(primary_key=True, db_column='ct_id')
    ct_title = models.CharField(max_length=200, db_column='ct_title', verbose_name='Title')


class Product(models.Model):
    pr_id = models.AutoField(primary_key=True, db_column='pr_id')
    pr_catal = models.ForeignKey(Catalog, 
                        db_column='pr_catal',
                        on_delete=models.CASCADE, 
                        related_name='ct_products')
    pr_dt_add = models.DateTimeField(auto_now_add=True)
