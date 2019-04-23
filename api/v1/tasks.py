import logging

from django.db.models import F

from project.celeryconf import app
from base.models import Content


logger = logging.getLogger(__name__)


@app.task(queue='content_counter')
def increase_content_counter(content: tuple):
    logger.info(f"Content ids: {content} increasing counter")
    Content.objects.filter(id__in=content).update(counter=F('counter') + 1)

