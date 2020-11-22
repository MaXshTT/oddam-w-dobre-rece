from rest_framework import serializers

from .models import Category, Donation, Institution


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donation
        fields = '__all__'


class InstitutionSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    kind = serializers.CharField(source='get_kind_display')

    class Meta:
        model = Institution
        fields = '__all__'
