from rest_framework import serializers 
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''
    Serialization for User that can be show in UserListView.
    '''

    class Meta:
        model = User
        fields = ('first_name', 
                'last_name',   
                'username',
                'email',
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
                )
        read_only_fields = ('balance', 'username')
    def update(self, instance, validated_data):
        '''
        Update and return an existing `User` instance, given the validated data.
        If user set accaunt = False, it can be hapened only once.
        in admin we can delete his profile. 
        '''
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance