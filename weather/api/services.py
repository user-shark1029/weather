from datetime import datetime, timedelta
from django.conf import settings
import requests

def get_real_weather(city):
    """Получение информации от стороннего OPENWEATHER API"""

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={settings.OPENWEATHER_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            timezone_offset_sec = data.get('timezone', 0)
            local_time_dt = datetime.utcnow() + timedelta(seconds=timezone_offset_sec)
            local_time_str = local_time_dt.strftime("%H:%M")
            return {
                "temperature": temp,
                "local_time": local_time_str,
            }
        elif response.status_code == 404:
            return None
        else:
            return None
    except requests.RequestException:
        return None