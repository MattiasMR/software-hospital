import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import HeaderTop from '../components/HeaderTop';
import WhiteCard from '../components/WhiteCard';
import HeaderBottom from '../components/HeaderBottom';
import DoctorList from "../components/DoctorList";

export default function Resumen() {
  const token = localStorage.getItem('accessToken') || '';

  // Fetcher para React Query
  async function fetchResumen() {
    const res = await fetch('http://127.0.0.1:8000/api/resumen/', {
      headers: { Authorization: token ? `Bearer ${token}` : '' },
    });
    if (!res.ok) throw new Error('No se pudo cargar el resumen');
    return res.json();
  }

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['resumen-dashboard'],
    queryFn: fetchResumen,
    staleTime: 60_000,
  });

  // --- Nuevo: Estados de filtro y búsqueda ---
  const [busqueda, setBusqueda] = useState('');
  const [especialidadFiltro, setEspecialidadFiltro] = useState('TODAS');

  const especialidades = [
    ...new Set((data?.doctores_hoy ?? []).map(doc => doc.especialidad__nombreEspecialidad || "Sin especialidad"))
  ];

  const doctoresFiltrados = (data?.doctores_hoy ?? []).filter(doc => {
    const coincideNombre =
      (doc.nombreCompleto || doc.nombre_completo || doc.nombre || "")
        .toLowerCase()
        .includes(busqueda.toLowerCase());
    const coincideEsp =
      especialidadFiltro === 'TODAS' ||
      (doc.especialidad__nombreEspecialidad || "Sin especialidad") === especialidadFiltro;
    return coincideNombre && coincideEsp;
  });

  return (
    <div className="flex h-screen bg-[#DAD9D9]">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <HeaderTop />
        <HeaderBottom title="Resumen General" showDatePicker={false} showFilterButton={true} />

        <main className="flex-1 p-8 overflow-auto">
          <div className="grid gap-8 max-w-screen-lg mx-auto">
            {/* Doctores del día */}
            <WhiteCard className="p-8 h-[70vh] pr-2 overflow-y-auto">
              <div className="font-bold mb-3 pr-2">Doctores de hoy</div>
              {/* --- Aquí van el buscador y el filtro --- */}
              <div className="flex gap-4 mb-4">
                <input
                  type="text"
                  className="border rounded px-2 py-1 flex-1"
                  placeholder="Buscar médico por nombre..."
                  value={busqueda}
                  onChange={e => setBusqueda(e.target.value)}
                />
                <select
                  className="border rounded px-2 py-1"
                  value={especialidadFiltro}
                  onChange={e => setEspecialidadFiltro(e.target.value)}
                >
                  <option value="TODAS">Todas las especialidades</option>
                  {especialidades.map((esp, i) => (
                    <option key={i} value={esp}>{esp}</option>
                  ))}
                </select>
              </div>
              {/* --- Lista filtrada --- */}
              <div className="max-h-[68vh] overflow-y-auto pr-2">
                <DoctorList
                  doctors={
                    doctoresFiltrados.map(doc => ({
                      id: doc.id,
                      nombre: doc.nombreCompleto || doc.nombre_completo || doc.nombre || "Sin nombre",
                      especialidad: doc.especialidad__nombreEspecialidad || "Sin especialidad"
                    }))
                  }
                />
              </div>
            </WhiteCard>
          </div>
          {/* Loading & error */}
          {isLoading && <p className="text-center mt-8">Cargando resumen...</p>}
          {error && (
            <div className="text-center mt-8 text-red-600">
              {error.message}
              <button onClick={() => refetch()} className="ml-2 underline">Reintentar</button>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
