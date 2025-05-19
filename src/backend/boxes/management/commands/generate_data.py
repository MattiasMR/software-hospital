# boxes/management/commands/generate_data.py
from __future__ import annotations

import random
from datetime import datetime, time, timedelta
from typing import List

from django.conf import settings
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

# Configurables por flags ──────────────────────────────────────────────
DEFAULT_SEED = 42
DEFAULT_DAYS = 7
BOXES_POR_PASILLO = 8
FRANJAS_HORAS = range(8, 22)  # 08:00-22:00


class Command(BaseCommand):
    help = "Genera datos de prueba realistas con restricciones por médico y box."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days", type=int, default=DEFAULT_DAYS,
            help=f"Días hacia adelante a generar (default {DEFAULT_DAYS})",
        )
        parser.add_argument(
            "--seed", type=int, default=DEFAULT_SEED,
            help=f"Semilla del RNG para tener datos reproducibles (default {DEFAULT_SEED})",
        )

    # ──────────────────────────────────────────────────────────────────
    def handle(self, *args, **opts):
        rng_seed: int = opts["seed"]
        n_days: int = opts["days"]

        random.seed(rng_seed)
        self.stdout.write(
            f"🔄  Generando datos de prueba (seed={rng_seed}, días={n_days}) ..."
        )

        with transaction.atomic():
            self._reset_tablas()
            especialidades = self._crea_catalogos_basicos()
            pasillos = self._crea_pasillos()
            boxes = self._crea_boxes(pasillos, especialidades)
            medicos = self._crea_medicos(especialidades)
            self._crea_consultas(boxes, medicos, n_days)

        self.stdout.write(
            self.style.SUCCESS("✅ ¡Datos de prueba generados correctamente!")
        )

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _reset_tablas(self):
        """Borra TODO lo dependiente; orden importa por FK."""
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

    # ------------------------------------------------------------------
    def _crea_catalogos_basicos(self) -> List[Especialidad]:
        self.stdout.write("📚  Creando catálogos …")

        disp_hab  = DisponibilidadBox.objects.create(disponibilidad="Habilitado")
        disp_inh  = DisponibilidadBox.objects.create(disponibilidad="Inhabilitado")
        _ = (disp_hab, disp_inh)  # noqa: F841 sólo para dejar claro que se usan

        especialidades = [
            Especialidad.objects.create(nombreEspecialidad=n)
            for n in ("Cardiología", "Ginecología", "Pediatría", "Traumatología")
        ]

        # Dos turnos de 6 h
        Jornada.objects.bulk_create(
            [
                Jornada(jornadaInicio=time(8, 0),  jornadaFin=time(14, 0)),
                Jornada(jornadaInicio=time(14, 0), jornadaFin=time(22, 0)),
            ]
        )

        EstadoConsulta.objects.bulk_create(
            [
                EstadoConsulta(estadoConsulta="Pendiente"),
                EstadoConsulta(estadoConsulta="Cancelada"),
                EstadoConsulta(estadoConsulta="Completada"),
            ]
        )

        return especialidades

    # ------------------------------------------------------------------
    def _crea_pasillos(self) -> List[Pasillo]:
        pasillos = [
            Pasillo.objects.create(nombrePasillo=f"Pasillo {chr(65+i)}")
            for i in range(4)
        ]
        self.stdout.write(f"🚪  Pasillos creados: {len(pasillos)}")
        return pasillos

    # ------------------------------------------------------------------
    def _crea_boxes(self, pasillos, especialidades) -> List[Box]:
        disp_hab = DisponibilidadBox.objects.get(disponibilidad="Habilitado")
        disp_inh = DisponibilidadBox.objects.get(disponibilidad="Inhabilitado")

        boxes: List[Box] = []
        numero_global = 1

        for pasillo in pasillos:
            for _ in range(BOXES_POR_PASILLO):
                disponibilidad = random.choices(
                    (disp_hab, disp_inh), weights=(0.85, 0.15)
                )[0]
                box = Box.objects.create(
                    pasillo=pasillo,
                    disponibilidadBox=disponibilidad,
                )
                # muchas-a-muchas
                box_esps = random.sample(
                    especialidades, k=random.randint(1, 2)
                )
                box.especialidades.set(box_esps)

                # número correlativo visible al front
                box.numeroBox = numero_global  # type: ignore[attr-defined]
                numero_global += 1

                boxes.append(box)

        self.stdout.write(f"📦  Boxes generados: {len(boxes)}")
        return boxes

    # ------------------------------------------------------------------
    def _crea_medicos(self, especialidades) -> List[Medico]:
        nombres = (
            "Fernanda Soto", "Javier Sánchez", "Josefa Rojas", "Camila Morales",
            "María González", "Carlos Muñoz", "Sofía Fernández", "Diego Ramírez",
            "Alejandra Ruiz", "Andrés Castro"
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
        return list(Medico.objects.all())  # con IDs asignados

    # ------------------------------------------------------------------
    def _crea_consultas(self, boxes, medicos, n_days: int):
        estados = {
            e.estadoConsulta: e for e in EstadoConsulta.objects.all()
        }
        hoy = timezone.localdate()
        consultas_bulk: List[Consulta] = []

        for offset in range(n_days):
            fecha = hoy + timedelta(days=offset)

            for box in boxes:
                if box.disponibilidadBox.disponibilidad == "Inhabilitado":
                    continue

                box_esps = list(box.especialidades.all())
                horas_medico: dict[int, List[int]] = {}

                for h in FRANJAS_HORAS:
                    hora_ini = time(h, 0)
                    hora_fin = time(h + 1, 0)

                    # Médicos con especialidad compatible y turno activo
                    medicos_validos = [
                        m
                        for m in medicos
                        if m.especialidad in box_esps
                        and m.jornada.jornadaInicio <= hora_ini
                        and m.jornada.jornadaFin >= hora_fin
                    ]
                    if not medicos_validos:
                        continue

                    random.shuffle(medicos_validos)
                    for medico in medicos_validos:
                        lista = horas_medico.setdefault(medico.id, [])
                        # máx 3 consultas totales y no más de 2 consecutivas
                        if len(lista) >= 3:
                            continue
                        if len(lista) >= 2 and h - 1 in lista and h - 2 in lista:
                            continue

                        # prob ≈ 30 % de generar consulta
                        if random.random() < 0.3:
                            inicio_dt = timezone.make_aware(
                                datetime.combine(fecha, hora_ini)
                            )
                            fin_dt = inicio_dt + timedelta(hours=1)

                            estado = (
                                estados["Pendiente"]
                                if random.random() < 0.3
                                else estados["Cancelada"]
                                if random.random() < 0.1
                                else estados["Completada"]
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
                            lista.append(h)
                            break  # sólo un médico por franja

        Consulta.objects.bulk_create(consultas_bulk, batch_size=1000)
        self.stdout.write(
            f"📈  Consultas generadas: {Consulta.objects.count()}"
        )
