from .models import Product, Machine, MixingChamber, ApplicationType, Temperature, Speed_of_spray, Substrate_type, \
    Hose_condition, Hose_insulation, Layer, Questions
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['q']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name']


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['machine_name']


class MixingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MixingChamber
        fields = ['mixing_name']


class ApplicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationType
        fields = ['app_type']


class TempSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ['temp']


class SpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speed_of_spray
        fields = ['speed']


class InsulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hose_insulation
        fields = ['insulation']


class ConditionSerialier(serializers.ModelSerializer):
    class Meta:
        model = Hose_condition
        fields = ['condition']


class SubstrateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substrate_type
        fields = ['type']


class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layer
        fields = ['number']
