'''
Url routing for the `data` django app
'''

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from data import views


app_name = 'data'

# Register drf views
router = DefaultRouter()

router.register('abstractmodel', views.AbstractModelViewSet)
router.register('amlink', views.AMLinkViewSet)
router.register('attribute', views.AttributeViewSet)
router.register('instance', views.InstanceViewSet)
router.register('measure', views.MeasureViewSet)

urlpatterns = [
	path('retrieve-data', views.RetrieveDataView.as_view(), name='retrieve-data'),
	path('upload-csv/', views.UploadCsvFileView.as_view(), name='upload-csv'),
    path('', include(router.urls)),
]
