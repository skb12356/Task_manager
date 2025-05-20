from django.contrib import admin

# Register your models here.
from .models import Company, Project, File, ChatMessage, Member

admin.site.register(Company)
admin.site.register(Project)
admin.site.register(File)
admin.site.register(ChatMessage)
admin.site.register(Member)
