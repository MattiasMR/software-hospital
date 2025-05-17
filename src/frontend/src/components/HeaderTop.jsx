import { CalendarDaysIcon, BellIcon, UserCircleIcon } from "@heroicons/react/24/solid"
import logo from '../assets/images/hospital-logo.png'
import { useNavigate } from "react-router-dom";


export default function HeaderTop() {
  const now = new Date()
  const formattedDate = now.toLocaleDateString('es-CL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
  const navigate = useNavigate(); // ¡Debe estar aquí!

  function handleLogout() {
    localStorage.removeItem("accessToken");
    navigate("/login");
  }

  return (
    <div className="flex items-center bg-white px-6" style={{ height: '4rem' }}>
      {/* logo takes up all the left-over space */}
      <div className="flex items-center flex-shrink-0">
        <img src={logo} alt="Hospital Padre Hurtado" className="h-12" />
      </div>

      {/* push the clock into the exact center */}
      <div className="flex-1 text-center">
        <p className="text-sm font-medium">{formattedDate}</p>
        <p className="text-sm">
          {now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>

      {/* icons on the right */}
      <div className="flex items-center gap-4">
        <button
          onClick={handleLogout}
          className="mt-1 px-3 py-1 rounded-full bg-gray-200 text-gray-800 font-semibold hover:bg-gray-300 transition text-xs"
        >
          Cerrar sesión
        </button>
        <BellIcon className="h-6 w-6 text-gray-500" />
        <UserCircleIcon className="h-8 w-8 text-cyan-500" />
      </div>
    </div>
  )
}
