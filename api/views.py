from rest_framework import views, status, serializers
from rest_framework.response import Response
from django.http import Http404
from django.urls import reverse
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken

# Import your serializers and models
from api.serializers import UserSerializer, TokenSerializer, AssistantSerializer, ChatSerializer
from api.models import Assistant, Chat

class NoAuthentication(BaseAuthentication):
    """Custom authentication class that bypasses all authentication."""
    def authenticate(self, request):
        # Return None to ensure no user is associated with the request
        return None

class AssistantDetailAPIView(views.APIView):
    """
    API view to retrieve, update, or delete assistant details.
    """
    serializer_class = AssistantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        """Attempt to get the assistant by primary key (pk) or raise Http404."""
        try:
            return Assistant.objects.get(pk=pk)
        except Assistant.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """Handle GET request to retrieve an assistant by pk."""
        assistant = self.get_object(pk)
        serializer = AssistantSerializer(assistant, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Handle PUT request to update an assistant by pk."""
        assistant = self.get_object(pk)
        serializer = self.serializer_class(assistant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        assistant = self.get_object(pk)
        serializer = self.serializer_class(assistant, data=request.data)
        if serializer.is_valid():
            # serializer.delete(assistant)
            # serializer = self.serializer_class(data=request.data)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssistantView(views.APIView):
    """
    A view that supports listing all Assistant instances or creating a new Assistant instance.
    This view handles GET and POST requests: GET requests return a list of all assistants,
    and POST requests allow for the creation of a new assistant with provided data.

    Attributes:
        serializer_class (AssistantSerializer): The serializer class used for validating and
            deserializing input, and for serializing output.
        authentication_classes (list): Authentication methods/classes used for this view.
        permission_classes (list): Permissions required to interact with this view.
    """
    serializer_class = AssistantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """Handle GET request to list all assistants."""
        qs = Assistant.objects.all()
        serializer = self.serializer_class(qs, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Handle POST request to create a new assistant."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    


class ChatView(views.APIView):
    """
    API view to list or create chat records.
    """
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """Handle GET request to list all chat records (Dummy implementation)."""
        chat = Chat.objects.all()  # Placeholder for actual chat retrieval logic
        serializer = self.serializer_class(chat, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """Handle POST request to create a new chat record."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ChatDetailAPIView(views.APIView):
    """
    API view to retrieve, update, or delete assistant details.
    """
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    
    def get_object(self, pk):
        """Attempt to get the assistant by primary key (pk) or raise Http404."""
        try:
            return Chat.objects.get(pk=pk)
        except Chat.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """Handle GET request to retrieve an assistant by pk."""
        chat = self.get_object(pk)
        serializer = ChatSerializer(chat, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Handle PUT request to update an assistant by pk."""
        chat = self.get_object(pk)
        serializer = self.serializer_class(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
class UserView(views.APIView):
    """
    API view to list or create users. Temporarily allows any access.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """Handle GET request to list all users (Dummy implementation)."""
        qs = ""  # Placeholder for User.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        """Handle POST request to create a new user."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TokenView(ObtainAuthToken):
    """
    API view to obtain authentication token.
    """
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]
