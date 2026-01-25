from django.contrib import admin
from django.urls import path
from api.views import UploadAnalyzeView  # <--- Import the logic

urlpatterns = [
    path('admin/', admin.site.urls),
    # This is the line your Desktop App is looking for:
    path('api/upload/', UploadAnalyzeView.as_view()), 
]