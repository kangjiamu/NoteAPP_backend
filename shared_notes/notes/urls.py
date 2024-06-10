# notes/urls.py
from django.urls import include, path

from .views import (ProfileUpdateView, auto_save, create_note, create_tag,
                    delete_note, delete_tag, get_profile, list_notes,
                    list_notes_by_tag, login, register, update_note,
                    update_profile, update_tag, upload_file)

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
    path('update_profile/', update_profile, name='update_profile'),
    path('get_profile/', get_profile, name='get_profile'),

    path('notes/<int:note_id>/autosave/', auto_save, name='auto_save'),
    # path('tags/create/', create_tag, name='create_tag'),
    path('notes/<int:note_id>/tags/create/', create_tag, name='create_tag'),
    path('tags/<int:tag_id>/', update_tag, name='update_tag'),
    path('tags/<int:tag_id>/delete/', delete_tag, name='delete_tag'),
    path('update_profile/', ProfileUpdateView.as_view(), name='update_profile'),
]
