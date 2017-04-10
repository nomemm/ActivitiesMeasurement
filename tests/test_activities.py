from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from activities.models import Activity
from activities.views import ActivityList
from measurements.models import Measurement

from activities.serializers import ActivitySerializer


class ActivityTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('testingUser')

    def createActivity(self):
        activity = Activity()
        activity.name = 'test from function'
        activity.user = User.objects.get_by_natural_key('testingUser')
        activity.save()
        return activity

    # view tests:
    def test_activitylist(self):
        """
            Test that this view will parse incoming
            multi-activity-containing JSON, check if
            it is correct and save all activities.
        """
        w = self.createActivity()
        url = reverse("activities")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200, 'reponse is not 200')
        self.assertEqual(w.name, 'test from function')

    # serializers tests:
    def test_activitiy_serializer_saved_from_JSON(self):
        """
            Test that serializer will take activity data
            and save it. Take into account measurements save!
        """
        json = {
            "activities": [
                {
                    "owner": "0",
                    "name": "testing json",
                    "measurements": [{
                        "name": "time spent",
                        "type": "int",
                        "value": "10"
                    },
                        {
                            "name": "lines of code was written",
                            "type": "int",
                            "value": "20"
                        }]
                }, {
                    "owner": "0",
                    "name": "testing json 2",
                    "measurements": [{
                        "name": "time spent",
                        "type": "int",
                        "value": "10"
                    }]
                }
            ]
        }

        for data in json['activities']:
            data['user'] = User.objects.get_by_natural_key('testingUser').id
            measurements_amount = len(Measurement.objects.all())
            serializer = ActivitySerializer(data=data)
            self.assertEqual(serializer.is_valid(), True,
                             'serializer is invalid')
            serializer.save()
            self.assertEqual(
                measurements_amount,
                Measurement.objects.count()-len(data['measurements']),
                'not all measurements were created'
            )

    def test_activity_is_not_saved_without_user(self):
        pass
# TODO: add login tests
