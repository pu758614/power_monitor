
from django.contrib import admin
from django.urls import path
from app import views,api_view
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('stream/', views.stream_view, name='stream'),
    path('stream/', views.stream_rtsp, name='stream_rtsp'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('api/getDevKpiDayList', api_view.getDevKpiDayList),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
