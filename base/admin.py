from django.contrib import admin

from base.models import Page, Content, PageContent


class PageContentInline(admin.TabularInline):
    model = PageContent
    extra = 1


class PageAdmin(admin.ModelAdmin):
    # https://code.djangoproject.com/ticket/6933
    search_fields = (
        '^title',
    )
    inlines = (PageContentInline,)

    list_display = (
        'id',
        'title',
        'created_at',
        'modified_at',
    )


class ContentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content_type',
        'title',
        'counter',
        'get_text_display',
        'video',
        'video_subtitles',
        'audio',
        'audio_bitrate',
        'created_at',
        'modified_at',
    )

    @staticmethod
    def get_text_display(obj):
        text = obj.text
        if len(text) > 100:
            text = f"{text[:100]}..."
        return text


admin.site.register(Page, PageAdmin)
admin.site.register(Content, ContentAdmin)
