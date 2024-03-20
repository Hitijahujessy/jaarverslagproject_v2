from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.urls import reverse
# Internals
from api.models import Assistant, Chat
from api.utils import create_new_assistant, modify_assistant, delete_assistant, send_message_to_assistant


class AssistantSerializer(serializers.ModelSerializer):
    """
    A serializer for the Assistant model that supports both serialization for API
    responses and deserialization for creating or updating Assistant instances from API requests.
    This serializer includes custom handling for creating new Assistant instances with interactions
    with external services, as well as updating existing instances.

    Attributes:
        company_name (CharField): Required field for specifying the company name associated with the assistant.
        new_name (CharField): Optional write-only field used for updating an assistant's name.
        url (SerializerMethodField): Field to store the URL for the assistant's detail view, dynamically generated.
    """
    company_name = serializers.CharField(required=True)
    new_name = serializers.CharField(write_only=True, required=False)  # For updating assistant's name
    
    # Dynamically generated field for the assistant's detail view URL
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        """
        Method to generate a fully qualified URL for the assistant's detail view.

        Parameters:
            obj (Assistant): The Assistant instance for which the URL is being generated.

        Returns:
            str: The fully qualified URL to the assistant's detail view, if request context is available. Otherwise, None.
        """
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
            'files': {'required': False},  # Optional field for any files associated with the assistant
        }

    def create(self, validated_data):
        """
        Overridden create method to handle the creation of a new Assistant instance.
        This includes calling an external service to create an assistant with OpenAI
        and saving the returned OpenAI ID along with the assistant details in the database.

        Parameters:
            validated_data (dict): Data validated by the serializer to create a new Assistant instance.

        Returns:
            Assistant: The newly created Assistant instance.
        """
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
        """
        Overridden update method to handle updates to an existing Assistant instance.
        This includes potentially updating the assistant's details with an external service (e.g., OpenAI)
        and applying changes to the Assistant instance in the database.

        Parameters:
            instance (Assistant): The current instance of the Assistant being updated.
            validated_data (dict): Data validated by the serializer for updating the Assistant instance.

        Returns:
            Assistant: The updated Assistant instance.
        """
        new_name = validated_data.get('new_name', None)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.updated_at = timezone.now()
        
        if 'files' in validated_data:
            instance.files = validated_data['files']

        modify_assistant(
            instance.openai_id, 
            new_name,
            instance.company_name, 
            instance.instructions,
            instance.files
        )
        
        if new_name:
            instance.name = new_name
            
        instance.save()
        instance.refresh_from_db()
        return instance
    
    def delete(self, instance):

        delete_assistant(
            instance.openai_id 
        )
            
        instance.delete()
        # instance.refresh_from_db()
        return {"status": "deleted"}
    
    
class ChatSerializer(serializers.ModelSerializer):
    """
    A serializer for the Chat model that facilitates the serialization of chat data for 
    API responses and the deserialization of input data to create new Chat instances. 
    This serializer is specifically designed to handle chat interactions between users 
    and assistants, capturing both user inputs and assistant outputs.

    Attributes:
        assistant_id (IntegerField): A write-only field used to specify the assistant 
            involved in the chat. This field is necessary for creating a chat instance 
            but is not included in serialized Chat model instances returned in API responses.
    """

    # Write-only field to capture the assistant's ID involved in the chat
    assistant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chat
        fields = (
            "id",          # Unique identifier for the chat instance
            "assistant_id",# ID of the assistant involved in the chat (write-only)
            "input",       # User input message to the assistant
            "output"       # Assistant's response to the user input
        )
        extra_kwargs = {
            "output": {"read_only": True},  # Output is generated, thus read-only
        }
        
    def create(self, validated_data):
        """
        Custom method to create a new Chat instance. This method retrieves the specified
        assistant based on the provided assistant ID, sends the user's input message to 
        the assistant, and saves the chat instance with the assistant's response as output.

        Parameters:
            validated_data (dict): Data validated by the serializer to be used in creating
                a new Chat instance. Must include 'assistant_id' and 'input'.

        Returns:
            Chat: The newly created Chat instance, including the assistant's response to 
            the user's input.

        Raises:
            models.Assistant.DoesNotExist: If no assistant is found matching the provided
                assistant_id in validated_data.
        """
        # Extract the assistant_id and use it to retrieve the Assistant instance
        assistant_id = validated_data.pop('assistant_id')
        assistant = Assistant.objects.get(id=assistant_id)

        # Use the assistant's OpenAI ID to send the user's input and obtain a response
        output = send_message_to_assistant(assistant.openai_id, validated_data["input"])

        # Create and save the new Chat instance with both input and obtained output
        chat = Chat(assistant=assistant, **validated_data, output=output)
        chat.save()
        return chat
    
    
