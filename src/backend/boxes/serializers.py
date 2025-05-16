from rest_framework import serializers
from .models import Box, DisponibilidadBox, TipoBox, Medico, Consulta, EstadoConsulta

class DisponibilidadBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadBox
        fields = ('idDisponibilidadBox', 'disponibilidad')

class TipoBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoBox
        fields = ('idTipoBox', 'tipoBox')

class BoxStatusSerializer(serializers.ModelSerializer):
    tipoBox         = TipoBoxSerializer(read_only=True)
    disponibilidad  = DisponibilidadBoxSerializer(source='disponibilidadBox', read_only=True)

    class Meta:
        model = Box
        fields = ('idBox', 'numeroBox', 'tipoBox', 'disponibilidad')

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ('idMedico', 'nombreCompleto')

class EstadoConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoConsulta
        fields = ('idEstadoConsulta', 'estadoConsulta')

class ConsultaDetailSerializer(serializers.ModelSerializer):
    medico         = MedicoSerializer(read_only=True)
    estadoConsulta = EstadoConsultaSerializer(read_only=True)

    class Meta:
        model = Consulta
        fields = (
            'idConsulta',
            'medico',
            'estadoConsulta',
            'fechaHoraInicio',
            'fechaHoraFin'
        )

class BoxDetailSerializer(serializers.ModelSerializer):
    tipoBox        = TipoBoxSerializer(read_only=True)
    disponibilidad = DisponibilidadBoxSerializer(source='disponibilidadBox', read_only=True)
    consultas      = ConsultaDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Box
        fields = (
            'idBox',
            'numeroBox',
            'tipoBox',
            'disponibilidad',
            'consultas'
        )
