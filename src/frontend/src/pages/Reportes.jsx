import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import HeaderTop from "../components/HeaderTop";
import WhiteCard from "../components/WhiteCard";
import bg from "../assets/images/login-bg.png";

export default function Reportes() {
  const [loading, setLoading] = useState(true);
  const [kpi, setKpi] = useState(null);
  const [error, setError] = useState(null);
  const [dateFrom, setDateFrom] = useState(new Date());
  const [dateTo, setDateTo] = useState(new Date());

  useEffect(() => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    const dFrom = dateFrom.toISOString().slice(0, 10);
    const dTo = dateTo.toISOString().slice(0, 10);

    fetch(
      `http://127.0.0.1:8000/api/boxes/reportes/?date_from=${dFrom}&date_to=${dTo}`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
      .then((res) => {
        if (!res.ok) throw new Error("Error al cargar el reporte");
        return res.json();
      })
      .then((data) => {
        setKpi(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [dateFrom, dateTo]);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar className="flex-none w-16" />
      <div className="relative flex-1 flex flex-col">
        <div className="absolute inset-0 bg-cover bg-center opacity-70 -z-10" style={{ backgroundImage: `url(${bg})` }} />

        <HeaderTop />
        <main className="flex-1 overflow-auto py-8">
          <div className="max-w-screen-md mx-auto px-4">
            <WhiteCard>
              <h1 className="text-2xl font-bold mb-4">Reporte de KPIs</h1>
              <div className="flex gap-4 mb-4">
                <input
                  type="date"
                  value={dateFrom.toISOString().slice(0, 10)}
                  onChange={e => setDateFrom(new Date(e.target.value))}
                  className="border rounded px-2 py-1"
                />
                <input
                  type="date"
                  value={dateTo.toISOString().slice(0, 10)}
                  onChange={e => setDateTo(new Date(e.target.value))}
                  className="border rounded px-2 py-1"
                />
              </div>
              {loading ? (
                <p>Cargando...</p>
              ) : error ? (
                <p className="text-red-600">{error}</p>
              ) : kpi ? (
                <div>
                  <p><b>% Ocupación global:</b> {kpi.porcentaje_ocupacion}%</p>
                  <p className="mt-4 font-semibold">Tiempos muertos por box (min):</p>
                  <ul className="ml-6">
                    {Object.entries(kpi.tiempos_muertos).map(([id, mins]) => (
                      <li key={id}>Box {id}: {mins} min</li>
                    ))}
                  </ul>
                  <p className="mt-4 font-semibold">Uso por especialidad:</p>
                  <ul className="ml-6">
                    {Object.entries(kpi.uso_por_especialidad).map(([esp, usos]) => (
                      <li key={esp}>{esp}: {usos} consultas</li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </WhiteCard>
          </div>
        </main>
      </div>
    </div>
  );
}
