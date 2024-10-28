from django.db import models

class Conta(models.Model):
    numero = models.IntegerField(unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

class Transacao(models.Model):
    TIPO_CHOICES = (
        ('deposito', 'Depósito'),
        ('saque', 'Saque'),
        ('transferencia', 'Transferência'),
    )
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes', blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    destino = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='transacoes_recebidas', blank=True, null=True)