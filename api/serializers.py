from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# Internals
from api.models import CodeExplainer, Assistant, Chat, UploadedFile
from api.utils import send_code_to_api, create_new_assistant, send_message_to_assistant


class AssistantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assistant
        fields = (
            "id",
        "name",
        "description",
        "instructions",
        "created_at",
        "updated_at",
        "query_count"
        )
        
    def create(self, validated_data):
        new_assistant = Assistant(**validated_data)
        data = create_new_assistant(validated_data["name"], validated_data["description"])
        new_assistant.save()
        return new_assistant
    
    
class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = (
            "id",
        "_input",
        "_output"
        )
        extra_kwargs = {
            "_output":{"read_only":True}
        }

    def create(self, validated_data):
        chat = Chat(**validated_data)
        _output = send_message_to_assistant(validated_data["_input"])
        chat._output = _output
        chat.save()
        return chat
    
    

class CodeExplainSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CodeExplainer
        fields = (
            "id",
        "_input",
        "_output"
        )
        extra_kwargs = {
            "_output":{"read_only":True}
        }
    
    def create(self, validated_data):
        ce = CodeExplainer(**validated_data)
        _output = send_code_to_api(validated_data["_input"])
        ce._output = _output
        ce.save()
        return ce
    
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password"
        )
        extra_kwargs = {
            "password":{"write_only": True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        # Save the password as hashed and crypted
        
        user.set_password(password)
        user.save()
        
        # Token based authentication
        Token.objects.create(user=user)
        
        return user
    
    
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type":"password"}, trim_whitespace=False)
    
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), username=username, password=password)
        if not user:
            msg = "Credentials are not provided correctly."
            raise serializers.ValidationError(msg, code="authentication")
        attrs["user"] = user
        return attrs

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'