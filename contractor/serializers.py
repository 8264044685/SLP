from rest_framework import serializers
from slp_admin import models

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contractor
        fields = "__all__"


    def create(self, validated_data):
        print('\nValidated_data',validated_data)
        contra = models.Contractor.objects.create(
            name = validated_data['user_name'],
            email = validated_data['user_email'],
            contact = validated_data['user_contact'],
            password = validated_data['password'],
        )
        return contra
