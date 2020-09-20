from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import reverse

from tinymce.models import HTMLField
from django.utils.text import slugify
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200)
    title_eng = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=200)
    title_eng = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    title_eng = models.CharField(max_length=200, blank=True)
    text = HTMLField()
    text_eng = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, max_length=240, db_index=True)

    def __str__(self):
        return self.title

    def image(self):
        qs = self.my_images.filter(main=True)
        return qs.first() if qs.exists() else False

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class PostImage(models.Model):
    main = models.BooleanField(default=True)
    image = models.ImageField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='my_images')

    def save(self, *args, **kwargs):
        if self.main:
            self.post.my_images.all().exclude(id=self.id).update(main=False) if self.post.my_images.all().exists() else ''
        self.save(*args, **kwargs)

    def __str__(self):
        return f'{self.post} - {self.id}'


@receiver(post_save, sender=Post)
def create_slug_for_post(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = Post.objects.filter(slug=new_slug).exists()
        instance.slug = f'{new_slug}-{instance.id}' if qs_exists else new_slug
        instance.save()
    if not instance.eng_title:
        instance.eng_title = instance.title
        instance.save()