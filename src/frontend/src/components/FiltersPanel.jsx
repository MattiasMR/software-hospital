export default function FiltersPanel({
  filters, setFilters,
  pasillos, boxes, medicos
}) {
  const chip = "w-full px-3 py-2 rounded bg-gray-100 text-sm";

  const upd = key => e => setFilters({ 
    ...filters, 
    [key]: e.target.value 
  });

  const DEFAULT_FILTERS = {
      disponibilidad: "ALL",
      po: "ALL",
      box: "ALL",
      pasillo: "ALL",
      medico: "ALL",
    };

  return (
    <div className="space-y-4">
      {/* ——— Filtro por disponibilidad ——— */}
      <select className={chip} value={filters.disponibilidad} onChange={upd("disponibilidad")}>
        <option value="ALL">Disponibilidad</option>
        <option value="Ocupado">Ocupado</option>
        <option value="Libre">Libre</option>
        <option value="Inhabilitado">Inhabilitado</option>
      </select>

      {/* ——— PO, Box, Pasillo, Médico ——— */}
      <select className={chip} value={filters.po} onChange={upd("po")}>
        <option value="ALL">PO</option>
        <option value="0-50">0-50 %</option>
        <option value="50-80">50-80 %</option>
        <option value="80-100">80-100 %</option>
      </select>

      <select className={chip} value={filters.box} onChange={upd("box")}>
        <option value="ALL">Box</option>
        {boxes.map(n => (
          <option key={n} value={n}>{n}</option>
        ))}
      </select>

      <select className={chip} value={filters.pasillo} onChange={upd("pasillo")}>
        <option value="ALL">Pasillo</option>
        {pasillos.map(p => (
          <option key={p} value={p}>{p}</option>
        ))}
      </select>

      <select className={chip} value={filters.medico} onChange={upd("medico")}>
        <option value="ALL">Médico</option>
        {medicos.map(m => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>

      <div className="mt-auto flex justify-end">
        <button
          type="button"
          onClick={() => setFilters(DEFAULT_FILTERS)}
          className="px-4 py-1 pt-2 rounded-full bg-gray-500 text-white text-sm font-medium hover:bg-cyan-700 transition"
        >
          Limpiar filtros
        </button>
      </div>

    </div>
  );
}
