from django.db import models


class Page(models.Model):
    title = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title


class ContentType(object):
    AUDIO = 1
    VIDEO = 2
    TEXT = 3


CONTENT_TYPE_CHOICES = (
    (ContentType.AUDIO, 'Audio'),
    (ContentType.VIDEO, 'Video'),
    (ContentType.TEXT, 'Text'),
)


class Content(models.Model):
    title = models.CharField(max_length=200)
    counter = models.PositiveIntegerField(default=0)

    content_type = models.PositiveSmallIntegerField(choices=CONTENT_TYPE_CHOICES)

    audio = models.FileField(upload_to='audio/', null=True, blank=True)
    audio_bitrate = models.PositiveIntegerField(null=True, blank=True)

    text = models.TextField(blank=True)

    video = models.FileField(upload_to='video/', null=True, blank=True)
    video_subtitles = models.FileField(upload_to='subtitles/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    pages = models.ManyToManyField(Page, related_name='content', through='PageContent')

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"{dict(CONTENT_TYPE_CHOICES).get(self.content_type)}: {self.title}"


class PageContent(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ('-order',)
