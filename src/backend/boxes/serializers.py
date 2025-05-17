from rest_framework import serializers

class BoxStatusSimpleSerializer(serializers.Serializer):
    idBox               = serializers.IntegerField()
    disponibilidad      = serializers.CharField()
    pasillo            = serializers.CharField()
    medicoAsignado     = serializers.CharField(allow_null=True)
    porcentajeOcupacion = serializers.IntegerField()

class ReporteKpiSerializer(serializers.Serializer):
    porcentaje_ocupacion   = serializers.FloatField()
    tiempos_muertos        = serializers.DictField()
    uso_por_especialidad   = serializers.DictField()
    rango                  = serializers.DictField()

class FranjaHorarioSerializer(serializers.Serializer):
    inicio        = serializers.CharField()
    fin           = serializers.CharField()
    medico        = serializers.CharField()
    especialidad  = serializers.CharField()
    estado        = serializers.CharField()

class BoxDetalleSerializer(serializers.Serializer):
    idBox               = serializers.IntegerField()
    pasillo             = serializers.CharField()
    franjas             = FranjaHorarioSerializer(many=True)
    porcentajeOcupacion = serializers.IntegerField()
