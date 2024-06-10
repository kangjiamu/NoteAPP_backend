import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Note, NoteCategory, Tag


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = User.objects.create_user(username=username, password=password)
        user.profile.nickname = "New User"
        user.profile.bio = "This guy is too lazy to leave anything here."
        user.profile.avatar = 'default'
        user.profile.save()
        return JsonResponse({'message': 'User created successfully'})


@csrf_exempt
def login(request):
    from django.contrib.auth import authenticate
    from django.contrib.auth import login as auth_login
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            print("login success")
            return JsonResponse({'message': 'Logged in successfully'})
        else:
            print("login failed")
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        print("hihi")
        return HttpResponse('This endpoint only accepts POST requests.', status=405)


@login_required
@csrf_exempt
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
@csrf_exempt
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
@csrf_exempt
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'DELETE':
        note.delete()
        return JsonResponse({'message': 'Note deleted successfully'})

@login_required
@csrf_exempt
def list_notes_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name, user=request.user)
    notes = tag.notes.all().values('id', 'title', 'content', 'created_at', 'updated_at')
    return JsonResponse(list(notes), safe=False)






@login_required
@csrf_exempt
def upload_file(request):
    print(request.FILES)
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
@login_required
@csrf_exempt
def get_profile(request):
    if request.method == 'GET':
        profile = request.user.profile
        return JsonResponse({
            'nickname': profile.nickname,
            'bio': profile.bio,
            'avatar': profile.avatar.url if profile.avatar else '',
            'local_avatar_url': profile.local_avatar_url,
            'remote_avatar_url': profile.remote_avatar_url,
        })

@login_required
@csrf_exempt
def update_profile(request):
    data = json.loads(request.body)
    user = request.user
    profile = user.profile

    profile.nickname = data.get('nickname', profile.nickname)
    profile.bio = data.get('bio', profile.bio)
    profile.local_avatar_url = data.get('local_avatar_url', profile.local_avatar_url)

    if 'avatar' in data:
        if data['avatar']:
            profile.avatar = data['avatar']
            profile.remote_avatar_url = request.build_absolute_uri(profile.avatar.url)

    if 'password' in data:
        if data['password']:
            user.set_password(data['password'])
            user.save()

    profile.save()
    return JsonResponse({'message': 'Profile updated successfully'})

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import ProfileSerializer


class ProfileUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        profile_data = request.data
        profile_instance = get_object_or_404(UserProfile, id=profile_data['id'])

        local_avatar_url = profile_data.get('local_avatar_url')
        if 'avatar' in request.FILES:
            profile_instance.avatar = request.FILES['avatar']
            profile_instance.remote_avatar_url = request.build_absolute_uri(profile_instance.avatar.url)

        profile_instance.local_avatar_url = local_avatar_url if local_avatar_url else profile_instance.local_avatar_url

        serializer = ProfileSerializer(instance=profile_instance, data=profile_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)