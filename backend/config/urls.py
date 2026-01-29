from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # <--- Built-in Login View
from api.views import UploadAnalyzeView, HistoryView, GeneratePDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', obtain_auth_token),  # <--- Login URL
    path('api/upload/', UploadAnalyzeView.as_view()),
    path('api/history/', HistoryView.as_view()),
    path('api/pdf/', GeneratePDFView.as_view()), # <--- PDF URL
]