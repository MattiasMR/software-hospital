from rest_framework import serializers

class ReporteKpiSerializer(serializers.Serializer):
    """
    KPIs agregados para rangos de fechas.
    Definimos tipos de los dicts para validación y documentación automática.
    """
    porcentaje_ocupacion = serializers.FloatField()
    tiempos_muertos      = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Clave: idBox | Valor: minutos libres entre consultas"
    )
    uso_por_especialidad = serializers.DictField(
        child=serializers.IntegerField(),
        help_text="Clave: nombre especialidad | Valor: cantidad de consultas"
    )
    rango = serializers.DictField(
        child=serializers.CharField(),
        help_text='{"desde": "YYYY-MM-DD", "hasta": "YYYY-MM-DD"}'
    )


class BoxStatusSimpleSerializer(serializers.Serializer):
    idBox               = serializers.IntegerField()
    disponibilidad      = serializers.CharField()          # “Habilitado”, “Libre”, “En curso”…
    pasillo             = serializers.CharField()
    medicoAsignado      = serializers.CharField(allow_null=True)
    porcentajeOcupacion = serializers.IntegerField()
    medicosDelDia       = serializers.ListField(
                             child=serializers.CharField(), 
                             allow_empty=True
                         )


class ConsultaSerializer(serializers.Serializer):
    inicio  = serializers.CharField()
    fin     = serializers.CharField()
    estado  = serializers.CharField()


class TurnoSerializer(serializers.Serializer):
    medico               = serializers.CharField()
    especialidad         = serializers.CharField(allow_null=True)
    rango                = serializers.CharField()
    horasOcupadas        = serializers.FloatField()
    porcentajeOcupacion  = serializers.IntegerField()
    consultas            = ConsultaSerializer(many=True)

class BoxDetalleSerializer(serializers.Serializer):
    pasillo             = serializers.CharField()
    turnos   = TurnoSerializer(many=True)
    