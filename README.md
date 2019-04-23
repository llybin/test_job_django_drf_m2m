Test job
-

Django, DRF, celery, many-to-many, docker, docker-compose

See test.pdf

[Variant with generic](https://github.com/llybin/test_job_django_drf_gm2m)

File fixtures
-

cp -r base/fixtures/media/* media

Web
-

docker-compose up runserver celery

Admin access: root:root

http://0.0.0.0:8000/admin/
http://0.0.0.0:8000/api/v1/

GET http://0.0.0.0:8000/api/v1/pages/ 200

```
{
    "count": 3,
    "next": "http://0.0.0.0:8000/api/pages/?limit=2&offset=2",
    "previous": null,
    "results": [
        {
            "id": 3,
            "url": "http://0.0.0.0:8000/api/v1/pages/3/",
            "title": "The third page",
            "created_at": "2019-04-23T20:16:59.440000Z",
            "modified_at": "2019-04-23T20:27:59.551746Z"
        },
        {
            "id": 2,
            "url": "http://0.0.0.0:8000/api/v1/pages/2/",
            "title": "The second empty page",
            "created_at": "2019-04-23T20:16:53.550000Z",
            "modified_at": "2019-04-23T20:16:53.550000Z"
        }
    ]
}
```

GET http://127.0.0.1:8000/api/v1/pages/3/ 200

```
{
    "id": 3,
    "url": "http://0.0.0.0:8000/api/v1/pages/3/",
    "title": "The third page",
    "created_at": "2019-04-23T20:16:59.440000Z",
    "modified_at": "2019-04-23T20:27:59.551000Z",
    "content": [
        {
            "id": 5,
            "content_type": 2,
            "counter": 0,
            "title": "The second video with sub",
            "video": "/media/video/SampleVideo_360x240_1mb_vVqX6In.mp4",
            "video_subtitles": "/media/subtitles/video.sub",
            "created_at": "2019-04-23T20:23:05.343000Z",
            "modified_at": "2019-04-23T20:23:05.343000Z"
        },
        {
            "id": 3,
            "content_type": 1,
            "counter": 0,
            "title": "first audio",
            "audio": "/media/audio/SampleAudio_0.4mb.mp3",
            "audio_bitrate": 64,
            "created_at": "2019-04-23T20:21:45.159000Z",
            "modified_at": "2019-04-23T20:21:45.159000Z"
        }
    ]
}
```


Tests
-

docker-compose up autotests
