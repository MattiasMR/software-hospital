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

function buildFranjas2h() {
  const franjas = [];
  for (let h = 4; h < 22; h += 2) {
    franjas.push({
      inicio: `${String(h).padStart(2, '0')}:00`,
      fin: `${String(h + 2).padStart(2, '0')}:00`
    });
  }
  return franjas;
}

export default function DetalleBox() {
  const { idBox } = useParams();
  const navigate = useNavigate();
  const { search } = useLocation();
  const qs = new URLSearchParams(search);
  const dateFromQuery = qs.get('date');

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

  const [selectedFranjaIdx, setSelectedFranjaIdx] = useState(0);
  const franjas = buildFranjas2h();
  const consultas = box?.consultas ?? [];

  const medicosPorFranja = franja => [
    ...new Set(
      consultas
        .filter(c => c.inicio >= franja.inicio && c.inicio < franja.fin)
        .map(c => c.medico)
    )
  ];

  const selectedFranja = franjas[selectedFranjaIdx];
  const consultasFranja = consultas.filter(
    c => c.inicio >= selectedFranja.inicio && c.inicio < selectedFranja.fin
  );

  // --- Render ---
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />

      <div className="relative flex-1 flex flex-col">
        <div
          className="absolute inset-0 -z-10 bg-cover bg-center opacity-60"
          style={{ backgroundImage: `url(${bg})` }}
        />

        <HeaderTop />
        <HeaderBottom
          title="Detalle de Box"
          backButton
          onBack={() => navigate(-1)}
        />

        <main className="flex-1 overflow-auto py-10 px-14">
          <div className="w-auto mx-auto h-[82vh]">
            {isError && (
              <div className="text-center text-red-600 mb-4">
                <p>Error al cargar detalle.</p>
                <button onClick={refetch} className="underline text-sm">
                  Reintentar
                </button>
              </div>
            )}

            <div className="flex flex-col md:flex-row gap-8 h-[80vh]">
              {/* Card 1: Franjas */}
              <WhiteCard className="p-8 flex flex-col flex-1 min-w-[350px] shadow-lg border border-cyan-100 bg-white bg-opacity-90">
                <div className="flex items-center mb-6">
                  <label className="text-cyan-700 text-base font-semibold mr-2">Fecha:</label>
                  <DatePicker
                    selected={date}
                    onChange={setDate}
                    dateFormat="yyyy-MM-dd"
                    className="border rounded px-2 py-1 text-sm bg-white"
                  />
                </div>

                {isLoading ? (
                  <div className="text-center flex-1 text-cyan-600 font-semibold">Cargando detalle…</div>
                ) : (
                  <>
                    <div className="mb-6 flex flex-row items-center justify-between">
                      <div>
                        <h1 className="text-3xl font-bold text-cyan-700">Box {idBox}</h1>
                        <p className="text-base text-gray-600">{box?.pasillo}</p>
                      </div>
                      <div className="ml-auto">
                        <DonutOcupacion porcentaje={box?.porcentajeOcupacion || 0} />
                      </div>
                    </div>
                    <h2 className="text-xl font-semibold mb-2 text-cyan-800">Turnos del día</h2>
                    <div className="flex-1 overflow-auto rounded-lg">
                      <table className="w-full text-[15px] border-separate border-spacing-y-2">
                        <thead>
                          <tr>
                            <th className="px-2 py-1 text-left text-cyan-900">Inicio</th>
                            <th className="px-2 py-1 text-left text-cyan-900">Fin</th>
                            <th className="px-2 py-1 text-left text-cyan-900">Médico(s)</th>
                          </tr>
                        </thead>
                        <tbody>
                          {franjas.map((franja, idx) => (
                            <tr
                              key={idx}
                              className={
                                "transition cursor-pointer rounded-lg " +
                                (idx === selectedFranjaIdx
                                  ? "bg-cyan-100 font-semibold shadow"
                                  : "hover:bg-cyan-50")
                              }
                              style={{ borderRadius: '0.6rem' }}
                              onClick={() => setSelectedFranjaIdx(idx)}
                            >
                              <td className="px-2 py-2 rounded-l-md">{franja.inicio}</td>
                              <td className="px-2 py-2">{franja.fin}</td>
                              <td className="px-2 py-2 rounded-r-md text-gray-800">
                                {medicosPorFranja(franja).join(", ") || <span className="text-gray-400">—</span>}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </>
                )}
              </WhiteCard>

              {/* Card 2: Consultas de franja seleccionada */}
              <WhiteCard className="p-8 flex flex-col flex-1 min-w-[400px] shadow-lg border border-cyan-100 bg-white bg-opacity-95">
                <h2 className="text-xl font-semibold mb-4 text-cyan-800">
                  Consultas de <span className="text-cyan-600">{selectedFranja.inicio}</span> a <span className="text-cyan-600">{selectedFranja.fin}</span>
                </h2>
                {isLoading ? (
                  <div className="text-center flex-1 text-cyan-600 font-semibold">Cargando consultas…</div>
                ) : (
                  <div className="flex-1 overflow-auto rounded-lg">
                    <table className="w-full text-[15px] border-separate border-spacing-y-2">
                      <thead>
                        <tr>
                          <th className="px-2 py-1 text-left text-cyan-900">Médico</th>
                          <th className="px-2 py-1 text-left text-cyan-900">Especialidad</th>
                          <th className="px-2 py-1 text-left text-cyan-900">Inicio</th>
                          <th className="px-2 py-1 text-left text-cyan-900">Fin</th>
                          <th className="px-2 py-1 text-left text-cyan-900">Estado</th>
                        </tr>
                      </thead>
                      <tbody>
                        {consultasFranja.length === 0 ? (
                          <tr>
                            <td colSpan={5} className="px-2 py-4 text-center text-gray-400 font-semibold">
                              Sin consultas registradas
                            </td>
                          </tr>
                        ) : (
                          consultasFranja.map((c, idx) => (
                            <tr key={idx} className="rounded-lg bg-cyan-50 even:bg-white">
                              <td className="px-2 py-2 rounded-l-md">{c.medico}</td>
                              <td className="px-2 py-2">{c.especialidad || <span className="text-gray-400">—</span>}</td>
                              <td className="px-2 py-2">{c.inicio}</td>
                              <td className="px-2 py-2">{c.fin}</td>
                              <td className="px-2 py-2 rounded-r-md">
                                <span className={
                                  c.estado === "Pendiente" ? "bg-yellow-200 text-yellow-700 px-2 py-1 rounded-md"
                                  : c.estado === "Confirmada" || c.estado === "En curso" ? "bg-cyan-200 text-cyan-800 px-2 py-1 rounded-md"
                                  : c.estado === "Cancelada" ? "bg-red-100 text-red-700 px-2 py-1 rounded-md"
                                  : "bg-gray-100 text-gray-700 px-2 py-1 rounded-md"
                                }>
                                  {c.estado}
                                </span>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                )}
              </WhiteCard>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
