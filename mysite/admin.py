from django.contrib import admin
from .models import Post
class postadmin(admin.ModelAdmin):
     list_display = ["title","published_date","edited_date"]
     list_display_links=["edited_date"]
     list_filter=["published_date"]
     search_fields=["title","content"]
     #list_editable=["title"]
     class Meta:
         model=Post

admin.site.register(Post,postadmin)
