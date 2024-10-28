from rest_framework import serializers
from .models import Conta, Transacao

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['numero', 'saldo']


class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ['tipo', 'conta', 'destino', 'valor']

    def create(self, validated_data):
        conta_numero = validated_data['conta']
        conta = Conta.objects.get(numero=conta_numero)
        validated_data['conta'] = conta

        if validated_data['tipo'] == 'transferencia':
            destino_numero = validated_data['destino']
            destino = Conta.objects.get(numero=destino_numero)
            validated_data['destino'] = destino

        return Transacao.objects.create(**validated_data)

# class TransacaoSerializer(serializers.ModelSerializer):
#     conta = serializers.SerializerMethodField()
#     destino = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Transacao
#         fields = ['tipo', 'conta', 'valor', 'destino']
#
#     def get_conta(self, obj):
#         return obj.conta.numero
#
#     def get_destino(self, obj):
#         if obj.destino:
#             return obj.destino.numero
#         return None
