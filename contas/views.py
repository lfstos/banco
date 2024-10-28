from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import F
from .models import Conta, Transacao
from .serializers import ContaSerializer, TransacaoSerializer
import logging

logger = logging.getLogger(__name__)

class ContaView(APIView):
    def post(self, request):
        logger.info('Requisição para criar conta')
        serializer = ContaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('Conta criada com sucesso')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransacaoView(APIView):
    def post(self, request):
        logger.info('Requisição para realizar transação')
        try:
            with transaction.atomic():
                if 'contas' in request.data and 'transacoes' in request.data:
                    # Cria ou atualiza contas sem alterar o saldo
                    for conta_data in request.data['contas']:
                        Conta.objects.get_or_create(numero=conta_data['numero'])

                    # Processa transações
                    for transacao_data in request.data['transacoes']:
                        if transacao_data['tipo'] in ['deposito', 'saque']:
                            conta = Conta.objects.get(numero=transacao_data['conta'])

                            if transacao_data['tipo'] == 'deposito':
                                conta.saldo += transacao_data['valor']
                            elif transacao_data['tipo'] == 'saque':
                                if conta.saldo < transacao_data['valor']:
                                    return Response({'erro': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
                                conta.saldo -= transacao_data['valor']
                            conta.save()

                            transacao = Transacao(
                                tipo=transacao_data['tipo'],
                                conta=conta,
                                valor=transacao_data['valor']
                            )
                            transacao.save()
                            logger.info('Transação %s realizada com sucesso', transacao_data['tipo'])

                        elif transacao_data['tipo'] == 'transferencia':
                            conta_origem = Conta.objects.get(numero=transacao_data['origem'])
                            conta_destino = Conta.objects.get(numero=transacao_data['destino'])
                            if conta_origem.saldo < transacao_data['valor']:
                                logger.error('Saldo insuficiente na conta %s para transferência', conta_origem.numero)
                                return Response({'erro': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
                            conta_origem.saldo -= transacao_data['valor']
                            conta_destino.saldo += transacao_data['valor']
                            conta_origem.save()
                            conta_destino.save()

                            transacao = Transacao(
                                tipo=transacao_data['tipo'],
                                conta=conta_origem,
                                valor=transacao_data['valor'],
                                destino=conta_destino
                            )
                            transacao.save()
                            logger.info('Transferência de %s para %s realizada com sucesso', conta_origem.numero, conta_destino.numero)

                    saldos = Conta.objects.values('numero', 'saldo')
                    return Response({'Saldos das Contas': list(saldos)}, status=status.HTTP_201_CREATED)

                elif 'tipo' in request.data and 'conta' in request.data and 'valor' in request.data:
                    conta, _ = Conta.objects.get_or_create(numero=request.data['conta'])

                    if request.data['tipo'] == 'deposito':
                        conta.saldo += request.data['valor']
                    elif request.data['tipo'] == 'saque':
                        if conta.saldo < request.data['valor']:
                            return Response({'erro': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
                        conta.saldo -= request.data['valor']
                    elif request.data['tipo'] == 'transferencia':
                        conta_destino = Conta.objects.get(numero=request.data['destino'])
                        if conta.saldo < request.data['valor']:
                            return Response({'erro': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
                        conta.saldo -= request.data['valor']
                        conta_destino.saldo += request.data['valor']
                        conta_destino.save()
                    conta.save()

                    transacao = Transacao(
                        tipo=request.data['tipo'],
                        conta=conta,
                        valor=request.data['valor'],
                        destino=request.data.get('destino')
                    )
                    transacao.save()
                    logger.info('Transação %s realizada com sucesso', request.data['tipo'])
                    saldos = Conta.objects.values('numero', 'saldo')
                    logger.info('Transações processadas com sucesso')
                    return Response({'Saldo da Conta': conta.saldo}, status=status.HTTP_201_CREATED)
                else:
                    logger.warning('Dados inválidos na requisição: %s', request.data)
                    return Response({'erro': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception('Erro ao processar transação')
            return Response({'erro': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
