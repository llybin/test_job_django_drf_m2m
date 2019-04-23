from django.db import models
from django.core.exceptions import ValidationError


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

CONTENT_TYPE_CHOICES_DICT = dict(CONTENT_TYPE_CHOICES)

# field name - required
CONTENT_TYPE_CUSTOM_FIELDS = {
    ContentType.AUDIO: (('audio', True), ('audio_bitrate', False)),
    ContentType.VIDEO: (('video', True), ('video_subtitles', False)),
    ContentType.TEXT: (('text', True),),
}

# fill dynamic all custom fields on start for using in validator
ALL_CONTENT_TYPE_CUSTOM_FIELDS = set()
for _content_type in CONTENT_TYPE_CUSTOM_FIELDS:
    for _f in CONTENT_TYPE_CUSTOM_FIELDS[_content_type]:
        ALL_CONTENT_TYPE_CUSTOM_FIELDS.add(_f[0])


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

    def content_type_validator(self, fields):
        for f in fields:
            if f[1] and not getattr(self, f[0]):
                raise ValidationError(
                    {f[0]: f"Must be filled for type: {CONTENT_TYPE_CHOICES_DICT[self.content_type]}"})

        type_fields = set(x[0] for x in fields)
        non_type_fields = ALL_CONTENT_TYPE_CUSTOM_FIELDS - type_fields

        for f in non_type_fields:
            if getattr(self, f):
                raise ValidationError(
                    {f: f"Must be empty for type: {CONTENT_TYPE_CHOICES_DICT[self.content_type]}"})

    def clean(self):
        self.content_type_validator(CONTENT_TYPE_CUSTOM_FIELDS[self.content_type])

    def __str__(self):
        return f"{CONTENT_TYPE_CHOICES_DICT[self.content_type]}: {self.title}"


class PageContent(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ('-order',)
