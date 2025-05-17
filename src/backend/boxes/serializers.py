from rest_framework import serializers
from .models import (
    Box, DisponibilidadBox, TipoBox,
    Medico, Consulta, EstadoConsulta, Pasillo
)

class DisponibilidadBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadBox
        fields = ('idDisponibilidadBox', 'disponibilidad')

class TipoBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoBox
        fields = ('idTipoBox', 'tipoBox')

class PasilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasillo
        fields = ('idPasillo', 'nombrePasillo')

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ('idMedico', 'nombreCompleto')

class EstadoConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoConsulta
        fields = ('idEstadoConsulta', 'estadoConsulta')

class BoxStatusSerializer(serializers.ModelSerializer):
    tipoBox           = TipoBoxSerializer(read_only=True)
    disponibilidadBox = DisponibilidadBoxSerializer(read_only=True)
    pasillo           = PasilloSerializer(read_only=True)
    medico            = MedicoSerializer(read_only=True)

    class Meta:
        model  = Box
        fields = (
            'idBox',
            'tipoBox',
            'disponibilidadBox',
            'pasillo',
            'medico',
        )

class ConsultaDetailSerializer(serializers.ModelSerializer):
    medico         = MedicoSerializer(read_only=True)
    estadoConsulta = EstadoConsultaSerializer(read_only=True)

    class Meta:
        model  = Consulta
        fields = (
            'idConsulta',
            'medico',
            'estadoConsulta',
            'fechaHoraInicio',
            'fechaHoraFin',
        )

class BoxDetailSerializer(serializers.ModelSerializer):
    tipoBox        = TipoBoxSerializer(read_only=True)
    disponibilidad = DisponibilidadBoxSerializer(read_only=True)
    pasillo        = PasilloSerializer(read_only=True)
    consultas      = ConsultaDetailSerializer(many=True, read_only=True)

    class Meta:
        model  = Box
        fields = (
            'idBox',
            'tipoBox',
            'disponibilidad',
            'pasillo',
            'consultas',
        )
