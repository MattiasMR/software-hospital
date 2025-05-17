from django.core.management.base import BaseCommand
from django.utils import timezone
from boxes.models import (
    Box, Especialidad, Pasillo, Medico, EstadoConsulta, Jornada, Consulta,
    DisponibilidadBox, BoxEspecialidad
)
from datetime import datetime, timedelta, time
import random

class Command(BaseCommand):
    help = "Genera datos de prueba realistas con restricciones por médico y box"

    def handle(self, *args, **options):
        self.stdout.write("⚠️  Esto eliminará todos los datos previos.")
        Consulta.objects.all().delete()
        BoxEspecialidad.objects.all().delete()
        Box.objects.all().delete()
        Medico.objects.all().delete()
        Pasillo.objects.all().delete()
        DisponibilidadBox.objects.all().delete()
        Especialidad.objects.all().delete()
        Jornada.objects.all().delete()
        EstadoConsulta.objects.all().delete()
        self.stdout.write("🔄️  Generando datos.")
        # Catálogos base
        disp_hab = DisponibilidadBox.objects.create(disponibilidad='Habilitado')
        disp_inh = DisponibilidadBox.objects.create(disponibilidad='Inhabilitado')
        especialidades = [Especialidad.objects.create(nombreEspecialidad=n) for n in [
            'Cardiología', 'Ginecología', 'Pediatría', 'Traumatología']]
        jornadas = [
            Jornada.objects.create(jornadaInicio=time(8,0), jornadaFin=time(14,0)),
            Jornada.objects.create(jornadaInicio=time(14,0), jornadaFin=time(22,0)),
        ]
        estados = {
            "Pendiente": EstadoConsulta.objects.create(estadoConsulta="Pendiente"),
            "Cancelada": EstadoConsulta.objects.create(estadoConsulta="Cancelada"),
            "Completada": EstadoConsulta.objects.create(estadoConsulta="Completada"),
        }

        pasillos = [Pasillo.objects.create(nombrePasillo=f"Pasillo {chr(65+i)}") for i in range(4)]
        boxes = []
        for pasillo in pasillos:
            for i in range(8):
                disponibilidad = random.choices([disp_hab, disp_inh], weights=[0.85, 0.15])[0]
                box = Box.objects.create(
                    pasillo=pasillo,
                    disponibilidadBox=disponibilidad,
                )
                box_esps = random.sample(especialidades, k=random.randint(1, 2))
                box.especialidades.set(box_esps)
                boxes.append(box)
        habilitados = [b for b in boxes if b.disponibilidadBox.disponibilidad == "Habilitado"] # debug
        print("Boxes habilitados:", len(habilitados)) # debug
        print("Boxes inhabilitados:", len(boxes) - len(habilitados)) # debug
        nombres = [
            "Fernanda Soto", "Javier Sánchez", "Josefa Rojas", "Camila Morales", "María González",
            "Carlos Muñoz", "Sofía Fernández", "Diego Ramírez", "Alejandra Ruiz", "Andrés Castro"
        ]
        medicos = []
        for nombre in nombres:
            especialidad = random.choice(especialidades)
            jornada = random.choice(jornadas)
            medico = Medico.objects.create(
                nombreCompleto=nombre,
                especialidad=especialidad,
                jornada=jornada
            )
            medicos.append(medico)

        N_DIAS = 7
        hoy = timezone.localdate()
        for day in range(N_DIAS):
            fecha = hoy + timedelta(days=day)
            for box in boxes:
                if box.disponibilidadBox.disponibilidad == 'Inhabilitado':
                    continue
                box_esps = list(box.especialidades.all())
                consultas_box_medico = {}  # (medico_id) -> [horas asignadas]

                for h in range(8, 22):
                    hora_inicio = time(h, 0)
                    hora_fin = time(h+1, 0)
                    # Médicos con especialidad compatible y jornada activa en esa hora
                    medicos_validos = [
                        m for m in medicos
                        if m.especialidad in box_esps
                        and m.jornada.jornadaInicio <= hora_inicio
                        and m.jornada.jornadaFin >= hora_fin
                    ]
                    random.shuffle(medicos_validos)
                    for medico in medicos_validos:
                        lista = consultas_box_medico.setdefault(medico.idMedico, [])
                        # Limita a 3 consultas totales y no más de 2 seguidas
                        if len(lista) >= 3:
                            continue
                        if len(lista) >= 2 and h-1 in lista and h-2 in lista:
                            continue  # Ya tiene 2 consecutivas previas
                        # 30% probabilidad de consulta
                        if (random.random() < 0.8 and len(Consulta.objects.filter(box=box)) < 5) or (random.random() < 0.4 and len(Consulta.objects.filter(box=box)) < 14):
                            inicio_dt = timezone.make_aware(datetime.combine(fecha, hora_inicio))
                            fin_dt = timezone.make_aware(datetime.combine(fecha, hora_fin))
                            # Estado
                            if random.random() < 0.3:
                                estado = estados["Pendiente"]
                            elif random.random() < 0.1:
                                estado = estados["Cancelada"]
                            else:
                                estado = estados["Completada"]
                            Consulta.objects.create(
                                box=box,
                                medico=medico,
                                estadoConsulta=estado,
                                fechaHoraInicio=inicio_dt,
                                fechaHoraFin=fin_dt
                            )
                            lista.append(h)
                            break  # Solo un médico por franja
        self.stdout.write(self.style.SUCCESS("✅ ¡Datos de prueba generados correctamente con restricciones!"))
