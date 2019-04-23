from django.test import TestCase, override_settings

from rest_framework import status
from rest_framework.test import APIClient


class PageListTest(TestCase):
    fixtures = [
        'initial_data.json'
    ]
    client = APIClient()

    def test_first_page(self):
        response = self.client.get('/api/v1/pages/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'count': 3,
                'next': 'http://testserver/api/v1/pages/?limit=2&offset=2',
                'previous': None,
                'results': [
                    {
                        'id': 3,
                        'url': 'http://testserver/api/v1/pages/3/',
                        'title': 'The third page',
                        'created_at': '2019-04-23T20:16:59.440000Z',
                        'modified_at': '2019-04-23T20:27:59.551000Z'
                    },
                    {
                        'id': 2,
                        'url': 'http://testserver/api/v1/pages/2/',
                        'title': 'The second empty page',
                        'created_at': '2019-04-23T20:16:53.550000Z',
                        'modified_at': '2019-04-23T20:16:53.550000Z'
                    }
                ]
            }
        )

    def test_pagination(self):
        response = self.client.get('/api/v1/pages/?limit=2&offset=2')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'count': 3,
                'next': None,
                'previous': 'http://testserver/api/v1/pages/?limit=2',
                'results': [
                    {
                        'id': 1,
                        'url': 'http://testserver/api/v1/pages/1/',
                        'title': 'The first page',
                        'created_at': '2019-04-23T20:16:44.903000Z',
                        'modified_at': '2019-04-23T20:27:37.365000Z'
                    }
                ]
            }
        )

    def test_default_order(self):
        response = self.client.get('/api/v1/pages/?limit=10')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertNotEqual(len(data['results']), 0)

        results = data['results']

        first_value = results.pop(0)['id']

        for r in results:
            self.assertGreater(first_value, r['id'])

    def test_fields(self):
        response = self.client.get('/api/v1/pages/?limit=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data['results']), 1)

        result = data['results'][0]

        self.assertSetEqual(
            set(result.keys()),
            {
                'id',
                'url',
                'title',
                'created_at',
                'modified_at',
            })


@override_settings(CELERY_ALWAYS_EAGER=True)
class PageDetailTest(TestCase):
    fixtures = [
        'initial_data.json'
    ]
    client = APIClient()

    def test_page_fields(self):
        response = self.client.get('/api/v1/pages/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.json()

        self.assertSetEqual(
            set(result.keys()),
            {
                'id',
                'url',
                'title',
                'content',
                'created_at',
                'modified_at',
            })

    def test_content_fields(self):
        response = self.client.get('/api/v1/pages/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data['content']), 4)

        content_video = data['content'][0]

        self.assertSetEqual(
            set(content_video.keys()),
            {
                'id',
                'counter',
                'title',
                'created_at',
                'modified_at',
                'video',
                'video_subtitles',
                'content_type',
            })

        content_audio = data['content'][1]

        self.assertSetEqual(
            set(content_audio.keys()),
            {
                'id',
                'counter',
                'title',
                'created_at',
                'modified_at',
                'audio',
                'audio_bitrate',
                'content_type',
            })

        content_text = data['content'][2]

        self.assertSetEqual(
            set(content_text.keys()),
            {
                'id',
                'counter',
                'title',
                'created_at',
                'modified_at',
                'text',
                'content_type',
            })

    def test_first_content(self):
        response = self.client.get('/api/v1/pages/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        content_text = data['content'][0]

        self.assertSetEqual(
            set(content_text.keys()),
            {
                'id',
                'counter',
                'title',
                'created_at',
                'modified_at',
                'video',
                'video_subtitles',
                'content_type',
            })

        self.assertEqual(content_text['id'], 4)
        self.assertEqual(content_text['title'], 'First video')
        self.assertEqual(content_text['created_at'], '2019-04-23T20:22:18.482000Z')
        self.assertEqual(content_text['video'], '/media/video/SampleVideo_360x240_1mb.mp4')
        self.assertEqual(content_text['content_type'], 2)

    def test_counter(self):
        response = self.client.get('/api/v1/pages/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data['content']), 4)

        content = data['content']

        counters = {}

        for x in content:
            counters[x['id']] = x['counter']

        response = self.client.get('/api/v1/pages/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data['content']), 4)

        content = data['content']

        for x in content:
            self.assertIn(x['id'], counters)
            self.assertEqual(x['counter'], counters[x['id']] + 1)

    def test_no_content(self):
        response = self.client.get('/api/v1/pages/2/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(len(data['content']), 0)
