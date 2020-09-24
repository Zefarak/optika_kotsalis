from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import reverse

from tinymce.models import HTMLField
from django.utils.text import slugify
# Create your models here.

def upload_product_photo(instance, filename):
    return f'bl0g/{instance.post.id}/{filename}'


class Category(models.Model):
    title = models.CharField(max_length=200)
    title_eng = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def get_update_url(self):
        return reverse('dashboard_blog:category_update_delete', kwargs={'pk': self.id, 'action': 'update'})

    def get_delete_url(self):
        return reverse('dashboard_blog:category_update_delete', kwargs={'pk': self.id, 'action': 'delete'})


class Tags(models.Model):
    title = models.CharField(max_length=200)
    title_eng = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def get_update_url(self):
        return reverse('dashboard_blog:validate_tag_edit_or_update', kwargs={'pk': self.id, 'action': 'update'})

    def get_delete_url(self):
        return reverse('dashboard_blog:validate_tag_edit_or_update', kwargs={'pk': self.id, 'action': 'update'})


class Post(models.Model):
    active = models.BooleanField(default=False, verbose_name='Κατασταση')
    is_featured = models.BooleanField(default=False, verbose_name='Pinned')
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, verbose_name='Τίτλος')
    title_eng = models.CharField(max_length=200, blank=True)
    text = HTMLField(verbose_name='Κείμενο')
    text_eng = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Κατηγορια')
    tags = models.ManyToManyField(Tags, blank=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True, max_length=240, db_index=True)

    def __str__(self):
        return self.title

    def image(self):
        qs = self.my_images.filter(main=True)
        return qs.first() if qs.exists() else False

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('dashboard_blog:post_update', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('dashboard_blog:post_delete', kwargs={'pk': self.id})


class PostImage(models.Model):
    main = models.BooleanField(default=True)
    image = models.ImageField(upload_to=upload_product_photo)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='my_images')

    def __str__(self):
        return f'{self.post} - {self.id}'

    def get_delete_url(self):
        return reverse('dashboard_blog:delete_image_view', kwargs={'pk': self.id})

    def get_validate_url(self):
        return reverse('dashboard_blog:validate_update_post_image', kwargs={'pk': self.id})


@receiver(post_save, sender=Post)
def create_slug_for_post(sender, instance, **kwargs):
    if not instance.slug:
        new_slug = slugify(instance.title, allow_unicode=True)
        qs_exists = Post.objects.filter(slug=new_slug).exists()
        instance.slug = f'{new_slug}-{instance.id}' if qs_exists else new_slug
        instance.save()
