from django.urls import path, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from rest_framework import routers

from devices import views as devices

from datas import views as datas

router = routers.DefaultRouter()

urlpatterns = i18n_patterns(
    # dashboard panels index page
    path('', devices.index, name='index'),

    # device api key
    path('key/list/', devices.key_list, name='key_list'),
    path('key/generate/<str:id>/', devices.generate_key, name='generate_key'),

    # add device
    path('device/add/', devices.device_add, name='device_add'),
    path('device/list/', devices.device_list, name='device_list'),
    path('device/edit/<str:id>/', devices.device_edit, name='device_edit'),
    path('device/delete/<str:id>/', devices.device_delete, name='device_delete'),

    # data query
    path('datas/', datas.datalist, name='datas'),
    path('datas/chart/<str:id>/', datas.data_chart, name='data_chart'),
    path('datas/chart/ajax/<str:id>/', datas.data_chart_ajax, name='data_chart_ajax'),

    # export xls
    path('export/<str:model>/', datas.export, name='export'),

    # django admin page
    path('admin/', admin.site.urls),
)

urlpatterns += [
    # REST framework
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/datas/', datas.DataList.as_view(), name='api_data'),
    path('api/datas/<int:pk>/', datas.DataDetail.as_view(), name='api_data_detail'),
]

urlpatterns += [
    path('media/<str:path>/', serve, {'document_root': settings.MEDIA_ROOT, }),
    path('static/<str:path>/', serve, {'document_root': settings.STATIC_ROOT, }),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
