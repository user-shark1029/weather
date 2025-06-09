from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils import timezone

from .models import ForecastModel

class CurrentWeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    local_time = serializers.CharField()

def validate_date_format(value):
    # try:
    #     dt = datetime.strptime(value, "%d.%m.%Y").date()
    # except ValueError:
    #     raise serializers.ValidationError("Дата должна быть в формате dd.MM.yyyy")
    today = timezone.now().date()
    max_date = today + timedelta(days=10)
    if value < today:
        raise serializers.ValidationError("Дата не может быть в прошлом")
    if value > max_date:
        raise serializers.ValidationError("Дата не может быть более чем на 10 дней вперёд")
    return value

class ForecastRequestSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    date = serializers.DateField(input_formats=['%d.%m.%Y'])

    def validate_date(self, value):
        return validate_date_format(value)

class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = ForecastModel
        fields = ['city', 'date', 'min_temperature', 'max_temperature']

    def validate_date(self, value):
        return validate_date_format(value)

    def validate(self, data):
        min_temp = data.get('min_temperature')
        max_temp = data.get('max_temperature')
        if min_temp is not None and max_temp is not None:
            if min_temp > max_temp:
                raise serializers.ValidationError("Минимальная температура не может быть больше максимальной.")
        return data