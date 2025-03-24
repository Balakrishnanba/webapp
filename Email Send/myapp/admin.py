from django.contrib import admin
from .models import ImageUpload, SentEmail


admin.site.register(ImageUpload)
admin.site.register(SentEmail)

