import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import HeaderTop from '../components/HeaderTop';
import WhiteCard from '../components/WhiteCard';
import HeaderBottom from '../components/HeaderBottom';
import DoctorList from "../components/DoctorList";
import DonutOcupacion from '../components/DonutOcupacion';

export default function Resumen() {
  const token = localStorage.getItem('accessToken') || '';

  // Resumen
  async function fetchResumen() {
    const res = await fetch('http://127.0.0.1:8000/api/resumen/', {
      headers: { Authorization: token ? `Bearer ${token}` : '' },
    });
    if (!res.ok) throw new Error('No se pudo cargar el resumen');
    return res.json();
  }

  // Boxes status para ocupación
  async function fetchBoxes() {
    const res = await fetch('http://127.0.0.1:8000/api/boxes/status/', {
      headers: { Authorization: token ? `Bearer ${token}` : '' },
    });
    if (!res.ok) throw new Error('No se pudo cargar los boxes');
    return res.json();
  }

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['resumen-dashboard'],
    queryFn: fetchResumen,
    staleTime: 60_000,
  });

  const { data: boxesData, isLoading: isBoxesLoading } = useQuery({
    queryKey: ['boxes-status'],
    queryFn: fetchBoxes,
    staleTime: 60_000,
  });

  // Cálculo del % de ocupación real
  let count = 0;
  let suma = 0;
  if (boxesData && Array.isArray(boxesData)) {
    boxesData.forEach(box => {
      if (box.porcentajeOcupacion === null) {
        return;
      }
      count += 1;
      suma += box.porcentajeOcupacion;
    });
  }
  const porcentajeOcupacion = count > 0
    ? Math.round((suma / count))
    : 0;

  return (
    <div className="flex h-screen bg-[#DAD9D9]">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <HeaderTop />
        <HeaderBottom title="Resumen General" showDatePicker={false} showFilterButton={false} />

        <main className="flex-1 p-8 overflow-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 max-w-screen-2xl mx-auto w-full ">
            {/* Consultas hoy */}
            <WhiteCard className="flex flex-col items-center justify-center text-center py-8 h-[320px] overflow-y-auto pr-2">
              <div className="text-5xl font-bold text-orange-500">{data?.consultas_hoy ?? '--'}</div>
              <div className="mt-4 text-xl font-medium">Consultas de hoy</div>
            </WhiteCard>

            {/* Donut de ocupación general */}
            <Link to="/dashboard" className="hover:scale-105 transition-transform duration-150 text-black " style={{ textDecoration: 'none' }}>
              <WhiteCard className="flex flex-col items-center justify-center text-center py-8 cursor-pointer h-[320px] pr-2">
                <div className="mb-2 font-bold text-lg">Ocupación General</div>
                <div className="mb-2 font-bold text-lg">de Boxes</div>
                <DonutOcupacion porcentaje={isBoxesLoading ? 0 : porcentajeOcupacion} />
                <div className="mt-2 text-sm text-gray-500">Ir al Dashboard</div>
                {isBoxesLoading && <span className="text-xs text-gray-400 mt-2">Cargando boxes...</span>}
              </WhiteCard>
            </Link>

            {/* Doctores del día */}
            <WhiteCard className="p-8 h-[320px] pr-2]">
              <div className="font-bold mb-3 pr-2">Doctores de hoy</div>
              <div className="max-h-[280px] overflow-y-auto pr-2">
                <DoctorList
                  doctors={
                    (data?.doctores_hoy ?? []).map(doc => ({
                      id: doc.id, // ¡¡AQUÍ el fix!!
                      nombre: doc.nombreCompleto || doc.nombre_completo || doc.nombre || "Sin nombre",
                      especialidad: doc.especialidad__nombreEspecialidad || "Sin especialidad"
                    }))
                  }
                />
              </div>
            </WhiteCard>

            {/* Disponibilidad de especialidades */}
            <WhiteCard className='p-8 h-[320px] pr-2'>
              <div className="font-bold mb-3 pr-2">Especialidades disponibles hoy</div>
              <ul className="max-h-[280px] overflow-y-auto pr-2 pl-0">
                {(data?.especialidades_disponibles ?? []).length === 0 && <li>No hay especialidades disponibles</li>}
                {(data?.especialidades_disponibles ?? []).map(e => (
                  <li key={e.especialidad} className="py-1 flex justify-between">
                    <span>{e.especialidad}</span>
                    <span className="font-bold">{e.cantidad_medicos}</span>
                  </li>
                ))}
              </ul>
            </WhiteCard>
          </div>

          {/* Distribución especialidades más consultadas */}
          <div className="max-w-screen-2xl mx-auto mt-8 w-full h-[320px]">
            <WhiteCard className='p-8 max-h-[44vh] '>
              <div className="font-bold mb-3 text-xl ">
                Distribución de consultas por especialidad (hoy)
              </div>
              <ol className="list-decimal list-inside text-lg space-y-2 overflow-y-auto max-h-[440px]">
                {(data?.top_especialidades ?? []).length === 0 && <li>No hay consultas hoy</li>}
                {(data?.top_especialidades ?? []).map((e, i) => (
                  <li key={i} className="flex justify-between items-center text-lg">
                    <span>{e.especialidad}</span>
                    <span className="text-cyan-700 font-bold">{e.consultas} consultas</span>
                  </li>
                ))}
              </ol>
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
