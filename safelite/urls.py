# You should always use include() when you include other URL patterns. admin.site.urls is the only exception to this.
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('dashboard.urls')),
    path('admin/', admin.site.urls),
]
