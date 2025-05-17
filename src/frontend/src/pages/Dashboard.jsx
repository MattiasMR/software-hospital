import { useState } from "react";
import useBoxesSSE from "../hooks/useBoxesSSE";
import useBoxFilters from "../hooks/useBoxFilters";
import Sidebar from "../components/Sidebar";
import HeaderTop from "../components/HeaderTop";
import HeaderBottom from "../components/HeaderBottom";
import BoxCard from "../components/BoxCard";
import bg from "../assets/images/login-bg.png";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [date, setDate] = useState(new Date());
  const boxes = useBoxesSSE(date); // soporte para fecha
  const { filters, setFilters, filteredBoxes } = useBoxFilters(boxes);
  const navigate = useNavigate();

  // Agrupar por pasillo
  const boxesByPasillo = filteredBoxes.reduce((acc, box) => {
    const p = box.pasillo || "Sin pasillo";
    acc[p] = acc[p] || [];
    acc[p].push(box);
    return acc;
  }, {});

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar className="flex-none w-16" />

      <div className="relative flex-1 flex flex-col">
        <div className="absolute inset-0 bg-cover bg-center opacity-70 -z-10" style={{ backgroundImage: `url(${bg})` }} />

        <HeaderTop />

        <HeaderBottom
          date={date}
          onDateChange={setDate}
          filters={filters}
          setFilters={setFilters}
          boxes={boxes}
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
                        numero={box.numeroBox ?? box.idBox}
                        tipo={box.tipoBox}
                        disponibilidad={box.disponibilidad}
                        medico={box.medicoAsignado}
                        porcentajeOcupacion={box.porcentajeOcupacion}
                        onClick={() => navigate(`/detalle-box/${box.idBox}`)}
                      />
                    ))}
                  </div>
                </section>
              ))}
          </div>
        </main>
      </div>
    </div>
  );
}
