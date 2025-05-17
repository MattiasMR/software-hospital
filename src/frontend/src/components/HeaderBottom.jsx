import FiltersBar from './FiltersBar'

export default function HeaderBottom({
  date, onDateChange,
  filters, setFilters,
  boxes
}) {
  return (
    <div className="flex items-center bg-white justify-between px-6" style={{ height: '3rem' }}>
      <h1 className="text-xl font-bold">Dashboard de Boxes</h1>
      <FiltersBar
        date={date}
        onDateChange={onDateChange}
        filters={filters}
        setFilters={setFilters}
        boxes={boxes}
      />
    </div>
  )
}
