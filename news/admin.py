from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Ip, Key_word, News


class Key_wordAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    list_display_links = ('id','title')



# Apply summernote to all TextField in model.
class NewsAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    list_display = ('id', "title", 'Контент', "title_content", 'category', 'created_ad', 'is_published')
    list_display_links = ('id', "title", 'Контент', 'title_content', 'created_ad', 'category')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',"title")
    list_display_links = ('id',"title")


admin.site.register(Category,CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Ip)
admin.site.register(Key_word,Key_wordAdmin)