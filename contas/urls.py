from django.urls import path
from .views import ContaView, TransacaoView

urlpatterns = [
    path('contas/', ContaView.as_view(), name='contas'),
    path('transacoes/', TransacaoView.as_view(), name='transacoes'),
]