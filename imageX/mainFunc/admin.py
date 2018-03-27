from django.contrib import admin
from .models import Tag,Member,Category,Photo

# Register your models here.
admin.site.register(Tag)
admin.site.register(Member)
admin.site.register(Category)
admin.site.register(Photo)
