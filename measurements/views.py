from django.http import JsonResponse
from measurements.models import Measurement
from measurements.serializers import MeasurementSerializer

from rest_framework.views import APIView


class MeasurementsList(APIView):
    """
    List all measurements
    """

    def get(self, request, format=None):
        measurements = Measurement.objects.filter(activity__user=request.user.id)
        serializer = MeasurementSerializer(measurements, many=True)
        resp = {'measurements': (serializer.data)}
        return JsonResponse(resp)
