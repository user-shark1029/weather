from django.urls import path, include
from .views import CurrentWeatherView, WeatherForecastView



urlpatterns_weather = [
    path('current/', CurrentWeatherView.as_view(), name='current-weather'),
    path('forecast/', WeatherForecastView.as_view(), name='weather-forecast'),
]

urlpatterns = [
    path('weather/', include(urlpatterns_weather))
]