class UserSerializer(serializers.ModelSerializer):
    """
    A serializer for Django's User model.

    This serializer is responsible for serializing and deserializing User objects. It includes
    custom behavior for securely handling passwords during user creation. Specifically, it ensures
    that passwords are properly hashed before being stored in the database. Additionally, this serializer
    automatically generates an authentication token for each new user, facilitating token-based
    authentication mechanisms.
    
    Attributes:
        Meta.model: Specifies the Django model to be serialized.
        Meta.fields: Defines the model fields to be included in the serialized output.
        Meta.extra_kwargs: Provides additional options for configuring the serializer behavior. In this
                           case, it sets the password field to "write_only" to ensure it is not included
                           in the serialized representation sent to clients.
    """

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Creates a new User instance.

        Overridden to ensure that the user's password is hashed prior to storing it in the database.
        After creating the user, it generates an authentication token for the user.

        Parameters:
            validated_data (dict): The data validated by the serializer, based on input provided
                                   by a client.

        Returns:
            User: The newly created User instance.

        Note:
            This method pops the "password" field from the validated data to handle it separately.
            After using `User.objects.create()` to create the User instance, it utilizes
            `set_password()` to hash the password. The user instance is then saved to the database.
            Finally, a new authentication token is created for the user using `Token.objects.create()`.
        """
        # Extract and remove the password from validated data
        password = validated_data.pop("password")
        # Create a new User instance with the validated data
        user = User.objects.create(**validated_data)
        # Hash the user's password
        user.set_password(password)
        # Save the user instance to the database with the hashed password
        user.save()
        # Generate an authentication token for the new user
        Token.objects.create(user=user)
        # Return the new user instance
        return user
    
    
class TokenSerializer(serializers.Serializer):
    """
    Serializer for handling user authentication requests.
    
    This serializer is responsible for validating user credentials (username and password).
    Upon successful authentication, it facilitates the generation of a token by adding
    the authenticated user to the validated data.
    """
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type":"password"}, trim_whitespace=False)
    
    def validate(self, attrs):
        """
        Validates user credentials.
        
        Attempts to authenticate the user with the provided username and password.
        If authentication is successful, the authenticated user object is added to attrs,
        allowing downstream processes to access the user. If authentication fails, it raises
        a ValidationError indicating that the credentials are incorrect.
        
        Parameters:
        - attrs (dict): The incoming data to validate, containing the username and password.
        
        Returns:
        - dict: The original attrs dict, updated to include the authenticated user object if authentication succeeds.
        
        Raises:
        - ValidationError: If authentication fails, indicating incorrect credentials.
        """
        username = attrs.get("username")
        password = attrs.get("password")
        # Authenticating user against the database
        user = authenticate(request=self.context.get("request"), username=username, password=password)
        if not user:
            # Authentication failed
            msg = "Credentials are not provided correctly."
            raise serializers.ValidationError(msg, code="authentication")
        # Authentication successful, adding user to attrs
        attrs["user"] = user
        return attrs
