from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #a field type that allows one-to many relationship, otherwise, use OneToOneField or ManyToManyField
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'pages'

    def __str__(self): #good for debugging, prints you something when you print the object
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING) #we do not modify the User model directly as others may call on it, so we link it to another database 1-1
    #by default there are 5 attributes to the user model we are adding 2 here
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True) #the upload_to attribute is conjoined to the MEDIA_ROOT

    def __str__(self):
        return self.user.username