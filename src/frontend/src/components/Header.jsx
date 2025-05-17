// src/components/Header.jsx
import { CalendarDaysIcon, BellIcon, QuestionMarkCircleIcon, UserCircleIcon } from "@heroicons/react/24/solid";

import logo                      from '../assets/images/hospital-logo.png';


export default function Header() {
  const now = new Date();
  const formatted = now.toLocaleDateString("es-CL", { day:"2-digit", month:"2-digit", year:"numeric" });

  return (
    <header className="flex items-center justify-between bg-white h-16 px-4 shadow">
      <div className="absolute top-4 left-4 z-20">
          <img src={logo} alt="Hospital Padre Hurtado" className="w-32" />
      </div>
      <div className="flex items-center gap-2">
        <CalendarDaysIcon className="h-6 w-6 text-gray-500" />
        <p className="text-sm font-medium">Dashboard</p>
      </div>

      {/* CENTRO: Fecha/Hora */}
      <div className="text-center hidden sm:block">
        <p className="text-xs font-medium">{formatted}</p>
        <p className="text-xs">{now.toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" })}</p>
      </div>

      {/* DER: Iconos */}
      <div className="flex items-center gap-3">
        <QuestionMarkCircleIcon className="h-6 w-6 text-gray-500" />
        <BellIcon className="h-6 w-6 text-gray-500" />
        <UserCircleIcon className="h-8 w-8 text-cyan-500" />
      </div>
    </header>
  );
}
