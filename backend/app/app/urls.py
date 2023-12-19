from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('account.urls')),
    path('', include('main.urls')),
    path('', include('article.urls')),
    path('', include('tests.urls')),
    path('profile/', include('user_profile.urls')),

    path('analytics/', include('analytics.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
