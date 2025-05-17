import { CalendarDaysIcon, BellIcon, QuestionMarkCircleIcon, UserCircleIcon } from '@heroicons/react/24/solid'
import FiltersBar from './FiltersBar'
import logo from '../assets/images/hospital-logo.png'
import { useSearchParams } from 'react-router-dom'

export default function Header({ date, onDateChange, filters, setFilters, boxes }) {
  // Fecha y hora actuales
  const now = new Date()
  const formattedDate = now.toLocaleDateString('es-CL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
  const formattedTime = now.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  })

  // Para sincronizar la query param “date” con el input de fecha
  const [searchParams] = useSearchParams()

  return (
    <div className="bg-white shadow flex flex-col">
      {/* Primera barra */}
      <div className="h-16 px-6 flex items-center justify-between">
        {/* Logo */}
        <img src={logo} alt="Hospital Padre Hurtado" className="h-10" />

        {/* Fecha / Hora */}
        <div className="text-center hidden sm:block">
          <p className="text-sm font-medium">{formattedDate}</p>
          <p className="text-sm">{formattedTime}</p>
        </div>

        {/* Iconos de ayuda / notificaciones / usuario */}
        <div className="flex items-center gap-4">
          <QuestionMarkCircleIcon className="h-6 w-6 text-gray-500" />
          <BellIcon className="h-6 w-6 text-gray-500" />
          <UserCircleIcon className="h-8 w-8 text-cyan-500" />
        </div>
      </div>

      {/* Segunda barra */}
      <div className="h-12 px-6 flex items-center justify-between">
        {/* Título */}
        <h1 className="text-xl font-bold">Dashboard de Boxes</h1>

        {/* Filtros */}
        <FiltersBar
          date={date}
          onDateChange={onDateChange}
          filters={filters}
          setFilters={setFilters}
          boxes={boxes}
        />
      </div>
    </div>
  )
}
