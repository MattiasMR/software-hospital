from django.db import models
from django.db.models import CheckConstraint, Q, F, Index


# ────────────────────────────────
#   Disponibilidad del Box
# ────────────────────────────────
class DisponibilidadBox(models.Model):
    id = models.AutoField(primary_key=True, db_column="idDisponibilidadBox")

    class Estado(models.TextChoices):
        HABILITADO   = "Habilitado"
        INHABILITADO = "Inhabilitado"

    disponibilidad = models.CharField(
        max_length=15,
        choices=Estado.choices,
        unique=True,
        db_column="disponibilidad",
    )

    class Meta:
        db_table = "DisponibilidadBox"

    def __str__(self):
        return self.get_disponibilidad_display()


# ────────────────────────────────
#   Especialidad
# ────────────────────────────────
class Especialidad(models.Model):
    id = models.AutoField(primary_key=True, db_column="idEspecialidad")
    nombreEspecialidad = models.CharField(
        max_length=100,
        db_column="nombreEspecialidad",
    )

    class Meta:
        db_table = "Especialidad"

    def __str__(self):
        return self.nombreEspecialidad


# ────────────────────────────────
#   Jornada
# ────────────────────────────────
class Jornada(models.Model):
    id = models.AutoField(primary_key=True, db_column="idJornada")
    jornadaInicio = models.TimeField()
    jornadaFin    = models.TimeField()

    class Meta:
        db_table = "Jornada"
        constraints = [
            CheckConstraint(
                check=Q(jornadaFin__gt=F("jornadaInicio")),
                name="jornada_fin_gt_inicio",
            )
        ]
        indexes = [
            Index(fields=["jornadaInicio", "jornadaFin"]),
        ]

    def __str__(self):
        return f"{self.jornadaInicio}–{self.jornadaFin}"


# ────────────────────────────────
#   Médico
# ────────────────────────────────
class Medico(models.Model):
    id = models.AutoField(primary_key=True, db_column="idMedico")
    nombreCompleto = models.CharField(
        max_length=120,
        db_index=True,
        db_column="nombreCompleto",
    )
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.PROTECT,
        db_column="idEspecialidad",
        related_name="medicos",
    )
    jornada = models.ForeignKey(
        Jornada,
        on_delete=models.PROTECT,
        db_column="idJornada",
        related_name="medicos",
    )

    class Meta:
        db_table = "Medico"
        indexes = [
            Index(fields=["especialidad"]),
            Index(fields=["jornada"]),
        ]

    def __str__(self):
        return self.nombreCompleto


# ────────────────────────────────
#   Pasillo
# ────────────────────────────────
class Pasillo(models.Model):
    id = models.AutoField(primary_key=True, db_column="idPasillo")
    nombrePasillo = models.CharField(
        max_length=50,
        unique=True,
        db_column="nombrePasillo",
    )

    class Meta:
        db_table = "Pasillo"

    def __str__(self):
        return self.nombrePasillo


# ────────────────────────────────
#   Box
# ────────────────────────────────
class Box(models.Model):
    id = models.AutoField(primary_key=True, db_column="idBox")
    pasillo = models.ForeignKey(
        Pasillo,
        on_delete=models.PROTECT,
        db_column="idPasillo",
        related_name="boxes",
    )
    disponibilidadBox = models.ForeignKey(
        DisponibilidadBox,
        on_delete=models.PROTECT,
        db_column="idDisponibilidadBox",
        related_name="boxes",
    )
    especialidades = models.ManyToManyField(
        Especialidad,
        through="BoxEspecialidad",
        related_name="boxes",
    )

    class Meta:
        db_table = "Box"
        indexes = [
            Index(fields=["pasillo"]),
            Index(fields=["disponibilidadBox"]),
        ]

    def __str__(self):
        return f"Box {self.id}"


# ────────────────────────────────
#   Box ↔ Especialidad (M2M)
# ────────────────────────────────
class BoxEspecialidad(models.Model):
    id = models.AutoField(primary_key=True)
    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        db_column="idBox",
    )
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.CASCADE,
        db_column="idEspecialidad",
    )

    class Meta:
        db_table = "BoxEspecialidad"
        unique_together = ("box", "especialidad")
        indexes = [
            Index(fields=["especialidad"]),
        ]


# ────────────────────────────────
#   Estado de Consulta
# ────────────────────────────────
class EstadoConsulta(models.Model):
    id = models.AutoField(primary_key=True, db_column="idEstadoConsulta")

    class Estado(models.TextChoices):
        PENDIENTE  = "Pendiente"
        CANCELADA  = "Cancelada"
        CONFIRMADA = "Confirmada"

    estadoConsulta = models.CharField(
        max_length=15,
        choices=Estado.choices,
        unique=True,
        db_column="estadoConsulta",
    )

    class Meta:
        db_table = "EstadoConsulta"

    def __str__(self):
        return self.get_estadoConsulta_display()


# ────────────────────────────────
#   Consulta
# ────────────────────────────────
class Consulta(models.Model):
    id = models.AutoField(primary_key=True, db_column="idConsulta")
    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        db_column="idBox",
        related_name="consultas",
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        db_column="idMedico",
        related_name="consultas",
    )
    estadoConsulta = models.ForeignKey(
        EstadoConsulta,
        on_delete=models.PROTECT,
        db_column="idEstadoConsulta",
        related_name="consultas",
    )
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin    = models.DateTimeField()

    class Meta:
        db_table = "Consulta"
        constraints = [
            CheckConstraint(
                check=Q(fechaHoraFin__gt=F("fechaHoraInicio")),
                name="consulta_fin_gt_inicio",
            )
        ]
        indexes = [
            Index(fields=["fechaHoraInicio", "box"]),
            Index(fields=["fechaHoraInicio", "estadoConsulta"]),
            Index(fields=["medico"]),
        ]

    def __str__(self):
        return f"Consulta {self.id}: Box {self.box_id} – Médico {self.medico_id}"

class AsignacionTurno(models.Model):
    id = models.AutoField(primary_key=True, db_column="idAsignacionTurno")
    box = models.ForeignKey(
        Box,
        on_delete=models.CASCADE,
        db_column="idBox",
        related_name="asignaciones_turno",
    )
    medico = models.ForeignKey(
        Medico,
        on_delete=models.CASCADE,
        db_column="idMedico",
        related_name="asignaciones_turno",
    )
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin = models.DateTimeField()

    class Meta:
        db_table = "AsignacionTurno"
        constraints = [
            CheckConstraint(
                check=Q(fechaHoraFin__gt=F("fechaHoraInicio")),
                name="asignacion_turno_fin_gt_inicio",
            )
        ]
        indexes = [
            Index(fields=["fechaHoraInicio", "box"]),
            Index(fields=["medico"]),
        ]

    def __str__(self):
        return f"Turno {self.id}: Box {self.box_id} – Médico {self.medico_id}"