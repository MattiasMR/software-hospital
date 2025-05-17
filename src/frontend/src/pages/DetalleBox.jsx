import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import HeaderTop from "../components/HeaderTop";
import WhiteCard from "../components/WhiteCard";
import DonutOcupacion from "../components/DonutOcupacion";
import bg from "../assets/images/login-bg.png";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

export default function DetalleBox() {
  const { idBox } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const dateFromQuery = queryParams.get("date");
  const [box, setBox] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [date, setDate] = useState(dateFromQuery ? new Date(dateFromQuery) : new Date());

  useEffect(() => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    const d = date.toISOString().slice(0, 10);
    fetch(`http://127.0.0.1:8000/api/boxes/${idBox}/detalle/?date=${d}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Error al cargar box");
        return res.json();
      })
      .then((data) => {
        setBox(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [idBox, date]);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar className="flex-none w-16" />
      <div className="relative flex-1 flex flex-col">
        <div
          className="absolute inset-0 bg-cover bg-center opacity-70 -z-10"
          style={{ backgroundImage: `url(${bg})` }}
        />
        <HeaderTop />
        <main className="flex-1 overflow-auto py-8">
          <div className="max-w-screen-md mx-auto px-4">
            <WhiteCard>
              <button
                className="mb-4 text-cyan-600 underline"
                onClick={() => navigate(-1)}
              >
                ← Volver
              </button>

              {/* Filtro de fecha visible */}
              <div className="mb-4">
                <DatePicker
                  selected={date}
                  onChange={setDate}
                  dateFormat="yyyy-MM-dd"
                  className="border rounded px-2 py-1 text-sm bg-white"
                />
                <span className="ml-3 text-gray-600 text-sm">Filtrar por fecha</span>
              </div>

              {loading ? (
                <p>Cargando...</p>
              ) : error ? (
                <p className="text-red-600">{error}</p>
              ) : box ? (
                <div>
                  {/* Datos principales y gráfico */}
                  <div className="flex flex-wrap items-center mb-6">
                    <div className="flex-1 min-w-[210px]">
                      <h1 className="text-2xl font-bold mb-2">
                        Box {box.idBox}
                      </h1>
                      <p>
                        <b>Pasillo:</b> {box.pasillo}
                      </p>
                    </div>
                    <DonutOcupacion porcentaje={box.porcentajeOcupacion} />
                  </div>
                  <h2 className="text-xl font-bold mt-6 mb-2">
                    Franjas horarias del día
                  </h2>
                  <table className="min-w-full table-auto border-collapse mt-2">
                    <thead>
                      <tr className="bg-gray-200">
                        <th className="px-3 py-1 text-left">Inicio</th>
                        <th className="px-3 py-1 text-left">Fin</th>
                        <th className="px-3 py-1 text-left">Médico</th>
                        <th className="px-3 py-1 text-left">Especialidad</th>
                        <th className="px-3 py-1 text-left">Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {box.franjas.length === 0 ? (
                        <tr>
                          <td colSpan={5} className="text-center text-gray-500 py-4">
                            No hay franjas para este día.
                          </td>
                        </tr>
                      ) : (
                        box.franjas.map((f, i) => (
                          <tr key={i}>
                            <td>{f.inicio}</td>
                            <td>{f.fin}</td>
                            <td>{f.medico}</td>
                            <td>{f.especialidad}</td>
                            <td>{f.estado}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              ) : null}
            </WhiteCard>
          </div>
        </main>
      </div>
    </div>
  );
}