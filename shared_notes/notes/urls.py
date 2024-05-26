# notes/urls.py
from django.urls import path, include
from .views import register, login, create_note, list_notes, update_note, delete_note, list_notes_by_tag, upload_file, update_profile, auto_save, create_tag, update_tag, delete_tag

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('notes/create/', create_note, name='create_note'),
    path('notes/', list_notes, name='list_notes'),
    path('notes/<int:note_id>/', update_note, name='update_note'),
    path('notes/<int:note_id>/delete/', delete_note, name='delete_note'),
    path('tags/<str:tag_name>/notes/',
         list_notes_by_tag, name='list_notes_by_tag'),
    path('upload/', upload_file, name='upload_file'),
    path('profile/update/', update_profile, name='update_profile'),
    path('notes/<int:note_id>/autosave/', auto_save, name='auto_save'),
    path('tags/create/', create_tag, name='create_tag'),
    path('tags/<int:tag_id>/', update_tag, name='update_tag'),
    path('tags/<int:tag_id>/delete/', delete_tag, name='delete_tag'),
]
