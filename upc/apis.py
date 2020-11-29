from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, MachineSerializer, MixingSerializer, QuestionSerializer, SpeedSerializer, \
    SubstrateSerializer, ApplicationTypeSerializer, ConditionSerialier, LayerSerializer, TempSerializer, \
    InsulationSerializer
from .models import Product, Machine, MixingChamber, ApplicationType, Temperature, Questions, Speed_of_spray, \
    Substrate_type, Hose_insulation, Layer, Hose_condition, getPressureset, getABHostHeat
from pyexcel_xlsx import get_data as xlsx_get


class MakeModels(APIView):
    def get(self, request):
        data = xlsx_get("upc/django-model-try.xlsx")
        print(list(data))
        Product_sheet = list(data)[0]
        Machine_sheet = list(data)[1]
        Mixing_sheet = list(data)[2]
        Type_sheet = list(data)[3]
        Temp_sheet = list(data)[4]
        Speed_sheet = list(data)[5]
        Insulation_sheet = list(data)[6]
        Condition_sheet = list(data)[7]
        SubstrateType_sheet = list(data)[8]
        Layer_sheet = list(data)[9]
        ABYeildDensity_sheet = list(data)[11]
        Pressure_sheet = list(data)[12]

        data1 = data[Product_sheet]
        for products in data1:
            Product.objects.create(product_name=products[0])
        data2 = data[Machine_sheet]
        for machines in data2:
            Machine.objects.create(machine_name=machines[0])
        data3 = data[Mixing_sheet]
        for mixings in data3:
            MixingChamber.objects.create(mixing_name=mixings[0])
        data4 = data[Type_sheet]
        for types in data4:
            ApplicationType.objects.create(app_type=types[0])
        data5 = data[Temp_sheet]
        for temps in data5:
            Temperature.objects.create(temp=temps[0])
        data6 = data[Speed_sheet]
        for speeds in data6:
            Speed_of_spray.objects.create(speed=speeds[0])
        data7 = data[Insulation_sheet]
        for insulations in data7:
            Hose_insulation.objects.create(insulation=insulations[0])
        data8 = data[Condition_sheet]
        for conditions in data8:
            Hose_condition.objects.create(condition=conditions[0])
        data9 = data[SubstrateType_sheet]
        for types in data9:
            Substrate_type.objects.create(type=types[0])
        data10 = data[Layer_sheet]
        for layers in data10:
            Layer.objects.create(number=layers[0], reduce=layers[1])
        data11 = data[ABYeildDensity_sheet]
        print(data11)
        for d in data11:
            print(d[0])
            getABHostHeat.objects.create(sprayer_forms=d[0],
                                         Ambient_temp=d[1], a_side_for_00=d[2],
                                         a_side_for_01=d[3], a_side_for_02=d[4], a_side_for_03=d[5], b_side_for_00=d[6],
                                         b_side_for_01=d[7], b_side_for_02=d[8], b_side_for_03=d[9],
                                         hose_heat_for_00=d[10], hose_heat_for_01=d[11], hose_heat_for_02=d[12],
                                         hose_heat_for_03=d[13], Y_for_00=d[14], Y_for_01=d[15], Y_for_02=d[16],
                                         Y_for_03=d[17], D_for_00=d[18], D_for_01=d[19], D_for_02=d[20], D_for_03=d[21])
        data12 = data[Pressure_sheet]
        for d in data12:
            getPressureset.objects.create(mixing=d[0],
                                          machine_Type=d[1], Pressure_for_wall=d[2],
                                          Pressure_for_ceiling=d[3])
        Q1 = Questions.objects.create(q="What type of foam are you spraying?")
        Q2 = Questions.objects.create(q="What kind of machine are you using?")
        Q3 = Questions.objects.create(q="What mixing chamber size are you using?")
        Q4 = Questions.objects.create(q="Are you spraying walls or ceilings?")
        Q5 = Questions.objects.create(q="What is the ambient temperature?")
        Q6 = Questions.objects.create(q="What is the substrate temperature?")
        Q7 = Questions.objects.create(q="What is the starting drum temperature?")
        Q8 = Questions.objects.create(q="What is the humidity level?")
        Q9 = Questions.objects.create(q="What is speed of spraying?")
        Q10 = Questions.objects.create(q="Is the hose well insulated?")
        Q11 = Questions.objects.create(q="Is hose in the sun, on hot asphalt,in the rain, or snow?")
        Q12 = Questions.objects.create(q="Substrate type?")
        Q13 = Questions.objects.create(q="How many layers will you spray?")

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Objects made successfully",
        }
        return Response(status_header)


