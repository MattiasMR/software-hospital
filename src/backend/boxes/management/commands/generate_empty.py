# boxes/management/commands/generate_data_empty.py

from __future__ import annotations

import random
from datetime import time
from typing import List

from django.core.management.base import BaseCommand
from django.db import transaction

from boxes.models import (
    Box,
    BoxEspecialidad,
    DisponibilidadBox,
    Especialidad,
    Jornada,
    Medico,
    Pasillo,
    EstadoConsulta,
)

DEFAULT_SEED = 42
BOXES_POR_PASILLO = 10

class Command(BaseCommand):
    help = "Genera solo la base vacía: especialidades, médicos, boxes, pasillos, sin consultas ni asignaciones."

    def add_arguments(self, parser):
        parser.add_argument("--seed", type=int, default=DEFAULT_SEED)

    def handle(self, *args, **opts):
        rng_seed: int = opts["seed"]
        random.seed(rng_seed)
        self.stdout.write(f"🔄  Generando base vacía (seed={rng_seed}) ...")

        with transaction.atomic():
            self._reset_tablas()
            especialidades = self._crea_catalogos_basicos()
            pasillos = self._crea_pasillos()
            boxes = self._crea_boxes(pasillos, especialidades)
            self._crea_medicos(especialidades)

        self.stdout.write(self.style.SUCCESS("✅ ¡Base vacía generada correctamente!"))

    def _reset_tablas(self):
        self.stdout.write("🧹  Limpiando tablas …")
        from boxes.models import Consulta
        Consulta.objects.all().delete()
        BoxEspecialidad.objects.all().delete()
        Box.objects.all().delete()
        Medico.objects.all().delete()
        Pasillo.objects.all().delete()
        DisponibilidadBox.objects.all().delete()
        Especialidad.objects.all().delete()
        Jornada.objects.all().delete()
        EstadoConsulta.objects.all().delete()

    def _crea_catalogos_basicos(self) -> List[Especialidad]:
        self.stdout.write("📚  Creando catálogos …")
        DisponibilidadBox.objects.create(disponibilidad="Habilitado")
        DisponibilidadBox.objects.create(disponibilidad="Inhabilitado")
        especialidades = [
            Especialidad.objects.create(nombreEspecialidad=n)
            for n in (
                "Cardiología", "Ginecología", "Pediatría", "Traumatología", "Neurocirugía",
                "Radiología", "Medicina General", "Dermatología", "Salud Mental"
            )
        ]
        Jornada.objects.bulk_create([
            Jornada(jornadaInicio=time(6, 0), jornadaFin=time(13, 0)),
            Jornada(jornadaInicio=time(13, 0), jornadaFin=time(22, 0)),
        ])
        EstadoConsulta.objects.bulk_create([
            EstadoConsulta(estadoConsulta="Pendiente"),
            EstadoConsulta(estadoConsulta="Cancelada"),
            EstadoConsulta(estadoConsulta="Completada"),
        ])
        return especialidades

    def _crea_pasillos(self) -> List[Pasillo]:
        pasillos = [
            Pasillo.objects.create(nombrePasillo=f"Pasillo {chr(65+i)}")
            for i in range(7)
        ]
        self.stdout.write(f"🚪  Pasillos creados: {len(pasillos)}")
        return pasillos

    def _crea_boxes(self, pasillos, especialidades) -> List[Box]:
        disp_hab = DisponibilidadBox.objects.get(disponibilidad="Habilitado")
        boxes: List[Box] = []
        numero_global = 1
        especialidad_general = Especialidad.objects.get(nombreEspecialidad="Medicina General")
        for pasillo in pasillos:
            for _ in range(BOXES_POR_PASILLO):
                box = Box.objects.create(
                    pasillo=pasillo,
                    disponibilidadBox=disp_hab,
                )
                # Solo asigna especialidades, no médicos ni consultas
                posibles = [e for e in especialidades if e != especialidad_general]
                extra_esps = random.sample(posibles, k=random.randint(1, 2))
                box_esps = [especialidad_general] + extra_esps
                box.especialidades.set(box_esps)
                box.numeroBox = numero_global  # type: ignore[attr-defined]
                numero_global += 1
                boxes.append(box)
        self.stdout.write(f"📦  Boxes generados: {len(boxes)}")
        return boxes

    def _crea_medicos(self, especialidades) -> List[Medico]:
        nombres = (
            "Fernanda Soto", "Javier Sánchez", "Josefa Rojas", "Camila Morales", "María González", "Carlos Muñoz",
            "Sofía Fernández", "Diego Ramírez", "Alejandra Ruiz", "Andrés Castro", "Valentina López", "Rodrigo Vargas",
            "Paula Martínez", "Tomás Gutiérrez", "Antonella Ríos", "Sebastián Herrera", "Gabriela Díaz", "Felipe Carrasco",
            "Martín Espinoza", "Isidora Pérez", "Ignacio Fuentes", "Daniela Castro", "Patricio Miranda", "Florencia Gallardo",
        )
        jornadas = list(Jornada.objects.all())
        medicos = [
            Medico(
                nombreCompleto=n,
                especialidad=random.choice(especialidades),
                jornada=random.choice(jornadas),
            )
            for n in nombres
        ]
        Medico.objects.bulk_create(medicos)
        self.stdout.write(f"🩺  Médicos generados: {len(medicos)}")
        return list(Medico.objects.all())
