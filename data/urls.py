'''
Url routing for the `data` django app
'''

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from data import views


app_name = 'data'

# Register drf views
router = DefaultRouter()

router.register(r'abstractmodel', views.AbstractModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