class TechSupportQuestions(APIView):
    def get(self, request):
        l = [Product, Machine, MixingChamber, ApplicationType, Temperature, Temperature, Temperature, Temperature,
             Speed_of_spray, Hose_insulation, Hose_condition, Substrate_type, Layer]
        s = [ProductSerializer, MachineSerializer, MixingSerializer, ApplicationTypeSerializer, TempSerializer,
             TempSerializer, TempSerializer, TempSerializer, SpeedSerializer, InsulationSerializer, ConditionSerialier,
             SubstrateSerializer, LayerSerializer]
        data = []
        for i in range(13):
            q_objs = Questions.objects.get(id=(i + 1))
            options_objs = l[i].objects.all()

            demo = QuestionSerializer(q_objs).data
            xxx = s[i](options_objs, many=True).data

            ans = []
            for x in xxx:
                ans.append(list(x.values())[0])

            demo['options'] = ans
            data.append(demo)

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "questions received successfully",
            'data': data
        }

        return Response(status_header)

    def post(self, request):

        productname = request.data[0]['options']
        machinename = request.data[1]['options']
        mixingchamber = request.data[2]['options']
        applicationtype = request.data[3]['options']
        ambienttemp = request.data[4]['options']

        product_name = productname
        if len(request.data) > 5:
            substratetemp = request.data[5]['options']
            if substratetemp != ambienttemp:
                ambienttemp = substratetemp

        if applicationtype == 'wall':
            Pressure = getPressureset.objects.get(mixing=mixingchamber,
                                                  machine_Type=machinename).Pressure_for_wall
        else:
            Pressure = getPressureset.objects.get(mixing=mixingchamber,
                                                  machine_Type=machinename).Pressure_for_ceiling
        if mixingchamber == '-00':
            A_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).a_side_for_00
            B_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).b_side_for_00
            Hose_heat = getABHostHeat.objects.get(sprayer_forms=productname,
                                                  Ambient_temp=ambienttemp).hose_heat_for_00
            yield_per_set = getABHostHeat.objects.get(sprayer_forms=productname,
                                                      Ambient_temp=ambienttemp).Y_for_00
            core_density = getABHostHeat.objects.get(sprayer_forms=productname,
                                                     Ambient_temp=ambienttemp).D_for_00

        elif mixingchamber == '-01':
            A_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).a_side_for_01
            B_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).b_side_for_01
            Hose_heat = getABHostHeat.objects.get(sprayer_forms=productname,
                                                  Ambient_temp=ambienttemp).hose_heat_for_01
            yield_per_set = getABHostHeat.objects.get(sprayer_forms=productname,
                                                      Ambient_temp=ambienttemp).Y_for_01
            core_density = getABHostHeat.objects.get(sprayer_forms=productname,
                                                     Ambient_temp=ambienttemp).D_for_01
        elif mixingchamber == '-02':
            A_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).a_side_for_02
            B_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).b_side_for_02
            Hose_heat = getABHostHeat.objects.get(sprayer_forms=productname,
                                                  Ambient_temp=ambienttemp).hose_heat_for_02
            yield_per_set = getABHostHeat.objects.get(sprayer_forms=productname,
                                                      Ambient_temp=ambienttemp).Y_for_02
            core_density = getABHostHeat.objects.get(sprayer_forms=productname,
                                                     Ambient_temp=ambienttemp).D_for_02
        else:
            A_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).a_side_for_03
            B_heater = getABHostHeat.objects.get(sprayer_forms=productname,
                                                 Ambient_temp=ambienttemp).b_side_for_03
            Hose_heat = getABHostHeat.objects.get(sprayer_forms=productname,
                                                  Ambient_temp=ambienttemp).hose_heat_for_03
            yield_per_set = getABHostHeat.objects.get(sprayer_forms=productname,
                                                      Ambient_temp=ambienttemp).Y_for_03
            core_density = getABHostHeat.objects.get(sprayer_forms=productname,
                                                     Ambient_temp=ambienttemp).D_for_03

        if len(request.data) > 5:
            drumtemp = request.data[6]['options']
            humidity = request.data[7]['options']
            speed = request.data[8]['options']
            insulation = request.data[9]['options']
            condition = request.data[10]['options']
            substratetype = request.data[11]['options']
            layers = request.data[12]['options']
            if drumtemp == 45 and A_heater != "n/a":
                A_heater = int(A_heater) + 3
            elif drumtemp == '30' and A_heater != "n/a":
                A_heater = None
            if humidity > 50 and ambienttemp <= 85 and A_heater != "n/a":
                A_heater = int(A_heater) + 5
            if speed == 'fast' and Hose_heat != "n/a":
                Hose_heat = int(Hose_heat) + 3
            elif speed == 'slow' and Hose_heat != "n/a":
                Hose_heat = int(Hose_heat) - 2
            if insulation == 'Well Insulated' and Hose_heat != "n/a":
                Hose_heat = int(Hose_heat) - 2
            elif insulation == 'Poorly Insulated' and Hose_heat != "n/a":
                Hose_heat = int(Hose_heat) + 2
            if condition == 'Rain' or condition == 'Snow' and Hose_heat != "n/a":
                Hose_heat = int(Hose_heat) + 2
            elif condition == 'Sun' or condition == 'Hot asphalt' and Hose_heat != "n/a":
                Hose_heat = int(Hose_heat) - 2
            if substratetype == 'Concrete' and A_heater != "n/a" and B_heater != "n/a" and Hose_heat != "n/a":
                A_heater = int(A_heater) + 2
                B_heater = int(B_heater) + 2
                Hose_heat = int(Hose_heat) + 2
            elif substratetype == 'Metal' and A_heater != "n/a" and B_heater != "n/a" and Hose_heat != "n/a":
                A_heater = int(A_heater) + 3
                B_heater = int(B_heater) + 3
                Hose_heat = int(Hose_heat) + 3

            yield_per_set = int(yield_per_set) - (Layer.objects.get(number=layers).reduce) * (int(yield_per_set) / 100)

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "questions received successfully",
            'data': [{'Recommendation Settings for': product_name, 'A_Heater': A_heater, 'B_Heater': B_heater,
                      'Hose Heat': Hose_heat, 'Pressureset': Pressure, 'Expected Yield Per Set': yield_per_set,
                      'Expected Core Density': core_density}]
        }
        return Response(status_header)

