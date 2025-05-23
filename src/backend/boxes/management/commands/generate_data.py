# boxes/management/commands/generate_data.py

from __future__ import annotations

import random
from datetime import datetime, time, timedelta
from typing import List, Dict, Set

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from boxes.models import (
    Box,
    BoxEspecialidad,
    Consulta,
    DisponibilidadBox,
    Especialidad,
    EstadoConsulta,
    Jornada,
    Medico,
    Pasillo,
)

DEFAULT_SEED = 42
DEFAULT_DAYS = 31
BOXES_POR_PASILLO = 10
FRANJAS_HORAS = range(6, 22)  # 06:00-22:00

class Command(BaseCommand):
    help = "Genera datos de prueba realistas y sin solapes."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
        parser.add_argument("--seed", type=int, default=DEFAULT_SEED)

    def handle(self, *args, **opts):
        rng_seed: int = opts["seed"]
        n_days: int = opts["days"]

        random.seed(rng_seed)
        self.stdout.write(f"🔄  Generando datos de prueba (seed={rng_seed}, días={n_days}) ...")

        with transaction.atomic():
            self._reset_tablas()
            especialidades = self._crea_catalogos_basicos()
            pasillos = self._crea_pasillos()
            boxes = self._crea_boxes(pasillos, especialidades)
            medicos = self._crea_medicos(especialidades)
            self._crea_consultas(boxes, medicos, especialidades, n_days)

        self.stdout.write(self.style.SUCCESS("✅ ¡Datos de prueba generados correctamente!"))

    def _reset_tablas(self):
        self.stdout.write("🧹  Limpiando tablas …")
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
        disp_hab  = DisponibilidadBox.objects.create(disponibilidad="Habilitado")
        disp_inh  = DisponibilidadBox.objects.create(disponibilidad="Inhabilitado")
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
            EstadoConsulta(estadoConsulta="Confirmada"),  # Corregido
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
                disponibilidad = random.choices((disp_hab,), weights=(1.0,))[0]
                box = Box.objects.create(
                    pasillo=pasillo,
                    disponibilidadBox=disponibilidad,
                )
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

    def _crea_consultas(self, boxes, medicos, especialidades, n_days: int):
        estados = {
            e.estadoConsulta: e for e in EstadoConsulta.objects.all()
        }
        hoy = timezone.localdate()
        consultas_bulk: List[Consulta] = []

        id_salud_mental = next(e.id for e in especialidades if e.nombreEspecialidad == "Salud Mental")
        id_medicina_general = next(e.id for e in especialidades if e.nombreEspecialidad == "Medicina General")
        medicos_salud_mental = [m for m in medicos if m.especialidad_id == id_salud_mental]

        for offset in range(n_days):
            fecha = hoy + timedelta(days=offset)
            medico_horas_ocupadas: Dict[int, Set[int]] = {}
            box_horas_ocupadas: Dict[int, Set[int]] = {}

            for box in boxes:
                if box.disponibilidadBox.disponibilidad == "Inhabilitado":
                    continue
                box_esps = set(box.especialidades.values_list("id", flat=True))
                box_id = box.id
                if box_id not in box_horas_ocupadas:
                    box_horas_ocupadas[box_id] = set()

                for h in FRANJAS_HORAS:
                    hora_ini = time(h, 0)
                    hora_fin = time(h + 2, 0)
                    franja_key = h

                    # Evita que haya 2 médicos distintos en el mismo box/franja salvo si ambos son Salud Mental
                    medicos_en_franja = [c.medico_id for c in consultas_bulk
                                         if c.box_id == box_id and c.fechaHoraInicio.hour == h]

                    # Busca médicos válidos (que tengan especialidad del box o Medicina General y estén libres en esa franja)
                    medicos_validos = [
                        m for m in medicos
                        if (m.especialidad_id in box_esps or m.especialidad_id == id_medicina_general)
                        and m.jornada.jornadaInicio <= hora_ini
                        and m.jornada.jornadaFin >= hora_fin
                        and h not in medico_horas_ocupadas.get(m.id, set())
                    ]

                    if not medicos_validos:
                        continue

                    # Controla que no haya 2 médicos no Salud Mental en la misma franja y box
                    puede_asignar = True
                    if medicos_en_franja:
                        # Ya hay uno o más médicos en esa franja
                        # Permite solo si ambos son Salud Mental
                        for mid in medicos_en_franja:
                            med_existe = next((x for x in medicos if x.id == mid), None)
                            if med_existe and med_existe.especialidad_id != id_salud_mental:
                                # Ya hay un médico no salud mental, no asignar otro no salud mental
                                puede_asignar = False
                                break

                    if not puede_asignar:
                        continue

                    random.shuffle(medicos_validos)

                    medico = medicos_validos[0]

                    # Si ya hay médicos y este no es Salud Mental, no asignar
                    if medicos_en_franja and medico.especialidad_id != id_salud_mental:
                        continue

                    if random.random() < 0.5:
                        inicio_dt = timezone.make_aware(datetime.combine(fecha, hora_ini))
                        fin_dt = inicio_dt + timedelta(hours=2)
                        estado = (
                            estados["Pendiente"]
                            if random.random() < 0.3
                            else estados["Cancelada"]
                            if random.random() < 0.1
                            else estados["Confirmada"]
                        )
                        consultas_bulk.append(
                            Consulta(
                                box=box,
                                medico=medico,
                                estadoConsulta=estado,
                                fechaHoraInicio=inicio_dt,
                                fechaHoraFin=fin_dt,
                            )
                        )
                        medico_horas_ocupadas.setdefault(medico.id, set()).add(h)
                        box_horas_ocupadas[box_id].add(h)

        # Opcional: agregar manualmente algunos casos con 2 médicos Salud Mental en mismo turno (p. ej. primeros 10 boxes)
        boxes_10 = boxes[:10]
        dia = hoy
        franja_especial = 8  # 08:00 - 10:00
        hora_ini = time(franja_especial, 0)
        inicio_dt = timezone.make_aware(datetime.combine(dia, hora_ini))
        fin_dt = inicio_dt + timedelta(hours=2)
        estado = estados["Confirmada"]

        usados: Set[int] = set()
        for box in boxes_10:
            box_esps = set(box.especialidades.values_list("id", flat=True))
            if id_salud_mental not in box_esps:
                continue

            candidatos = [
                m for m in medicos_salud_mental
                if franja_especial not in [
                    c.fechaHoraInicio.hour
                    for c in consultas_bulk
                    if c.box_id == box.id and c.medico_id == m.id and c.fechaHoraInicio.date() == dia
                ] and m.id not in usados
            ]

            if len(candidatos) < 2:
                continue

            for medico in candidatos[:2]:
                consultas_bulk.append(
                    Consulta(
                        box=box,
                        medico=medico,
                        estadoConsulta=estado,
                        fechaHoraInicio=inicio_dt,
                        fechaHoraFin=fin_dt,
                    )
                )
                usados.add(medico.id)

        Consulta.objects.bulk_create(consultas_bulk, batch_size=1000)
        self.stdout.write(f"📈  Consultas generadas: {Consulta.objects.count()}")

        # --- Asegura KPIs para Camila Morales ---
        medico_cm = Medico.objects.filter(nombreCompleto="Camila Morales").first()
        if medico_cm:
            box = Box.objects.first()
            if box:
                for i in range(5):
                    inicio = timezone.make_aware(datetime.combine(hoy + timedelta(days=i), time(10, 0)))
                    fin = inicio + timedelta(hours=1)
                    Consulta.objects.create(
                        box=box,
                        medico=medico_cm,
                        estadoConsulta=estados["Confirmada"],
                        fechaHoraInicio=inicio,
                        fechaHoraFin=fin,
                    )
                    
