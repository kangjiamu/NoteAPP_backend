from django.contrib.auth.models import User
from django.db import models


class NoteCategory(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name
    
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notes')
    tags = models.ManyToManyField(
        Tag, related_name='notes', blank=True)  # 多对多关系

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    local_avatar_url = models.CharField(max_length=255, blank=True, null=True)
    remote_avatar_url = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

# 图片音频上传


class NoteAttachment(models.Model):
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    file_type = models.CharField(max_length=50)  # e.g., 'image', 'audio'



