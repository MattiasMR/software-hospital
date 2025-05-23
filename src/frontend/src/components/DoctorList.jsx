import { Link } from "react-router-dom";

// src/components/DoctorList.jsx
export default function DoctorList({ doctors = [] }) {
  return (
    <div className="flex flex-col gap-4">
      {doctors.length === 0 ? (
        <div className="text-gray-400 text-center">Sin doctores para hoy</div>
      ) : (
        doctors.map((doctor, idx) => (
          <div
            key={doctor.id || idx} // Prefiere id real si existe
            className="flex items-center bg-white rounded-lg shadow px-4 py-2 hover:shadow-md transition group"
          >
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-cyan-100 flex items-center justify-center text-cyan-700 font-bold text-lg mr-4">
              {doctor.avatarUrl ? (
                <img
                  src={doctor.avatarUrl}
                  alt={doctor.nombre}
                  className="w-10 h-10 rounded-full object-cover"
                />
              ) : (
                doctor.nombre?.[0]?.toUpperCase() || "?"
              )}
            </div>
            <div className="flex-1">
              <div className="font-semibold text-gray-900 group-hover:text-cyan-700">
                {doctor.nombre}
              </div>
              <div className="text-sm text-gray-500">
                {doctor.especialidad || "Sin especialidad"}
              </div>
            </div>
            <div>

            </div>
          </div>
        ))
      )}
    </div>
  );
}
