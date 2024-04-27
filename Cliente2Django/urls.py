from django.contrib import admin
from django.urls import include, path
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crudApp.urls')),

]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

