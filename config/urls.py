from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from common.views import SystemView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('comments.urls')),
    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = SystemView.as_view(template_name='common/errors/pages_error.html', status=404)
handler400 = SystemView.as_view(template_name='common/errors/pages_error.html', status=400)
handler500 = SystemView.as_view(template_name='common/errors/pages_error.html', status=500)