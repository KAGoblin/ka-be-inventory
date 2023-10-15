"""
URL configuration for ka_starter_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import re_path
from oscar.views import handler403
from oscar.views import handler404
from oscar.views import handler500

urlpatterns = [
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    re_path(r'^admin/django-rq/', include('django_rq.urls')),
    re_path(r'^admin/su/', include('django_su.urls')),
    re_path(r'^admin/', admin.site.urls),

    # API Layer for oscar
    # re_path(r'^api/v2/', api_v2.urls),
    re_path(r'^api/', include("oscarapi.urls")),

    # oscar
    # - Block default public views (because we're only using it as API server)
    re_path(r'^catalogue/', handler404,
            kwargs={'exception': Exception('Page not Found')}),
    re_path(r'^basket/', handler404,
            kwargs={'exception': Exception('Page not Found')}),
    re_path(r'^checkout/', handler404,
            kwargs={'exception': Exception('Page not Found')}),
    re_path(r'^search/', handler404,
            kwargs={'exception': Exception('Page not Found')}),
    re_path(r'^offers/', handler404,
            kwargs={'exception': Exception('Page not Found')}),
    # - Get default oscar application routes
    re_path(r'', include(apps.get_app_config('oscar').urls[0])),
]

if settings.DEBUG:
    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        re_path(r'^403$', handler403, kwargs={
                'exception': Exception('Permission Denied')}),
        re_path(r'^404$', handler404, kwargs={
                'exception': Exception('Page not Found')}),
        re_path(r'^500$', handler500, kwargs={
                'exception': Exception('Internal Server Error')}),
    ]
