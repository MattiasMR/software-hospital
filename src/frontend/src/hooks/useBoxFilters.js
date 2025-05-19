import { useMemo } from 'react';

/**
 * Filtra en memoria el array de boxes según los filtros seleccionados.
 * @param {Array}  boxes   – listado completo de boxes
 * @param {Object} filters – { disponibilidad, box, po, pasillo, medico }
 * @returns {{ filteredBoxes: Array }} – boxes que cumplen todos los filtros
 */
export default function useBoxFilters(boxes, filters) {
  const filteredBoxes = useMemo(() => {
    return boxes.filter(box => {
      // Disponibilidad: ALL | Libre | Ocupado | Inhabilitado
      if (filters.disponibilidad !== 'ALL' &&
          box.disponibilidad !== filters.disponibilidad) {
        return false;
      }

      // Número de box
      if (filters.box !== 'ALL' &&
          String(box.idBox) !== String(filters.box)) {
        return false;
      }

      // Porcentaje de ocupación
      if (filters.po !== 'ALL') {
        const po = box.porcentajeOcupacion ?? 0;
        if (filters.po === '0-50'   && !(po >=   0 && po <  50)) return false;
        if (filters.po === '50-80'  && !(po >=  50 && po <  80)) return false;
        if (filters.po === '80-100' && !(po >=  80 && po <= 100)) return false;
      }

      // Pasillo
      if (filters.pasillo !== 'ALL' &&
          box.pasillo !== filters.pasillo) {
        return false;
      }

      // Médico del día
      if (filters.medico !== 'ALL') {
        if (
          !Array.isArray(box.medicosDelDia) ||
          !box.medicosDelDia.includes(filters.medico)
        ) {
          return false;
        }
      }

      // Si pasa todas las comprobaciones, lo incluimos
      return true;
    });
  }, [boxes, filters]);

  return { filteredBoxes };
}