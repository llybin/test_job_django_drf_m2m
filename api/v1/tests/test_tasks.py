from django.test import TestCase

from base.models import Page
from api.v1.tasks import increase_content_counter


class CounterTest(TestCase):
    fixtures = [
        'initial_data.json'
    ]

    def test_empty_list(self):
        increase_content_counter(tuple())
        self.assertTrue(True)

    def test_ok(self):
        page = Page.objects.get(id=1)

        data = page.content.all()
        self.assertEqual(len(data), 4)

        counters = {}
        for x in data:
            counters[x.id] = x.counter

        increase_content_counter(tuple(counters.keys()))

        for x in data:
            x.refresh_from_db()

            self.assertIn(x.id, counters)
            self.assertEqual(x.counter, counters[x.id] + 1)
