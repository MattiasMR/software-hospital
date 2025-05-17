// src/components/HeaderBottom.jsx
import { FunnelIcon } from "@heroicons/react/24/solid";
import DatePicker from "react-datepicker";

export default function HeaderBottom({
  date, setDate,
  onOpenFilters // nueva prop
}) {
  return (
    <div className="flex items-center gap-4 bg-white py-2">
      <h1 className="text-lg font-bold flex-1">Dashboard de Boxes</h1>

      <div className="flex items-center gap-4 px-4">
      {/* único filtro visible: día */}
      <DatePicker
        selected={date}
        onChange={setDate}
        dateFormat="yyyy-MM-dd"
        className="border rounded px-2 py-1 text-sm bg-white"
      />

      {/* botón que abre el off-canvas */}
      <button
        onClick={onOpenFilters}
        className="flex items-center gap-1 px-3 py-2 rounded bg-gray-500 text-white text-sm hover:bg-cyan-700"
      >
        <FunnelIcon className="w-4 h-4" />
        Filtros
      </button>
      </div>
    </div>
  );
}
