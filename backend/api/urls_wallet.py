from django.urls import path
from ..wallet_api import (
    WalletBalanceView, WalletCreateView, BankAccountLinkView, 
    DepositView, WithdrawView, TransferView, EscrowLockView,
    SavingsDepositView, TransactionHistoryView, PaymentAuthorizationView
)

urlpatterns = [
    path('wallet/balance', WalletBalanceView.as_view()),
    path('wallet/create', WalletCreateView.as_view()),
    path('wallet/link-bank', BankAccountLinkView.as_view()),
    path('wallet/deposit', DepositView.as_view()),
    path('wallet/withdraw', WithdrawView.as_view()),
    path('wallet/transfer', TransferView.as_view()),
    path('wallet/escrow/lock', EscrowLockView.as_view()),
    path('wallet/savings/deposit', SavingsDepositView.as_view()),
    path('wallet/history', TransactionHistoryView.as_view()),
    path('wallet/authorize-payment', PaymentAuthorizationView.as_view()),
]
