from django.shortcuts import render

# Create your views here.
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import EquipmentData

class UploadAnalyzeView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=400)

        file_obj = request.FILES['file']
        instance = EquipmentData.objects.create(file=file_obj)

        try:
            # Pandas Logic
            df = pd.read_csv(instance.file.path)
            stats = {
                "total_count": len(df),
                "avg_pressure": round(df['Pressure'].mean(), 2) if 'Pressure' in df else 0,
                "avg_temp": round(df['Temperature'].mean(), 2) if 'Temperature' in df else 0,
                "chart_labels": df['Type'].unique().tolist(),
                "chart_data": df['Type'].value_counts().reindex(df['Type'].unique(), fill_value=0).tolist()
            }
            return Response({"status": "success", "stats": stats})
        except Exception as e:
            return Response({"error": str(e)}, status=500)