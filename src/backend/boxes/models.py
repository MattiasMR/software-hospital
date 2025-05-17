from django.db import models

class DisponibilidadBox(models.Model):
    idDisponibilidadBox = models.AutoField(primary_key=True, db_column='idDisponibilidadBox')
    disponibilidad = models.CharField(max_length=50)  # "Habilitado" o "Inhabilitado"
    class Meta:
        db_table = 'DisponibilidadBox'
    def __str__(self):
        return self.disponibilidad

class Especialidad(models.Model):
    idEspecialidad = models.AutoField(primary_key=True, db_column='idEspecialidad')
    nombreEspecialidad = models.CharField(max_length=100)
    class Meta:
        db_table = 'Especialidad'
    def __str__(self):
        return self.nombreEspecialidad

class Jornada(models.Model):
    idJornada = models.AutoField(primary_key=True, db_column='idJornada')
    jornadaInicio = models.TimeField()
    jornadaFin    = models.TimeField()
    class Meta:
        db_table = 'Jornada'
    def __str__(self):
        return f"{self.jornadaInicio}–{self.jornadaFin}"

class Medico(models.Model):
    idMedico = models.AutoField(primary_key=True, db_column='idMedico')
    nombreCompleto = models.CharField(max_length=200)
    especialidad = models.ForeignKey('Especialidad', on_delete=models.PROTECT, db_column='idEspecialidad', related_name='medicos')
    jornada = models.ForeignKey('Jornada', on_delete=models.PROTECT, db_column='idJornada', related_name='medicos')
    class Meta:
        db_table = 'Medico'
    def __str__(self):
        return self.nombreCompleto

class Pasillo(models.Model):
    idPasillo = models.AutoField(primary_key=True, db_column='idPasillo')
    nombrePasillo = models.CharField(max_length=50)
    class Meta:
        db_table = 'Pasillo'
    def __str__(self):
        return self.nombrePasillo

class Box(models.Model):
    idBox = models.AutoField(primary_key=True, db_column='idBox')
    pasillo = models.ForeignKey('Pasillo', on_delete=models.PROTECT, db_column='idPasillo', related_name='boxes')
    disponibilidadBox = models.ForeignKey('DisponibilidadBox', on_delete=models.PROTECT, db_column='idDisponibilidadBox', related_name='boxes')
    especialidades = models.ManyToManyField('Especialidad', through='BoxEspecialidad', related_name='boxes')
    class Meta:
        db_table = 'Box'
    def __str__(self):
        return f"Box {self.idBox}"

class BoxEspecialidad(models.Model):
    box = models.ForeignKey('Box', on_delete=models.CASCADE, db_column='idBox')
    especialidad = models.ForeignKey('Especialidad', on_delete=models.CASCADE, db_column='idEspecialidad')
    class Meta:
        db_table = 'BoxEspecialidad'
        unique_together = ('box', 'especialidad')

class EstadoConsulta(models.Model):
    idEstadoConsulta = models.AutoField(primary_key=True, db_column='idEstadoConsulta')
    estadoConsulta = models.CharField(max_length=50) # "Ocupado", "Libre", "Cancelada", etc.
    class Meta:
        db_table = 'EstadoConsulta'
    def __str__(self):
        return self.estadoConsulta

class Consulta(models.Model):
    idConsulta = models.AutoField(primary_key=True, db_column='idConsulta')
    box = models.ForeignKey('Box', on_delete=models.CASCADE, db_column='idBox', related_name='consultas')
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE, db_column='idMedico', related_name='consultas')
    estadoConsulta = models.ForeignKey('EstadoConsulta', on_delete=models.PROTECT, db_column='idEstadoConsulta', related_name='consultas')
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin    = models.DateTimeField()
    class Meta:
        db_table = 'Consulta'
    def __str__(self):
        return f"Consulta {self.idConsulta}: Box {self.box_id} – Médico {self.medico_id}"

