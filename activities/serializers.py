from django.contrib.auth.models import User, Group
from activities.models import Activity
from measurements.models import Measurement
from measurements.serializers import MeasurementSerializer
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ActivitySerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Activity
        fields = ('id', 'name', 'comments', 'measurements')

    def create(self, validated_data):
        measurements_data = validated_data.pop('measurements')
        activity = Activity.objects.create(**validated_data)
        for measurement_data in measurements_data:
            Measurement.objects.create(activity=activity, **measurement_data)
        return activity
