from django.test import TestCase
from activities.models import Activity
from activities.serializers import ActivitySerializer


class ActivityTestCase(TestCase):
    def setUp(self):
        pass

    def test_activitiy_is_saved_from_JSON(self):
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

        activity = ActivitySerializer.create(json)
        self.assertEqual(activity.owner, 0)
        self.assertEqual(activity.name, "testing json")
        self.assertEqual(len(activity.measurements), 2)

# TODO: add login tests
