from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify #supaya bisa pake spasi di url
# from accounts.models import User

import misaka #supaya bisa ngebuat link

from django.contrib.auth import get_user_model
User = get_user_model() #call model(data) for this user

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library() #use custom template tags



class Group(models.Model): #database untuk group (informasi dari tiap group)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User,through="GroupMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("groups:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class GroupMember(models.Model):#database untuk anggota tiap group
    group = models.ForeignKey(Group, related_name="memberships")
    user = models.ForeignKey(User,related_name='user_groups')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("group", "user")
