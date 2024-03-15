from rest_framework import views, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken

# Import your serializers and models
from api.serializers import CodeExplainSerializer, UserSerializer, TokenSerializer, AssistantSerializer, ChatSerializer, FileUploadSerializer
from api.models import CodeExplainer, Assistant

class NoAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return None

class AssistantDetailAPIView(views.APIView):
    serializer_class = AssistantSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, pk):
        try:
            return Assistant.objects.get(pk=pk)
        except Assistant.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def get(self, request, pk, format=None):
        assistant = self.get_object(pk)
        serializer = self.serializer_class(assistant)  # Removed many=True because it's a single object
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        assistant = self.get_object(pk)  # Use get_object which handles DoesNotExist
        serializer = self.serializer_class(assistant, data=request.data)  # Pass instance for update
        if serializer.is_valid():
            serializer.save()  # Internally calls update or create
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssistantView(views.APIView):
    serializer_class = AssistantSerializer
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, format=None):
        qs = Assistant.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatView(views.APIView):
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, format=None):
        qs = CodeExplainer.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CodeExplainView(views.APIView):
    serializer_class = CodeExplainSerializer
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, format=None):
        qs = CodeExplainer.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # Temporarily AllowAny, change later
    def get(self, request, format=None):
        qs = User.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(ObtainAuthToken):
    serializer_class = TokenSerializer
    permission_classes = [AllowAny] # Temporarily AllowAny, change later

class FileUploadAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(User=request.user) # Provide the user information
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
