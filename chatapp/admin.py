from django.contrib import admin
from .models import ChatRoom, ChatMessage

# Register your models here.


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(ChatRoom, ChatRoomAdmin)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'message', 'date')
    search_fields = ('user', 'room', 'message')
    list_filter = ('room', 'date')
admin.site.register(ChatMessage, ChatMessageAdmin)