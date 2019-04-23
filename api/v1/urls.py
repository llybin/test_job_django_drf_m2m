from rest_framework import routers

from api.v1 import views

router = routers.DefaultRouter()

router.register('pages', views.PageViewSet, basename='pages')

urlpatterns = router.urls
