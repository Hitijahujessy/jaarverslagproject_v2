from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.urls import reverse
# Internals
from api.models import Assistant, Chat
from api.utils import create_new_assistant, modify_assistant, send_message_to_assistant


class AssistantSerializer(serializers.ModelSerializer):
    
    company_name = serializers.CharField(required=True)
    new_name = serializers.CharField(write_only=True, required=False)
    
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('detail', kwargs={'pk': obj.pk}))
        return None
    
    class Meta:
        model = Assistant
        fields = (
            "id",
            "openai_id",
            "url",
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
        # Use .get to avoid KeyError if 'files' is not in validated_data
        files = validated_data.get('files')
        
        openai_assistant = create_new_assistant(
            validated_data["name"], 
            validated_data["company_name"], 
            validated_data["instructions"], 
            files
            )
        openai_id = openai_assistant.id
        new_assistant = Assistant(openai_id=openai_id, **validated_data)
        
        new_assistant.save()
        return new_assistant
    
    def update(self, instance, validated_data):
        # Directly update instance fields with new values from validated_data
        new_name = validated_data.get('new_name', None)  # Assume 'new_name' is the field for updates
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.updated_at = timezone.now()
        # Check if 'files' is in validated_data and only update if present
        if 'files' in validated_data:
            instance.files = validated_data['files']
        else:
            instance.files = instance.files

        # Assuming modify_assistant updates the name in an external OpenAI API
        modify_assistant(
            instance.openai_id, 
            new_name,
            instance.company_name, 
            instance.instructions,
            instance.files
        )
        
        if new_name:
            instance.name = new_name  # Update the name if new_name is provided
            
        # Save the instance after all updates
        instance.save()

        # Refresh the instance from DB to reflect any changes
        instance.refresh_from_db()

        return instance
    
    
class ChatSerializer(serializers.ModelSerializer):
    assistant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chat
        fields = (
            "id",
            "assistant_id",
            "input",
            "output"
        )
        extra_kwargs = {
            "output": {"read_only": True},
        }
        
    def create(self, validated_data):
        # Use the assistant_id to get the Assistant instance
        assistant_id = validated_data.pop('assistant_id')
        assistant = Assistant.objects.get(id=assistant_id)

        # Now that you have the assistant, you can use its openai_id
        output = send_message_to_assistant(assistant.openai_id, validated_data["input"])

        # Create the Chat instance with the output
        chat = Chat(assistant=assistant, **validated_data, output=output)
        chat.save()
        return chat
    
    
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
