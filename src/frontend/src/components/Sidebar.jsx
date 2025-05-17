import { Link, useLocation } from "react-router-dom";
import {
  HomeIcon,
  MagnifyingGlassIcon,
  ExclamationTriangleIcon,
  CalendarIcon,
  ChartBarIcon,
  Cog6ToothIcon,
} from "@heroicons/react/24/solid";

const icons = [
  { icon: HomeIcon, to: "/" },
  { icon: MagnifyingGlassIcon },
  { icon: ExclamationTriangleIcon },
  { icon: CalendarIcon },
  { icon: ChartBarIcon },
  { icon: Cog6ToothIcon },
];

export default function Sidebar( {className = "" }) {
  const { pathname } = useLocation();

  return (
    <aside className={`bg-white flex flex-col items-center gap-4 shadow ${className}`}>
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
