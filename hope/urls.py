from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('', include('base.urls')),    # Base application URLs
    path('api/', include('base.api.urls'))  # API endpoints
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
