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
router.register(r'amlink', views.AMLinkViewSet)
router.register(r'attribute', views.AttributeViewSet)
router.register(r'measure', views.MeasureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
