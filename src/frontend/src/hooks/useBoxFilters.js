import { useMemo } from "react";

/**
 * @param {Array}  boxes   – array proveniente del SSE / backend
 * @param {Object} filters – { disponibilidad, box, po, pasillo, medico }
 */

export default function useBoxFilters(boxes, filters) {
  const filteredBoxes = useMemo(() => {
    return boxes.filter((box) => {
      // Disponibilidad: Libre | Ocupado | Inhabilitado
      if (
        filters.disponibilidad !== "ALL" &&
        box.disponibilidad !== filters.disponibilidad
      )
        return false;

      // Box (id numérico)
      if (filters.box !== "ALL" && String(box.idBox) !== String(filters.box))
        return false;

      // Porcentaje de ocupación
      if (filters.po !== "ALL") {
        const po = box.porcentajeOcupacion ?? 0;
        if (filters.po === "0-50" && !(po >= 0 && po < 50)) return false;
        if (filters.po === "50-80" && !(po >= 50 && po < 80)) return false;
        if (filters.po === "80-100" && !(po >= 80 && po <= 100)) return false;
      }

      // Pasillo
      if (filters.pasillo !== "ALL" && box.pasillo !== filters.pasillo)
        return false;

      // Médico asignado
      if (filters.medico !== "ALL" && box.medicoAsignado !== filters.medico)
        return false;

      return true;
    });
  }, [boxes, filters]);

  return { filteredBoxes };
}
