
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ocr_app.views import upload_file,display_data,download_excel

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",upload_file,name="upload_file"),
    path("display_data/",display_data,name="display_data"),
    path("download/",download_excel,name="download_excel"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
