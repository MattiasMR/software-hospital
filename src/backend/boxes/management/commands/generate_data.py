from django.core.management.base import BaseCommand
from django.utils import timezone
from boxes.models import (
    Box, TipoBox, DisponibilidadBox, Especialidad, Pasillo,
    Medico, EstadoConsulta, Jornada, Consulta
)
from datetime import datetime, timedelta, time
import random

class Command(BaseCommand):
    help = "Genera datos de prueba: catálogos, médicos, boxes, y consultas para varios días."

    def handle(self, *args, **options):
        self.stdout.write("⚠️  Esto eliminará todos los datos previos (Boxes, Médicos, Consultas, etc.)")
        confirm = input("¿Seguro que quieres continuar? (sí/no): ")
        if confirm.lower() not in ("sí", "si", "yes", "y"):
            self.stdout.write("Cancelado.")
            return

        # 1. Elimina todos los datos relevantes (orden seguro)
        Consulta.objects.all().delete()
        Box.objects.all().delete()
        Medico.objects.all().delete()
        Pasillo.objects.all().delete()
        TipoBox.objects.all().delete()
        DisponibilidadBox.objects.all().delete()
        Especialidad.objects.all().delete()
        Jornada.objects.all().delete()
        EstadoConsulta.objects.all().delete()

        # 2. Catálogos base
        tipos = [TipoBox.objects.create(tipoBox=nombre) for nombre in ['General', 'Especial']]
        disponibilidades = [DisponibilidadBox.objects.create(disponibilidad=n) for n in ['Libre', 'Ocupado', 'Inhabilitado']]
        especialidades = [Especialidad.objects.create(nombreEspecialidad=n) for n in ['Cardiología', 'Ginecología', 'Pediatría', 'Traumatología']]
        jornadas = [Jornada.objects.create(jornadaInicio=ini, jornadaFin=fin) for ini, fin in [
            ("08:00", "12:00"), ("12:00", "16:00"), ("16:00", "20:00")]]
        estados = [
            EstadoConsulta.objects.create(estadoConsulta=n)
            for n in ['Ocupado', 'Libre', 'Inhabilitado', 'Pendiente', 'Confirmada', 'Cancelada']
        ]

        # 3. Pasillos
        pasillos = [Pasillo.objects.create(nombrePasillo=f"Pasillo {chr(65+i)}") for i in range(4)]  # Pasillo A-D

        # 4. Médicos
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

        # 5. Boxes (6 por pasillo)
        boxes = []
        for pasillo in pasillos:
            for i in range(6):
                dispo = random.choice(disponibilidades)
                box = Box.objects.create(
                    tipoBox=random.choice(tipos),
                    disponibilidadBox=dispo,
                    pasillo=pasillo,
                )
                # Relacionar con algunas especialidades
                box.especialidades.set(random.sample(especialidades, k=random.randint(1, len(especialidades))))
                boxes.append((box, dispo.disponibilidad))  # Guardamos disponibilidad para el siguiente paso

        # 6. Consultas: Para N días, todos los boxes habilitados, franjas de 1h, médicos rotando
        N_DIAS = 7
        horas = [(8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18)]
        hoy = timezone.localdate()
        for day in range(N_DIAS):
            fecha = hoy + timedelta(days=day)
            for box, dispo in boxes:
                # Si el box está inhabilitado, no generar consultas ni asignar médicos
                if dispo == "Inhabilitado":
                    continue
                for h_ini, h_fin in horas:
                    inicio = datetime.combine(fecha, time(h_ini, 0))
                    fin = datetime.combine(fecha, time(h_fin, 0))
                    estado = random.choice([e for e in estados if e.estadoConsulta in ["Ocupado", "Libre"]])
                    medico = random.choice(medicos) if estado.estadoConsulta == "Ocupado" else None
                    Consulta.objects.create(
                        box=box,
                        medico=medico,
                        estadoConsulta=estado,
                        fechaHoraInicio=inicio,
                        fechaHoraFin=fin
                    )