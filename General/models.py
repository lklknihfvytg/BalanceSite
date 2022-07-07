from django.db import models


class Coin(models.Model):
	tic = models.CharField('Название', max_length = 5)
	leverage = models.IntegerField('Умножение')
	entry_price = models.FloatField('Цена входа')
	position_amt = models.FloatField('Кол-во')
	liquidation_price = models.FloatField('Цена ликвидации')
	mark_price = models.FloatField('Цена')
	unrealized_profit = models.FloatField('Плюс')
	notional = models.FloatField('Объем')
	warning = models.FloatField('Ликвидация')

#	class Meta:
#        verbose_name = 'Монета'
#        verbose_name_plural = 'Монеты'
