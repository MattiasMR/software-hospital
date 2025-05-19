// src/pages/DetalleBox.jsx

import { useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';

import { useBoxDetalleQuery } from '../hooks/useBoxDetalleQuery';

import Sidebar from '../components/Sidebar';
import HeaderBottom from '../components/HeaderBottom';
import HeaderTop from '../components/HeaderTop';
import WhiteCard from '../components/WhiteCard';
import DonutOcupacion from '../components/DonutOcupacion';

import bg from '../assets/images/login-bg.png';

function formatDateLocal(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export default function DetalleBox() {
  const { idBox } = useParams();
  const navigate = useNavigate();
  const { search } = useLocation();
  const qs = new URLSearchParams(search);
  const dateFromQuery = qs.get('date');

  // Parse YYYY-MM-DD into a local Date at midnight
  const [date, setDate] = useState(() => {
    if (dateFromQuery) {
      const [y, m, d] = dateFromQuery.split('-').map(Number);
      return new Date(y, m - 1, d);
    }
    return new Date();
  });

  const {
    data: box,
    isLoading,
    isError,
    refetch,
  } = useBoxDetalleQuery(idBox, date);

  const handleBack = () => {
    const ds = formatDateLocal(date);
    navigate(`/?date=${ds}`);
  };

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
                  title="Detalle de Box"
                  backButton
                  onBack={() => navigate(-1)}
                />

        <main className="flex-1 overflow-auto py-8">
          <div className="max-w-screen-md mx-auto px-4">
            <WhiteCard className='p-8'>
              {/* controles: Volver + Fecha */}
              <div className="flex flex-wrap items-center justify-between mb-6 gap-4">
                <div className="flex items-center space-x-2">
                  <label className="text-gray-700 text-sm">Fecha:</label>
                  <DatePicker
                    selected={date}
                    onChange={setDate}
                    dateFormat="yyyy-MM-dd"
                    className="border rounded px-2 py-1 text-sm bg-white"
                  />
                </div>
              </div>

              {isLoading ? (
                <p className="text-center">Cargando detalle…</p>
              ) : isError ? (
                <div className="text-center text-red-600">
                  <p>Error al cargar detalle.</p>
                  <button
                    onClick={() => refetch()}
                    className="underline text-sm"
                  >
                    Reintentar
                  </button>
                </div>
              ) : (
                <>
                  {/* Título y Donut */}
                  <div className="flex flex-wrap items-center justify-between gap-6 mb-6">
                    <div>
                      <h1 className="text-2xl font-bold">Box {idBox}</h1>
                      <p className="text-sm text-gray-600">
                        <span className="font-medium">{box.pasillo}</span>
                      </p>
                    </div>
                    <DonutOcupacion porcentaje={box.porcentajeOcupacion} />
                  </div>

                  {/* Franjas */}
                  <h2 className="text-xl font-semibold mb-2">
                    Franjas horarias del día
                  </h2>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm border-collapse">
                      <thead className="bg-gray-100">
                        <tr>
                          <th className="border px-2 py-1">Hora</th>
                          <th className="border px-2 py-1">Médico</th>
                          <th className="border px-2 py-1">Especialidad</th>
                          <th className="border px-2 py-1">Estado</th>
                        </tr>
                      </thead>
                      <tbody>
                        {box.franjas.length === 0 ? (
                          <tr>
                            <td
                              colSpan={4}
                              className="border px-2 py-4 text-center text-gray-500"
                            >
                              Sin franjas
                            </td>
                          </tr>
                        ) : (
                          box.franjas.map((f, idx) => (
                            <tr
                              key={idx}
                              className="odd:bg-white even:bg-gray-50"
                            >
                              <td className="border px-2 py-1">
                                {f.inicio} – {f.fin}
                              </td>
                              <td className="border px-2 py-1">
                                {f.medico || '—'}
                              </td>
                              <td className="border px-2 py-1">
                                {f.especialidad || '—'}
                              </td>
                              <td className="border px-2 py-1">{f.estado}</td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </>
              )}
            </WhiteCard>
          </div>
        </main>
      </div>
    </div>
  );
}
