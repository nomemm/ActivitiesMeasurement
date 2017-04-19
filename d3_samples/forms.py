from django import forms
from django.utils.translation import ugettext_lazy as _

from dash.base import DashboardPluginFormBase

from measurements.models import Measurement

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'


class ChartForm(forms.Form, DashboardPluginFormBase):
    """Chart form for `ChartBasePlugin` plugin."""

    plugin_data_fields = [
        ("title", ""), ("data", ""),
    ]

    title = forms.CharField(label=_("Title"), required=True)
    possible_filters = set(i.name for i in Measurement.objects.only('name'))
    data = forms.ChoiceField(
        choices=[
            (i, i) for i in possible_filters
        ]
    )
