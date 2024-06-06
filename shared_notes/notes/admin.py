from django.contrib import admin
from .models import Note, NoteCategory, Tag, UserProfile, NoteAttachment
# Register your models here.


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at',
                    'updated_at', 'display_tags')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    raw_id_fields = ('user',)

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    raw_id_fields = ('user',)
