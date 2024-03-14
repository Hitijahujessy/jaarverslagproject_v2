from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# Internals
from api.models import CodeExplainer, Assistant, Chat, UploadedFile
from api.utils import send_code_to_api, create_new_assistant, modify_assistant, send_message_to_assistant


class AssistantSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=True)
    new_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Assistant
        fields = (
            "id",
            "name",
            "new_name",
            "company_name",
            "instructions",
            "created_at",
            "updated_at",
            "query_count",
            "files"
        )
        extra_kwargs = {
            'files': {'required': False},
        }

        
    def create(self, validated_data):
        new_assistant = Assistant(**validated_data)
        data = create_new_assistant(
            validated_data["name"], 
            validated_data["company_name"], 
            validated_data["instructions"], 
            validated_data["files"])
        new_assistant.save()
        return new_assistant
    
    def update(self, instance, validated_data):
        # new_name = validated_data.get('new_name')
        
        # Update the instance with validated_data
        instance.name = validated_data.get('name', instance.name)
        new_name = validated_data.get('new_name', instance.name)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.files = validated_data.get('files', instance.files)
        
        # Now, you can call your modify_assistant function if needed
        # Assuming modify_assistant updates some external system and doesn't return anything
        modify_assistant(
            instance.name, 
            new_name,
            instance.company_name, 
            instance.instructions,
            instance.files)

        # Don't forget to save the instance after modifying it
        instance.save()
        
        # Return the updated instance
        return instance
    
    
class ChatSerializer(serializers.ModelSerializer):
    assistant_name = serializers.SlugRelatedField(slug_field='name', queryset=Assistant.objects.all(), source='assistant')

    class Meta:
        model = Chat
        fields = (
            "id",
            "assistant_name",
            "_input",
            "_output"
        )
        extra_kwargs = {
            "_output": {"read_only": True}
        }
        
    def create(self, validated_data):
        assistant = validated_data['assistant']  # Extract the assistant instance
        _output = send_message_to_assistant(assistant.name, validated_data["_input"])
        chat = Chat(**validated_data, _output=_output)
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