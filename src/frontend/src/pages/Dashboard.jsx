// src/pages/Dashboard.jsx

import React, { useState, useMemo, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';

// hooks
import { useBoxesQuery, fetchBoxes } from '../hooks/useBoxesQuery';
import useBoxFilters from '../hooks/useBoxFilters';

// components
import Offcanvas    from '../components/Offcanvas';
import HeaderTop    from '../components/HeaderTop';
import HeaderBottom from '../components/HeaderBottom';
import FiltersPanel from '../components/FiltersPanel';
import Sidebar      from '../components/Sidebar';
import BoxCard      from '../components/BoxCard';

// asset
import bg from '../assets/images/login-bg.png';

// Helper to get today's date as YYYY-MM-DD
function todayYYYYMMDD() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const queryClient = useQueryClient();
  const token = localStorage.getItem('accessToken') || '';

  // ALWAYS treat the date as a string in YYYY-MM-DD
  const paramDate = searchParams.get('date');
  const [dateStr, setDateStr] = useState(paramDate || todayYYYYMMDD());

  // Parse dateStr only for display purposes (e.g., in DatePicker or headers)
  const dateObj = React.useMemo(() => {
    const [y, m, d] = dateStr.split('-').map(Number);
    return new Date(y, m - 1, d);
  }, [dateStr]);

  // Keep picker and URL param in sync
  const handleDateChange = newDateStr => {
    setDateStr(newDateStr);
    setSearchParams({ date: newDateStr }, { replace: true });
  };

  // Prefetch all boxes for current month
  useEffect(() => {
    const [year, month] = dateStr.split('-').map(Number);
    const daysInMonth = new Date(year, month, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
      const ds = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      queryClient.prefetchQuery({
        queryKey: ['boxes', ds],
        queryFn: () => fetchBoxes(ds, token),
        staleTime: 1000 * 60 * 60,
      });
    }
  }, [dateStr, queryClient, token]);

  // Filters and filter panel
  const [filters, setFilters] = useState({
    disponibilidad: 'ALL',
    po: 'ALL',
    box: 'ALL',
    pasillo: 'ALL',
    medico: 'ALL',
  });
  const [showFilters, setShowFilters] = useState(false);

  // Fetch boxes for selected date
  const {
    data: boxes = [],
    isLoading,
    isError,
    refetch,
    isFetching,
    isPreviousData,
  } = useBoxesQuery(dateObj);

  // In-memory filter
  const { filteredBoxes } = useBoxFilters(boxes, filters);

  // Unique lists for selects
  const pasillos = useMemo(
    () => [...new Set(boxes.map(b => b.pasillo))].filter(Boolean).sort(),
    [boxes]
  );
  const boxNums = useMemo(
    () => [...new Set(boxes.map(b => b.idBox))].sort((a, b) => a - b),
    [boxes]
  );
  const medicos = useMemo(
    () => [...new Set(boxes.flatMap(b => b.medicosDelDia))].sort(),
    [boxes]
  );

  // Group by pasillo
  const boxesByPasillo = useMemo(() => {
    return filteredBoxes.reduce((acc, box) => {
      const p = box.pasillo || 'Sin pasillo';
      acc[p] = acc[p] || [];
      acc[p].push(box);
      return acc;
    }, {});
  }, [filteredBoxes]);

  // Ahora:
  if (isLoading && boxes.length === 0) {
    // Solo si no hay ningún dato cacheado aún, muestra el loading
    return <p className="p-6 text-center">Cargando boxes…</p>;
  }
  if (isError) {
    return (
      <div className="p-6 text-center text-red-600">
        Error al cargar boxes.{" "}
        <button onClick={() => refetch()} className="underline">
          Reintentar
        </button>
      </div>
    );
  }

  // Render
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />

      <div className="relative flex-1 flex flex-col">
        {/* fondo difuminado */}
        <div
          className="absolute inset-0 -z-10 bg-cover bg-center opacity-70"
          style={{ backgroundImage: `url(${bg})` }}
        />

        <HeaderTop />

        <HeaderBottom
          title="Dashboard de Boxes"
          // Pass the raw string for input type=date
          date={dateStr}
          setDate={handleDateChange}
          onOpenFilters={() => setShowFilters(true)}
          // In your HeaderBottom, use the string for <input type="date" value={date} />
        />

        <main className="flex-1 overflow-auto py-6">
          <div className="max-w-screen-xl mx-auto px-4">
            {Object.entries(boxesByPasillo)
              .sort(([a], [b]) => a.localeCompare(b))
              .map(([pasillo, group]) => (
                <section key={pasillo} className="mb-12">
                  <h2 className="inline-block bg-white rounded-full px-6 py-2 text-xl font-bold mb-4 shadow">
                    {pasillo}
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    {group.map(box => (
                      <BoxCard
                        key={box.idBox}
                        id={box.idBox}
                        numero={box.idBox}
                        disponibilidad={box.disponibilidad}
                        medico={box.medicoAsignado}
                        porcentajeOcupacion={box.porcentajeOcupacion}
                        onClick={() =>
                          navigate(`/detalle-box/${box.idBox}?date=${dateStr}`)
                        }
                      />
                    ))}
                  </div>
                </section>
              ))}
          </div>
        </main>
      </div>

      {/* off-canvas de filtros */}
      <Offcanvas open={showFilters} onClose={() => setShowFilters(false)}>
        <h2 className="text-xl font-semibold mb-4">Filtros</h2>
        <FiltersPanel
          date={dateStr}
          setDate={handleDateChange}
          filters={filters}
          setFilters={setFilters}
          pasillos={pasillos}
          boxes={boxNums}
          medicos={medicos}
        />
      </Offcanvas>
    </div>
  );
}
