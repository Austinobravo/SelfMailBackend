from rest_framework import serializers
from .models import SelfMailModel

class FormattedDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        # Format the date as "Aug 20 2023, 15:30"
        formatted_date = value.strftime('%b %d %Y, %H:%M')
        return formatted_date

class SelfMailSerializer(serializers.ModelSerializer):
    formatted_date = FormattedDateTimeField(source='date_created')

    class Meta:
        model = SelfMailModel
        fields = ('id', 'date_created', 'formatted_date', 'from_mail', 'to_mail','subject', 'file', 'description')