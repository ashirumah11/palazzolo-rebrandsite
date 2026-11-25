from rest_framework import serializers
from .models import Admission, Fee


class FeeSerializer(serializers.ModelSerializer):
    formatted_amount = serializers.SerializerMethodField()

    class Meta:
        model = Fee
        fields = [
            'id',
            'course',
            'fee_type',
            'amount',
            'formatted_amount',
            'is_published',
            'note',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_formatted_amount(self, obj):
        return obj.formatted_amount


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'course',
            'applied_at',
            'status',
            'message',
        ]
        read_only_fields = ['id', 'applied_at']
