from django.urls import path
# Internals
from api.views import UserView, TokenView, CodeExplainView, AssistantView, AssistantDetailEditAPIView, ChatView, FileUploadAPIView


urlpatterns = [
    path('users/', UserView.as_view(), name="users"),
    path('tokens/', TokenView.as_view(), name="tokens"),
    path('assistants/', AssistantView.as_view(), name="assistants"),
    path("assistants/<int:pk>/", AssistantDetailEditAPIView.as_view(), name="assistant-detail-edit"),
    path('chat/', ChatView.as_view(), name="chat"),
    # path('code-explain/', CodeExplainView.as_view(), name="code-explain"),
    # path('upload-file/', FileUploadAPIView.as_view(), name='upload-file'),
]

