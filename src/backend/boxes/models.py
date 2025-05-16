from django.db import models

class DisponibilidadBox(models.Model):
    idDisponibilidadBox = models.BigAutoField(primary_key=True)
    disponibilidad      = models.CharField(max_length=100)

    class Meta:
        db_table = 'DisponibilidadBox'
        verbose_name = 'Disponibilidad Box'
        verbose_name_plural = 'Disponibilidades Box'

    def __str__(self):
        return self.disponibilidad


class TipoBox(models.Model):
    idTipoBox = models.BigAutoField(primary_key=True)
    tipoBox   = models.CharField(max_length=100)

    class Meta:
        db_table = 'TipoBox'
        verbose_name = 'Tipo Box'
        verbose_name_plural = 'Tipos Box'

    def __str__(self):
        return self.tipoBox

class Box(models.Model):
    idBox             = models.BigAutoField(primary_key=True)
    numeroBox         = models.IntegerField()
    tipoBox           = models.ForeignKey(
        TipoBox,
        on_delete=models.PROTECT,
        db_column='idTipoBox',
        related_name='boxes'
    )
    disponibilidadBox = models.ForeignKey(
        DisponibilidadBox,
        on_delete=models.PROTECT,
        db_column='idDisponibilidadBox',
        related_name='boxes'
    )

    class Meta:
        db_table = 'Box'
        verbose_name = 'Box'
        verbose_name_plural = 'Boxes'

    def __str__(self):
        return f"Box {self.numeroBox} – {self.tipoBox}"


class Especialidad(models.Model):
    idEspecialidad      = models.BigAutoField(primary_key=True)
    nombreEspecialidad  = models.CharField(max_length=100)

    class Meta:
        db_table = 'Especialidad'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def __str__(self):
        return self.nombreEspecialidad


class Jornada(models.Model):
    idJornada      = models.BigAutoField(primary_key=True)
    jornadaInicio  = models.TimeField()
    jornadaFin     = models.TimeField()

    class Meta:
        db_table = 'Jornada'
        verbose_name = 'Jornada'
        verbose_name_plural = 'Jornadas'

    def __str__(self):
        return f"{self.jornadaInicio} – {self.jornadaFin}"


class Medico(models.Model):
    idMedico        = models.BigAutoField(primary_key=True)
    nombreCompleto  = models.CharField(max_length=200)
    especialidad    = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        db_column='idEspecialidad',
        related_name='medicos'
    )
    jornada         = models.ForeignKey(
        Jornada,
        on_delete=models.PROTECT,
        db_column='idJornada',
        related_name='medicos'
    )

    class Meta:
        db_table = 'Medico'
        verbose_name = 'Médico'
        verbose_name_plural = 'Médicos'

    def __str__(self):
        return self.nombreCompleto


class EstadoConsulta(models.Model):
    idEstadoConsulta = models.BigAutoField(primary_key=True)
    estadoConsulta   = models.CharField(max_length=100)

    class Meta:
        db_table = 'EstadoConsulta'
        verbose_name = 'Estado Consulta'
        verbose_name_plural = 'Estados Consulta'

    def __str__(self):
        return self.estadoConsulta


class Consulta(models.Model):
    idConsulta      = models.BigAutoField(primary_key=True)
    box             = models.ForeignKey(
        Box,
        on_delete=models.PROTECT,
        db_column='idBox',
        related_name='consultas'
    )
    medico          = models.ForeignKey(
        Medico,
        on_delete=models.PROTECT,
        db_column='idMedico',
        related_name='consultas'
    )
    estadoConsulta  = models.ForeignKey(
        EstadoConsulta,
        on_delete=models.PROTECT,
        db_column='idEstadoConsulta',
        related_name='consultas'
    )
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin    = models.DateTimeField()

    class Meta:
        db_table = 'Consulta'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f"Consulta {self.idConsulta} – {self.box} con {self.medico}"
