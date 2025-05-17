import random
from django.core.management.base import BaseCommand
from boxes.models import (
    Box,
    TipoBox,
    DisponibilidadBox,
    Especialidad,
    Pasillo,
    Medico,
    EstadoConsulta,
)

class Command(BaseCommand):
    help = "Genera datos de prueba: catálogos y boxes con idBox autonumérico."

    def handle(self, *args, **options):
        # 1. Asegurar que existan los catálogos básicos
        for nombre in ['General', 'Especial']:
            TipoBox.objects.get_or_create(tipoBox=nombre)

        for estado in ['Libre', 'Ocupado', 'Inhabilitado']:
            DisponibilidadBox.objects.get_or_create(disponibilidad=estado)

        for est in ['Pendiente', 'Confirmada', 'Cancelada']:
            EstadoConsulta.objects.get_or_create(estadoConsulta=est)

        # 2. Crear pasillos A–D
        pasillos = []
        for pasillo in ['Pasillo 1', 'Pasillo 2', 'Pasillo 3', 'Pasillo 4']:
            p, _ = Pasillo.objects.get_or_create(nombrePasillo=pasillo)
            pasillos.append(p)

        # 3. Recoger datos relacionados
        tipos      = list(TipoBox.objects.all())
        dispos     = list(DisponibilidadBox.objects.all())
        medicos    = list(Medico.objects.all())
        especiales = list(Especialidad.objects.all())

        # 4. Limpiar boxes previos
        Box.objects.all().delete()

        # 5. Generar 5 boxes por pasillo
        for pasillo in pasillos:
            for _ in range(5):
                # Creamos la instancia sin pasar idBox ni numeroBox
                box = Box.objects.create(
                    tipoBox=random.choice(tipos),
                    disponibilidadBox=random.choice(dispos),
                    pasillo=pasillo,
                )

                # 6. (opcional) asignar 0–todas las especialidades
                if especiales:
                    muestra = random.sample(especiales, k=random.randint(0, len(especiales)))
                    for esp in muestra:
                        # usando la tabla intermedia automática
                        box.especialidades.add(esp)

                # 7. Asignar médico al 70% de los boxes
                if medicos and random.random() < 0.7:
                    box.medico = random.choice(medicos)
                    box.save()

        self.stdout.write(self.style.SUCCESS("✅ Boxes generados correctamente con idBox autonumérico."))
