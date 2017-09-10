from django.db import models

from django.core.urlresolvers import reverse

# Create your models here.
# model view controller - MVC

STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)



class posts(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, auto_created= True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
       # return "posts/%s" %self.id
        return reverse("posts:retrieve", kwargs={'id':self.id})
