// src/components/HeaderBottom.jsx
export default function HeaderBottom({
  date,
  setDate,
  onOpenFilters,
  title,
  showDatePicker = true, 
  showFilterButton = true, 
  backButton = false, 
  onBack 
}) {
  return (
    <div className="flex items-center justify-between pt-4 px-6 bg-white shadow">
      <h2 className="text-xl font-bold">{title}</h2>
      <div className="flex items-center gap-4">
        {showDatePicker && date && setDate && (
          <input
            type="date"
            value={date}
            onChange={e => setDate(e.target.value)}
            className="border rounded px-2 py-1"
          />
        )}
        {showFilterButton && onOpenFilters && (
          <button
            onClick={onOpenFilters}
            className="px-4 py-1 bg-cyan-600 text-white rounded shadow hover:bg-cyan-700 transition"
          >
            Filtros
          </button>
        )}
        {backButton && (
          <button
            onClick={onBack}
            className="px-4 py-1 bg-gray-300 text-black rounded shadow hover:bg-gray-400 transition"
          >
            Volver
          </button>
        )}
      </div>
    </div>
  );
}
