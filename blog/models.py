from django.db import models
from django.conf import settings
# Create your models here.


# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import ContentType,GenericRelation


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def not_category(self):    
        return super().get_queryset().filter(status=3)

class PostQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=[Post.STATUS_PUBLISHED, Post.STATUS_ARCHIVED])

    def published(self):
        return self.filter(status=Post.STATUS_PUBLISHED)


class Post(models.Model):
    STATUS_DRAFT = 1
    STATUS_PUBLISHED = 2
    STATUS_ARCHIVED = 3
    STATUSES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_ARCHIVED, 'Archived'),
    )

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    snippet = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.SmallIntegerField(choices=STATUSES)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    posts = PostManager()
    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.title


class Inventory(models.Model):
    name = models.CharField(max_length=25)




class Room(models.Model):
    name = models.CharField(max_length=15)
    inventorys = models.ManyToManyField(Inventory,through='Kit', through_fields=('room','inventor'))
    notes = GenericRelation('Note')


class Kit(models.Model):
    inventor = models.ForeignKey(Inventory,on_delete=models.CASCADE,related_name='kits')
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    count = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.room.name


class Note(models.Model):
    text = models.TextField()
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey(ct_field='content_type',fk_field='object_id')




#
# class Group(models.Model):
#     title = models.CharField(max_length=45)
#
#
# class StudentStatus(models.Model):
#     status = models.CharField(max_length=15)
#     date = models.DateField()
#     # student_id = models.PositiveIntegerField(default=0)
#
#
#
# class Student(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
#     name = models.CharField('Ismi', max_length=25)
#     last_name = models.CharField('Familyasi', max_length=25)
#     brith = models.DateField('Tugulgan kuni')
#     adres = models.CharField('Manzili', max_length=355)
#     phone = models.CharField('Telefoni', max_length=16)
#
#
# class StudentData(models.Model):
#     student = models.ForeignKey(Student,on_delete=models.CASCADE)
#     group = models.ForeignKey(Group,on_delete=models.CASCADE)
#     year_month = models.DateField()
#     status = models.ManyToManyField(StudentStatus)
#     # date = models.DateField(auto_now_add=True)
#     # status = models.NullBooleanField()