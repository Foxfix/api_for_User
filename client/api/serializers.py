from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from rest_framework.serializers import ( 
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer, 
    SerializerMethodField,
    ValidationError,
    ) 

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class UserSerializer(serializers.ModelSerializer):
    '''
    Serialization for User that can be show in UserListView.
    '''

    class Meta:
        model = User
        fields = ('first_name', 
                'last_name',
                'passport_number', 
                'email',
                'balance', 
                )


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    Serialization for User Detail. 
    '''
    class Meta:
        model = User
        fields = ('first_name', 
                'last_name',
                'email',
                'balance',
                'username',
                'passport_number',
                'accaunt',
                )
        read_only_fields = ('balance', 'username', 'password',)

    def update(self, instance, validated_data):
        '''
        Update and return an existing `User` instance, given the validated data.
        '''
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.passport_number = validated_data.get('passport_number', instance.passport_number)
        instance.accaunt = validated_data.get('accaunt', instance.accaunt)
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    '''
    Serialization for User while created.
    '''
    passport_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 
                'last_name', 
                'passport_number', 
                'username', 
                'password', 
                'email',)
        extra_kwargs = {"password":
                            {"write_only": True}
                            } # password will not be shown in api

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError('This users email has already registered.')
        return data

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'])
        user.save()
        return user 

    


class UserLoginSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = EmailField(label='Email', allow_blank=True, required=False)
    class Meta:
        model = User
        fields = ('token',
                'username', 
                'password',
                'email')

        extra_kwargs = {"password":
                            {"write_only": True}
                            } # password will not be shown in api
    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username= data.get("username", None)
        password = data["password"]
        if not email and not username:
            raise ValidationError('A username or email is required to login.')
        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
            ).distinct()
        if user.exists() and user.count() == 1:
           user = user.first()
        else:
            raise ValidationError("This username/email is not valid.")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again..")

        # retrieve the jwt token 
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        data["token"] = token
        return data 


   