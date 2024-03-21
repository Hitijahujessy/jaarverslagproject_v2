from django.urls import path
# Internals
from api.views import UserView, TokenView, AssistantView, AssistantDetailAPIView, ChatView, ChatDetailAPIView


urlpatterns = [
    path('users/', UserView.as_view(), name="users"),
    path('tokens/', TokenView.as_view(), name="tokens"),
    path('assistants/', AssistantView.as_view(), name="assistants"),
    path("assistants/<int:pk>/", AssistantDetailAPIView.as_view(), name="detail"),
    path('chat/', ChatView.as_view(), name="chat"),
    path('chat/<int:pk>/', ChatDetailAPIView.as_view(), name="chat-detail"),
    
]

