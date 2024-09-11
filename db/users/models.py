from django.db import models


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'users'
