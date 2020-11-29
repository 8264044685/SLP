from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=255)


class Machine(models.Model):
    machine_name = models.CharField(max_length=255)


class MixingChamber(models.Model):
    mixing_name = models.CharField(max_length=255)


class ApplicationType(models.Model):
    app_type = models.CharField(max_length=255)


class Temperature(models.Model):
    temp = models.IntegerField()


class Speed_of_spray(models.Model):
    speed = models.CharField(max_length=255)


class Hose_insulation(models.Model):
    insulation = models.CharField(max_length=255)


class Hose_condition(models.Model):
    condition = models.CharField(max_length=255)


class Substrate_type(models.Model):
    type = models.CharField(max_length=255)


class Layer(models.Model):
    number = models.IntegerField()
    reduce = models.IntegerField()


class Questions(models.Model):
    q = models.CharField(max_length=255)


class getABHostHeat(models.Model):
    sprayer_forms = models.CharField(max_length=255)
    Ambient_temp = models.CharField(max_length=255)
    a_side_for_00 = models.CharField(max_length=255)
    a_side_for_01 = models.CharField(max_length=255)
    a_side_for_02 = models.CharField(max_length=255)
    a_side_for_03 = models.CharField(max_length=255)
    b_side_for_00 = models.CharField(max_length=255)
    b_side_for_01 = models.CharField(max_length=255)
    b_side_for_02 = models.CharField(max_length=255)
    b_side_for_03 = models.CharField(max_length=255)
    hose_heat_for_00 = models.CharField(max_length=255)
    hose_heat_for_01 = models.CharField(max_length=255)
    hose_heat_for_02 = models.CharField(max_length=255)
    hose_heat_for_03 = models.CharField(max_length=255)
    Y_for_00 = models.CharField(max_length=255)
    Y_for_01 = models.CharField(max_length=255)
    Y_for_02 = models.CharField(max_length=255)
    Y_for_03 = models.CharField(max_length=255)
    D_for_00 = models.CharField(max_length=255)
    D_for_01 = models.CharField(max_length=255)
    D_for_02 = models.CharField(max_length=255)
    D_for_03 = models.CharField(max_length=255)


class getPressureset(models.Model):
    mixing = models.CharField(max_length=255)
    machine_Type = models.CharField(max_length=255)
    Pressure_for_wall = models.CharField(max_length=255, null=True)
    Pressure_for_ceiling = models.CharField(max_length=255, null=True)

