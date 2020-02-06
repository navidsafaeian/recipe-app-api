from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        # the password should be write only.
        # it should not be serialized when get is called
        # we specify extra kwargs for each field
        # list of accepted args for can be found under core argument section of
        # https://www.django-rest-framework.org/api-guide/fields/
        # for password field, args under serializer.CharField are also valid
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # create is called when we use the CreateAPI view
    # which takes a POST request to create a user
    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        # we have to upate password separately from other data
        # so pop the unencrypted password from validated_data if it was updated or return none as default if it was skipped for updating
        password = validated_data.pop('password', None)
        # update all other fields in the model apart from password
        user = super().update(instance, validated_data)
        # update encrypted password if provided by user
        if password:
            user.set_password(password)
            user.save()

        return user    

"""Serializer can also be used without a model Since this is not a model, we inherit from serializers.Serializer This is for an API that will get some data from user, validate it and return some value."""
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    # create fields to get data for authentication
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    # override validate method and raise exception if invalid
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            # we use gettext to enable language tranlation for this text
            msg = _('Unable to authenticate with provided credentials')
            # pass correct code will raise the relavant http status code
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
