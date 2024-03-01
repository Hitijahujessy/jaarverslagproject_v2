from django.urls import path
# Internals
from api.views import UserView, TokenView, CodeExplainView, AssistantView



urlpatterns = [
    path('users/', UserView.as_view(), name="users"),
    path('tokens/', TokenView.as_view(), name="tokens"),
    path('assistants/', AssistantView.as_view(), name="assistants"),
    path('code-explain/', CodeExplainView.as_view(), name="code-explain"),
]

