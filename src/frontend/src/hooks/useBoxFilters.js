import { useState, useMemo } from "react";

// Recibe array de boxes, retorna filtros, setters y la lista filtrada
export default function useBoxFilters(boxes) {
  const [filters, setFilters] = useState({
    status:       "ALL",
    box:          "ALL",
    po:           "ALL",
    pasillo:      "ALL",
    medico:       "ALL",
    especialidad: "ALL",
  });

  // Filtrado reactivo y eficiente
  const filteredBoxes = useMemo(() => {
    return boxes.filter(box => {
      if (filters.status !== "ALL" && box.disponibilidad !== filters.status)
        return false;
      if (filters.box !== "ALL" && String(box.numeroBox ?? box.idBox) !== String(filters.box))
        return false;
      if (filters.po !== "ALL") {
        const po = box.porcentajeOcupacion ?? 0;
        if (filters.po === "0-50"      && !(po >= 0   && po < 50))  return false;
        if (filters.po === "50-80"     && !(po >= 50  && po < 80))  return false;
        if (filters.po === "80-100"    && !(po >= 80  && po <= 100)) return false;
      }
      if (filters.pasillo !== "ALL" && box.pasillo !== filters.pasillo)
        return false;
      if (filters.medico !== "ALL" && box.medicoAsignado !== filters.medico)
        return false;
      // Aquí podrías añadir más reglas si agregas campos (especialidad, etc)
      return true;
    });
  }, [boxes, filters]);

  return { filters, setFilters, filteredBoxes };
}
