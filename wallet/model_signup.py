from django.db import models

class userprofile(models.Model):
    name=models.CharField(max_length=100)
    website=models.CharField(max_length=200)
    email=models.EmailField()
    birth_date=models.DateField()
    sex=models.CharField(max_length=50)
    country=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    mailing=models.BooleanField()
    

    def __unicode__(self):
        return self.name
#admin.site.register(userprofile)
