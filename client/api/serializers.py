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


class UserSerializer(serializers.ModelSerializer):
    '''
    Serialization for User that can be show in UserListView.
    '''

    class Meta:
        model = User
        fields = ('first_name', 
                'last_name', 
                'email',
                'balance',
                )


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    Serialization for User Detail. Used nested relationships.
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
                'password',
                )
        read_only_fields = ('balance', 'username')
    def update(self, instance, validated_data):
        '''
        Update and return an existing `User` instance, given the validated data.
        '''
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.passport_number = validated_data.get('passport_number', instance.passport_number)
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
    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        passport_number = validated_data['passport_number']
        username = validated_data['username']
        password = validated_data['password']
        user_obj = User(
            username = username,)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



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
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # payload = jwt_payload_handler(user_obj)
        # token = jwt_encode_handler(payload)
        data["token"] = "SOME RANDOM TOKEN"
        return data 


   