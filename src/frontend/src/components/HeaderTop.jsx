import { BellIcon, UserCircleIcon } from "@heroicons/react/24/solid"
import logo from '../assets/images/hospital-logo.png'
import { useNavigate } from "react-router-dom";


export default function HeaderTop( {className = "" } ) {
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
    <div className="flex items-center bg-white" style={{ height: '5rem' }}>
  
      {/* Logo a la izquierda */}
      <div className="w-auto h-full flex items-center justify-center bg-white">
        <img 
          src={logo} 
          alt="Hospital Padre Hurtado" 
          className="h-full w-auto" />
      </div>

      {/* Hora al centro */}
      <div className="flex-1 text-center">
        <p className="text-m font-medium">{formattedDate}</p>
        <p className="text-m">
          {now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })}
        </p>
      </div>

      {/* Iconos a la derecha */}
      <div className="flex items-center gap-4 pr-4">
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
