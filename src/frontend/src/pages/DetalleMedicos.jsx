import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import Sidebar from '../components/Sidebar';
import HeaderTop from '../components/HeaderTop';
import HeaderBottom from '../components/HeaderBottom';
import WhiteCard from "../components/WhiteCard";
import { Bar, Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

// Registrar Chart.js
ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

function getDateString(date) {
  return date.toISOString().slice(0, 10);
}

export default function DetalleMedico() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Rango de fechas (últimos 7 días)
  const today = new Date();
  const [dateTo, setDateTo] = useState(getDateString(today));
  const [dateFrom, setDateFrom] = useState(
    getDateString(new Date(today.getFullYear(), today.getMonth(), today.getDate() - 6))
  );

  // Consulta a backend
  const fetchKpis = async () => {
    const res = await fetch(
      `http://127.0.0.1:8000/api/medicos/${id}/detalle/?date_from=${dateFrom}&date_to=${dateTo}`,
      { headers: { Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}` } }
    );
    if (!res.ok) throw new Error('Error al cargar los KPIs');
    return res.json();
  };

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['detalle-medico', id, dateFrom, dateTo],
    queryFn: fetchKpis,
  });

  // Preparar datos para gráficos
  const especialidades = data?.uso_por_especialidad ? Object.keys(data.uso_por_especialidad) : [];
  const usoEspecialidades = data?.uso_por_especialidad ? Object.values(data.uso_por_especialidad) : [];

  // Horas por semana para gráfico de barras
  const semanas = data?.horas_por_semana?.map(w => w.semana) ?? [];
  const horasPorSemana = data?.horas_por_semana?.map(w => w.horas) ?? [];

  // Box más usado
  const boxMasUsado = data?.box_mas_usado?.id ? `Box ${data.box_mas_usado.id}` : "—";
  const boxHoras = data?.box_mas_usado?.horas || 0;

  // Consultas realizadas
  const consultasRealizadas = data?.consultas_realizadas ?? 0;

  return (
    <div className="flex h-screen bg-[#DAD9D9]">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <HeaderTop />
        <HeaderBottom title="Detalle Médico" showDatePicker={false} showFilterButton={false} />

        <main className="flex-1 p-8 overflow-auto">
          <div className="max-w-2xl mx-auto w-full">
            <WhiteCard className="p-8">
              {!isLoading && !error && (
  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
    <div>
      <div className="text-2xl font-bold text-cyan-800">{data?.nombre ?? "Nombre Médico"}</div>
      <div className="text-lg text-gray-600">{data?.especialidad ?? "Especialidad"}</div>
    </div>
  </div>
)}

              <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-6 gap-4">
                <div className="flex flex-row gap-4">
                  <div>
                    <label className="block text-xs">Desde</label>
                    <input
                      type="date"
                      className="border rounded px-2 py-1"
                      value={dateFrom}
                      onChange={e => setDateFrom(e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="block text-xs">Hasta</label>
                    <input
                      type="date"
                      className="border rounded px-2 py-1"
                      value={dateTo}
                      onChange={e => setDateTo(e.target.value)}
                    />
                  </div>
                  <button
                    className="self-end h-9 px-4 py-1 bg-cyan-600 text-white rounded mt-auto"
                    onClick={refetch}
                  >
                    Buscar
                  </button>
                </div>
                <button
                  className="h-9 px-4 py-1 bg-gray-300 rounded hover:bg-gray-400 transition"
                  onClick={() => navigate(-1)}
                >
                  Volver
                </button>
              </div>

              {/* KPIs */}
              {isLoading ? (
                <div>Cargando...</div>
              ) : error ? (
                <div className="text-red-600">Error: {error.message}</div>
              ) : (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                    <div className="flex flex-col items-center">
                      <span className="text-lg font-semibold text-gray-700 mb-1">Porcentaje ocupación</span>
                      <span className="text-3xl font-bold text-cyan-700">{data.porcentaje_ocupacion ?? 0}%</span>
                    </div>
                    <div className="flex flex-col items-center">
                      <span className="text-lg font-semibold text-gray-700 mb-1">Consultas realizadas</span>
                      <span className="text-3xl font-bold text-orange-500">{consultasRealizadas}</span>
                    </div>
                    <div className="flex flex-col items-center">
                      <span className="text-lg font-semibold text-gray-700 mb-1">Box más usado</span>
                      <span className="text-xl font-bold">{boxMasUsado}</span>
                      <span className="text-base text-gray-600">({boxHoras} hrs)</span>
                    </div>
                  </div>

                  {/* Gráfico de barras: Horas asignadas por semana */}
                  <div className="mb-10">
                    <div className="font-bold mb-2 text-center">Horas asignadas por semana</div>
                    <div className="h-[260px]">
                      <Bar
                        data={{
                          labels: semanas,
                          datasets: [
                            {
                              label: "Horas",
                              data: horasPorSemana,
                            },
                          ],
                        }}
                        options={{
                          responsive: true,
                          plugins: { legend: { display: false } },
                          scales: { y: { beginAtZero: true } },
                        }}
                        height={240}
                      />
                    </div>
                  </div>

                  {/* Gráfico de torta: Uso por especialidad */}
                  <div className="mb-10">
                    <div className="font-bold mb-2 text-center">Consultas por especialidad</div>
                    <div className="flex justify-center">
                      <div className="w-[320px]">
                        <Pie
                          data={{
                            labels: especialidades,
                            datasets: [
                              {
                                data: usoEspecialidades,
                              },
                            ],
                          }}
                          options={{
                            responsive: true,
                            plugins: { legend: { position: 'bottom' } },
                          }}
                          height={180}
                        />
                      </div>
                    </div>
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
