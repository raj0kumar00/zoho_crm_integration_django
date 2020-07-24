
from django.contrib import admin
from django.urls import path, include
from zoho import urls as zohourls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(zohourls)),
]
