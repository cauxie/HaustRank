from django.db import models

class WalletStat(models.Model):
    wallet_address = models.CharField(max_length=255, unique=True)
    transactions = models.IntegerField(default=0)

    def get_level(self):
        if 20 <= self.transactions <= 90:
            return 1
        elif 100 <= self.transactions <= 200:
            return 2
        elif 201 <= self.transactions <= 400:
            return 3
        elif 401 <= self.transactions <= 999:
            return 4
        elif self.transactions >= 1000:
            return 5
        return 0  # less than 20 txns
