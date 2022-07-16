from django.db import models

# Create your models here.
class user_login(models.Model):
    uname = models.CharField(max_length=100)
    passwd = models.CharField(max_length=25)
    u_type = models.CharField(max_length=10)

    def __str__(self):
        return self.uname

class user_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gender = models.CharField(max_length=25)
    dob = models.CharField(max_length=25)
    addr = models.CharField(max_length=500)
    pin = models.CharField(max_length=25)
    contact = models.CharField(max_length=25)
    email = models.CharField(max_length=250)
    status = models.CharField(max_length=25)

    def __str__(self):
        return self.fname


class user_search(models.Model):
    user_id = models.IntegerField()
    query = models.CharField(max_length=100)
    dt = models.CharField(max_length=25)
    tm = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

class book_details(models.Model):
    isbn = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    pub_year = models.CharField(max_length=25)
    publisher = models.CharField(max_length=500)
    urls = models.CharField(max_length=250)
    urlm = models.CharField(max_length=250)
    urll = models.CharField(max_length=250)
    file_path = models.CharField(max_length=250)
    status = models.CharField(max_length=25)
