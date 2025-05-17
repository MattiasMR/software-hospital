import DatePicker from "react-datepicker";

export default function FiltersBar({
  date,
  onDateChange,
  filters, setFilters,
  boxes,
}) {
  /* lista de codes para combo */
  const boxCodes = [...new Set(boxes.map(b => b.code))];

  const chip = "px-3 py-1 rounded-full bg-gray-300 hover:bg-gray-400 text-sm";
  const set  = k => e => setFilters({ ...filters, [k]: e.target.value });

  return (
    <div className="flex flex-wrap gap-3 items-center">
      {/* único selector de fecha (día) */}
      <DatePicker
        selected={date}
        onChange={onDateChange}
        dateFormat="dd/MM/yyyy"
        className="border rounded px-2 py-1 text-sm bg-white"
      />

      {/* Combos de filtrado */}
      <select className={chip} value={filters.po}   onChange={set("po")}>
        <option value="ALL">PO</option>
        <option value="0-50">0-50 %</option>
        <option value="50-80">50-80 %</option>
        <option value="80-100">80-100 %</option>
      </select>

      <select className={chip} value={filters.box} onChange={set("box")}>
        <option value="ALL">Box</option>
        {[...new Set(boxes.map(b => b.code))]
          .sort((a, b) => a - b)
          .map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
      </select>


      <select className={chip} value={filters.status} onChange={set("status")}>
        <option value="ALL">Estado</option>
        <option value="HABILITADO">Habilitado</option>
        <option value="OCUPADO">Ocupado</option>
        <option value="INHABILITADO">Inhabilitado</option>
      </select>
      <select className={chip} value={filters.pasillo} onChange={set("pasillo")}>
        <option value="ALL">Pasillo</option>
        {["A", "B", "C"].filter(p => boxes.some(b => b.pasillo === p)).map(p => (
          <option key={p} value={p}>{p}</option>
        ))}
      </select>
      <select className={chip} value={filters.doctor} onChange={set("doctor")}>
        <option value="ALL">Médico</option>
        {[...new Set(boxes.map(b => b.doctor).filter(d => d && d !== "—"))]
          .sort()
          .map(name => (
            <option key={name} value={name}>{name}</option>
        ))}
      </select>
      <select className={chip} value={filters.especialidad} onChange={set("especialidad")}>
        <option value="ALL">Especialidad</option>
        {[...new Set(
          boxes.flatMap(b => b.especialidades_dia || [])
        )]
          .sort()
          .map(spec => (
            <option key={spec} value={spec}>{spec}</option>
        ))}
      </select>

    </div>
  );
}
