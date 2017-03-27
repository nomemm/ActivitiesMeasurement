from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from activities.models import Activity
from measurements.models import Measurement
from measurements.serializers import MeasurementSerializer
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'activities')

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ActivitySerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Activity
        fields = ('id', 'name', 'comments', 'measurements', 'user')

    def create(self, validated_data):
        measurements_data = validated_data.pop('measurements')
        activity = Activity.objects.create(**validated_data)
        for measurement_data in measurements_data:
            Measurement.objects.create(activity=activity, **measurement_data)
        return activity
