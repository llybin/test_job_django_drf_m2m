from rest_framework import serializers

from base.models import Page, Content, ContentType
from api.v1.tasks import increase_content_counter


class PagesSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:v1:pages-detail')

    class Meta:
        model = Page
        fields = (
            'id',
            'url',
            'title',
            'created_at',
            'modified_at',
        )


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'id',
            'content_type',
            'counter',
            'title',
            'audio',
            'audio_bitrate',
            'created_at',
            'modified_at',
        )


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'id',
            'content_type',
            'counter',
            'title',
            'video',
            'video_subtitles',
            'created_at',
            'modified_at',
        )


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'id',
            'content_type',
            'counter',
            'title',
            'text',
            'created_at',
            'modified_at',
        )


class ContentRelatedField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        if value.content_type == ContentType.AUDIO:
            serializer = AudioSerializer(value)
        elif value.content_type == ContentType.VIDEO:
            serializer = VideoSerializer(value)
        elif value.content_type == ContentType.TEXT:
            serializer = TextSerializer(value)
        else:
            raise Exception('Unexpected type of object')

        return serializer.data


class ManyContentRelatedField(serializers.ManyRelatedField):
    def to_representation(self, value):
        data = super().to_representation(value)

        content = tuple(x['id'] for x in data)

        increase_content_counter.delay(content)

        return data


class PageDetailSerializer(PagesSerializer):
    content = ManyContentRelatedField(ContentRelatedField(), read_only=True)

    class Meta:
        model = Page
        fields = (
            'id',
            'url',
            'title',
            'created_at',
            'modified_at',
            'content',
        )
