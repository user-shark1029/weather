import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings

from .services import get_real_weather
from .models import ForecastModel
from .serializers import (
    CurrentWeatherSerializer,
    ForecastRequestSerializer,
    ForecastOverrideSerializer,
)

class CurrentWeatherView(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({"error": "Параметр 'city' обязателен."}, status=status.HTTP_400_BAD_REQUEST)
        weather_data = get_real_weather(city)
        if weather_data is None:
            return Response({"error": "Город не найден или ошибка получения данных."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CurrentWeatherSerializer(weather_data)
        return Response(serializer.data)

class WeatherForecastView(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        date_str = request.query_params.get('date')
        if not city or not date_str:
            return Response({"error": "Параметры 'city' и 'date' обязательны."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ForecastRequestSerializer(data={'city': city, 'date': date_str})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data['date']
        data = ForecastModel.objects.filter(city__iexact=city, date=validated_data).first()
        if data:
            response_data = {
                "min_temperature": data.min_temperature,
                "max_temperature": data.max_temperature,
            }
            return Response(response_data)
        weather_info = get_real_weather(city)
        if weather_info is None:
            return Response({"error": "Город не найден или ошибка получения данных."}, status=status.HTTP_404_NOT_FOUND)
        temp_current = weather_info['temperature']
        response_data = {
            "min_temperature": temp_current - 5,
            "max_temperature": temp_current + 5,
        }
        return Response(response_data)
    
    def post(self, request):
        serializer = ForecastOverrideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_validated = serializer.validated_data
        obj, created = ForecastModel.objects.update_or_create(
            city=data_validated['city'],
            date=data_validated['date'],
            defaults={
                'min_temperature': data_validated['min_temperature'],
                'max_temperature': data_validated['max_temperature'],
            }
        )
        return Response({
            "message": f"Прогноз для {obj.city} на {obj.date} успешно сохранён.",
            "created": created,
         })
    