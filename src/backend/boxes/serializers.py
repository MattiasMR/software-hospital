from rest_framework import serializers

class BoxStatusSimpleSerializer(serializers.Serializer):
    idBox               = serializers.IntegerField()
    numeroBox           = serializers.IntegerField()
    tipoBox             = serializers.CharField()
    disponibilidad      = serializers.CharField()
    pasillo             = serializers.CharField()
    medicoAsignado      = serializers.CharField(allow_null=True)
    porcentajeOcupacion = serializers.IntegerField()

class ReporteKpiSerializer(serializers.Serializer):
    porcentaje_ocupacion   = serializers.FloatField()
    tiempos_muertos        = serializers.DictField()
    uso_por_especialidad   = serializers.DictField()
    rango                  = serializers.DictField()