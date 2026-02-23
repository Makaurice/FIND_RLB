from django.urls import path
from ..find_token_api import TokenBalanceView, TokenTransferView, TokenClaimTeamView

urlpatterns = [
    path('token/balance/<str:address>', TokenBalanceView.as_view()),
    path('token/transfer', TokenTransferView.as_view()),
    path('token/claim-team', TokenClaimTeamView.as_view()),
]
