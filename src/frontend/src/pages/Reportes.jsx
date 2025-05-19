// src/pages/Reportes.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip,
  PieChart, Pie, Cell, Legend, ResponsiveContainer
} from 'recharts';

import Sidebar       from '../components/Sidebar';
import HeaderTop from '../components/HeaderTop';
import HeaderBottom  from '../components/HeaderBottom';
import WhiteCard     from '../components/WhiteCard';

// helper para formatear Date -> YYYY-MM-DD
function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

// fetcher para React Query (queda, pero sin fondo ni lógica visual aquí aún)
async function fetchReportes({ queryKey }) {
  const [, from, to] = queryKey;
  const token = localStorage.getItem('accessToken');
  const res = await fetch(
    `http://127.0.0.1:8000/api/boxes/reportes/?date_from=${from}&date_to=${to}`,
    {
      headers: {
        Authorization: token ? `Bearer ${token}` : '',
      },
    }
  );
  if (res.status === 401) {
    localStorage.removeItem('accessToken');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }
  if (!res.ok) throw new Error(`Error ${res.status} cargando reporte`);
  return res.json();
}

export default function Reportes() {
  const navigate = useNavigate();
  const token    = localStorage.getItem('accessToken') || '';

  // rango de fechas
  const [dateFrom, setDateFrom] = useState(new Date());
  const [dateTo,   setDateTo]   = useState(new Date());

  const fromStr = formatDate(dateFrom);
  const toStr   = formatDate(dateTo);

  const { data: kpi, isLoading, error, refetch } = useQuery({
    queryKey: ['reportes', fromStr, toStr],
    queryFn:  fetchReportes,
    keepPreviousData: true,
    staleTime: 60_000,
  });

  // datos de ejemplo para visualización
  const barData = Object.entries(kpi?.medicos_por_franja  ?? {})
    .map(([franja, count]) => ({ franja, count }));
  const pieData = Object.entries(kpi?.uso_por_especialidad ?? {})
    .map(([name, value]) => ({ name, value }));
  const COLORS  = ['#2dd4bf','#22d3ee','#38bdf8','#60a5fa','#818cf8','#a78bfa'];

  return (
    <div className="flex h-screen bg-[#DAD9D9]">
      <Sidebar />

      <div className="flex-1 flex flex-col">

        <HeaderTop />
        {/* HeaderBottom reusado con título y botón de volver */}
        <HeaderBottom
          title="Reportes"
          backButton
          onBack={() => navigate(-1)}
        />

        <main className="flex-1 p-6 overflow-hidden bg-[#DAD9D9]">
          <div className="space-y-6">

            {/* rango de fechas */}
            <div className="flex justify-center space-x-4">
              <input
                type="date"
                value={fromStr}
                onChange={e => setDateFrom(new Date(e.target.value))}
                className="border px-3 py-1 rounded"
              />
              <span className="self-center text-gray-600">a</span>
              <input
                type="date"
                value={toStr}
                onChange={e => setDateTo(new Date(e.target.value))}
                className="border px-3 py-1 rounded"
              />
            </div>

            {isLoading ? (
              <p className="text-center">Cargando reporte…</p>
            ) : error ? (
              <div className="text-center text-red-600 space-y-2">
                <p>{error.message}</p>
                <button onClick={() => refetch()} className="underline text-sm">
                  Reintentar
                </button>
              </div>
            ) : (

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

                {/* 1. Gráfico de barras */}
                <WhiteCard className="flex flex-col items-center w-full h-full p-0"> 
                <h3 className="mb-2 font-semibold pt-4">Médicos por franja</h3>
                <div className="w-[calc(100%-2.5rem)] h-[calc(100%-2.5rem)] p-0">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={barData} margin={{ top: 20, right: 20, left: 0, bottom: 20 }}>
                      <XAxis dataKey="franja" tick={{ fontSize: 10 }} />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#db2777" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </WhiteCard>


                {/* 2. Panel central de KPIs */}
                <div className="flex flex-col gap-4 w-full">
                  
                <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                  <WhiteCard className="text-center p-6 ">
                    <p className="text-xl text-black font-bold">Médico líder</p>
                    <p className="mt-1 text-xl">{kpi?.medico_lider?.name||'—'}</p>
                    <p>{kpi?.medico_lider?.horas||0} horas</p>
                  </WhiteCard>

                  <WhiteCard className="text-center p-2">
                    <p className="text-xl text-black font-bold mb-2">Ranking de Médicos</p>
                    <ol className="list-decimal list-inside space-y-1 text-l pr-10">
                      {(kpi?.ranking_medicos ?? []).map(b => (
                        <li key={b.id}>{b.id} – {b.horas} horas</li>
                      ))}
                    </ol>
                  </WhiteCard>
                </div>

                <div className='grid grid-cols-1 md:grid-cols-2 gap-4'>
                  <WhiteCard className="text-center p-6">
                    <p className="text-xl text-black font-bold">Box líder</p>
                    <p className="mt-1 text-xl">
                      Box {kpi?.box_mayor_uso?.id || '—'}
                    </p>
                    <p>{kpi?.box_mayor_uso?.horas || 0} horas</p>
                  </WhiteCard>

                  <WhiteCard className="text-center p-6">
                    <p className="text-xl text-black font-bold mb-2">Ranking de Boxes</p>
                    <ol className="list-decimal list-inside space-y-1 text-l pr-10">
                      {(kpi?.ranking_boxes ?? []).map(b => (
                        <li key={b.id}>Box {b.id} – {b.horas} horas</li>
                      ))}
                    </ol>
                  </WhiteCard>
                </div>

                  <WhiteCard className="text-center p-6">
                    <p className="text-xl text-black font-bold">Especialidad más demandada</p>
                    <p className="mt-1 text-xl">
                      {kpi?.especialidad_mas_demanda?.name || '—'}
                    </p>
                    <p>{kpi?.especialidad_mas_demanda?.horas || 0} horas</p>
                  </WhiteCard>

                  
                </div>

                {/* 3. Gráfico circular */}
                <WhiteCard className="flex flex-col items-center">
                  <h3 className="mb-4 font-semibold">Horas por especialidad</h3>
                  <div className="w-full h-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={pieData}
                          dataKey="value"
                          nameKey="name"
                          outerRadius="70%"
                          label
                        >
                          {pieData.map((_, i) => (
                            <Cell key={i} fill={COLORS[i % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend verticalAlign="bottom" height={100} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </WhiteCard>

              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
