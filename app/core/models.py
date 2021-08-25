from django.db import models

status_choice_field = [
    (1, 'Enable'),
    (0, 'Disable')
]


class Coin(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    code = models.IntegerField()
    url = models.URLField()
    indicators_url = models.URLField()
    status = models.IntegerField(choices=status_choice_field, default=1)


class Predict(models.Model):
    coin = models.ForeignKey('Coin', models.CASCADE)
    batch_number = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, null=True)
    price_change_one_hour = models.FloatField(blank=True, null=True)
    price_change_one_day = models.FloatField(blank=True, null=True)
    price_change_seven_days = models.FloatField(blank=True, null=True)
    price_change_one_month = models.FloatField(blank=True, null=True)
    price_change_one_year = models.FloatField(blank=True, null=True)
    price_change_since_ath = models.FloatField(blank=True, null=True)
    price_prediction_one_day = models.FloatField(blank=True, null=True)
    price_prediction_one_month = models.FloatField(blank=True, null=True)
    price_prediction_one_year = models.FloatField(blank=True, null=True)
    price_forecast_one = models.FloatField(blank=True, null=True)
    price_forecast_two = models.FloatField(blank=True, null=True)
    price_forecast_three = models.FloatField(blank=True, null=True)
    price_forecast_four = models.FloatField(blank=True, null=True)
    sell = models.IntegerField(blank=True, null=True)
    neutral = models.IntegerField(blank=True, null=True)
    buy = models.IntegerField(blank=True, null=True)
    rank_1 = models.IntegerField(blank=True, null=True)
    rank_2 = models.IntegerField(blank=True, null=True)
    rank_3 = models.IntegerField(blank=True, null=True)
    rank_4 = models.IntegerField(blank=True, null=True)

