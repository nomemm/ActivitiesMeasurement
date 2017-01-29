from django.contrib.auth.models import User, Group
from activities.models import Activity
from measurements.models import Measurement
from measurements.serializers import MeasurementSerializer
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    activities = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Activity.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups', 'activities')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class ActivitySerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)
    user = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Activity
        fields = ('id', 'name', 'comments', 'measurements', 'user')

    def create(self, validated_data):
        measurements_data = validated_data.pop('measurements')
        activity = Activity.objects.create(**validated_data)
        for measurement_data in measurements_data:
            Measurement.objects.create(activity=activity, **measurement_data)
        return activity
