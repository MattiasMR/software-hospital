import { Link, useLocation } from "react-router-dom";
import {
  HomeIcon,
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
  CalendarIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  Squares2X2Icon,
} from "@heroicons/react/24/solid";

const icons = [
  { icon: HomeIcon, to: "/resumen" },
  { icon: Squares2X2Icon, to: "/dashboard" },
  { icon: ChartBarIcon, to: "/reportes" },
  { icon: MagnifyingGlassIcon, to: "/medicos" },
  { icon: ExclamationTriangleIcon },
  { icon: CalendarIcon },
  { icon: Cog6ToothIcon },
];

export default function Sidebar( {className = "" }) {
  const { pathname } = useLocation();

  return (
    <aside className={`bg-white flex flex-col items-center gap-4 shadow w-14 pt-28 ${className}`}>
      {icons.map(({ icon: Icon, to }, i) =>
        to ? (
          <Link key={i} to={to}>
            <Icon
              className={`h-7 w-7 cursor-pointer ${
                pathname === to ? "text-cyan-600" : "text-gray-700"
              } hover:text-cyan-500`}
            />
          </Link>
        ) : (
          <Icon key={i} className="h-7 w-7 text-gray-700" />
        )
      )}
    </aside>
  );
}
