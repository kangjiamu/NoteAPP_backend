from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Note, NoteCategory, Tag
from django.contrib.auth.models import User
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile



@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'User created successfully'})


@csrf_exempt
def login(request):
    from django.contrib.auth import authenticate, login as auth_login
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': 'Logged in successfully'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)


@login_required
def create_note(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        content = data['content']
        tags = data.get('tags', [])  # 获取标签列表
        note = Note.objects.create(
            title=title, content=content, user=request.user)
        for tag_name in tags:
            # 如果标签不存在，则创建
            tag, created = Tag.objects.get_or_create(
                name=tag_name, user=request.user)
            note.tags.add(tag)
        return JsonResponse({'message': 'Note created successfully', 'note_id': note.id})


@login_required
def list_notes(request):
    notes = request.user.notes.all().values(
        'id', 'title', 'content', 'created_at', 'updated_at')
    return JsonResponse(list(notes), safe=False)

@login_required
def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        tags = data.get('tags', [])
        note.tags.clear()
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(
                name=tag_name, user=request.user)
            note.tags.add(tag)
        note.save()
        return JsonResponse({'message': 'Note updated successfully'})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'DELETE':
        note.delete()
        return JsonResponse({'message': 'Note deleted successfully'})

@login_required
def list_notes_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name, user=request.user)
    notes = tag.notes.all().values('id', 'title', 'content', 'created_at', 'updated_at')
    return JsonResponse(list(notes), safe=False)

@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        profile = user.profile
        profile.nickname = data.get('nickname', profile.nickname)
        profile.bio = data.get('bio', profile.bio)
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        return JsonResponse({'message': 'Profile updated successfully'})




@login_required
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({'file_url': file_url})
    return JsonResponse({'error': 'File upload failed'}, status=400)

@login_required
@csrf_exempt
def auto_save(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        note.content = data.get('content', note.content)
        note.save()
        return JsonResponse({'message': 'Note auto-saved successfully'})


@login_required
@csrf_exempt
def create_tag(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tag_name = data['name']
        tag, created = Tag.objects.get_or_create(
            name=tag_name, user=request.user)
        return JsonResponse({'message': 'Tag created successfully', 'tag_id': tag.id})


@login_required
@csrf_exempt
def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    if request.method == 'PUT':
        data = json.loads(request.body)
        tag.name = data.get('name', tag.name)
        tag.save()
        return JsonResponse({'message': 'Tag updated successfully'})


@login_required
@csrf_exempt
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    if request.method == 'DELETE':
        tag.delete()
        return JsonResponse({'message': 'Tag deleted successfully'})
