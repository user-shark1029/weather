from django.db import models

class ForecastModel(models.Model):
    city = models.CharField(max_length=100,
                            verbose_name='Город')
    date = models.DateField(verbose_name='Дата')
    min_temperature = models.DecimalField(max_digits=3,
                                          decimal_places=1,
                                          verbose_name='Минимальная температура')
    max_temperature = models.DecimalField(max_digits=3,
                                          decimal_places=1,
                                          verbose_name='Максимальная температура')

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'

    def __str__(self):
        return f"{self.city} - {self.date}"