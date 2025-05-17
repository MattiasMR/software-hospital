// src/pages/Dashboard.jsx
import { useState, useEffect } from 'react';
import { useSearchParams }      from 'react-router-dom';

import Sidebar                   from '../components/Sidebar';
import Header                    from '../components/Header';
import FiltersBar                from '../components/FiltersBar';
import BoxCard                   from '../components/BoxCard';

import bg                        from '../assets/images/login-bg.png';

export default function Dashboard() {
  const [boxes, setBoxes]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  // fecha desde query o hoy
  const [searchParams] = useSearchParams();
  const dateParam      = searchParams.get('date');
  const [date, setDate] = useState(
    dateParam ? new Date(dateParam) : new Date()
  );
  const isoDate = date.toISOString().slice(0, 10);

  // filtros
  const [filters, setFilters] = useState({
    status:       'ALL',
    box:          'ALL',
    po:           'ALL',
    pasillo:      'ALL',
    medico:       'ALL',
    especialidad: 'ALL',
  });

  useEffect(() => {
    setLoading(true);
    const token = localStorage.getItem('accessToken');

    fetch(`http://127.0.0.1:8000/api/boxes/status/?date=${isoDate}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(res => {
        if (res.status === 401) {
          window.location.href = '/login';
          throw new Error('No autorizado');
        }
        if (!res.ok) {
          throw new Error('Error al cargar boxes');
        }
        return res.json();
      })
      .then(data => {
        setBoxes(data);
        setError(null);
      })
      .catch(err => {
        console.error(err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [isoDate]);

  if (loading) return <p className="p-6">Cargando boxes…</p>;
  if (error)   return <p className="p-6 text-red-600">{error}</p>;

  // agrupar por pasillo
  const boxesByPasillo = boxes.reduce((acc, box) => {
    const p = box.pasillo || 'Sin pasillo';
    acc[p] = acc[p] || [];
    acc[p].push(box);
    return acc;
  }, {});

  return (
    <div className="relative flex h-screen">
      {/* fondo DEBAJO de todo */}
      <div
        className="absolute inset-0 bg-cover bg-center opacity-70 -z-10"
        style={{ backgroundImage: `url(${bg})` }}
      />

      {/* sidebar sólido encima del fondo */}
      <Sidebar />

      {/* contenido principal */}
      <div className="relative flex-1 flex flex-col">
      
        {/* header */}
        <div className="relative z-10">
          <Header />
        </div>

        {/* filtros */}
        <div className="px-6 py-4">
          <FiltersBar
            date={date}
            onDateChange={d => setDate(d)}
            filters={filters}
            setFilters={setFilters}
            boxes={boxes}
          />
        </div>

        {/* listado de boxes */}
        <main className="flex-1 overflow-auto px-6 pb-6">
          {Object.entries(boxesByPasillo)
            .sort(([a], [b]) => a.localeCompare(b))
            .map(([pasillo, group]) => (
              <section key={pasillo} className="mb-12">
                <h2 className="text-2xl font-bold mb-4">{pasillo}</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                  {group.map(box => (
                    <BoxCard
                      key={box.idBox}
                      id={box.idBox}
                      numero={box.numeroBox}
                      tipo={box.tipoBox.tipoBox}
                      disponibilidad={box.disponibilidad.disponibilidad}
                      medico={box.medico?.nombreCompleto}
                      porcentajeOcupacion={box.porcentajeOcupacion}
                    />
                  ))}
                </div>
              </section>
            ))}
        </main>
      </div>
    </div>
  );
}
