// React
import { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";

// React hooks
import useBoxesSSE from "../hooks/useBoxesSSE";
import useBoxFilters from "../hooks/useBoxFilters";

// Components
import Offcanvas      from "../components/Offcanvas";
import HeaderTop from "../components/HeaderTop";
import HeaderBottom from "../components/HeaderBottom";
import FiltersPanel   from "../components/FiltersPanel";
import Sidebar from "../components/Sidebar";
import BoxCard from "../components/BoxCard";

// Assets
import bg from "../assets/images/login-bg.png";


export default function Dashboard() {
  const [date, setDate] = useState(new Date());
  const [filters, setFilters] = useState({
    disponibilidad: "ALL",
    po:            "ALL",
    box:           "ALL",
    pasillo:       "ALL",
    medico:        "ALL",
  });
  const [showFilters, setShowFilters] = useState(false);

  /* ---------------- datos desde el backend ---------------- */
  const boxes = useBoxesSSE(date);              // SSE en tiempo real
  const { filteredBoxes } = useBoxFilters(boxes, filters);

  /* ---------------- listas únicas para los combos ---------------- */
  const pasillos = useMemo(
    () => [...new Set(boxes.map(b => b.pasillo))].filter(Boolean).sort(),
    [boxes]
  );
  const boxNums = useMemo(
    () => [...new Set(boxes.map(b => b.idBox))].sort((a, b) => a - b),
    [boxes]
  );
  const medicos = useMemo(
    () => [...new Set(boxes.map(b => b.medicoAsignado).filter(Boolean))].sort(),
    [boxes]
  );

  const navigate = useNavigate();

  /* ---------------- agrupar tarjetas por pasillo ---------------- */
  const boxesByPasillo = useMemo(() => {
    return filteredBoxes.reduce((acc, box) => {
      const p = box.pasillo || "Sin pasillo";
      acc[p] = acc[p] || [];
      acc[p].push(box);
      return acc;
    }, {});
  }, [filteredBoxes]);

  /* ============================================================= */
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar className="flex-none w-14 pt-21" />

      <div className="relative flex-1 flex flex-col">
        {/* fondo difuminado */}
        <div
          className="absolute inset-0 -z-10 bg-cover bg-center opacity-70"
          style={{ backgroundImage: `url(${bg})` }}
        />

        <HeaderTop />

        <HeaderBottom
          date={date}
          setDate={setDate}
          onOpenFilters={() => setShowFilters(true)}
        />

        {/* ---------------- listados de boxes ---------------- */}
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
                          navigate(
                            `/detalle-box/${box.idBox}?date=${date
                              .toISOString()
                              .slice(0, 10)}`
                          )
                        }
                      />
                    ))}
                  </div>
                </section>
              ))}
          </div>
        </main>
      </div>

      {/* ---------------- panel off-canvas con filtros ---------------- */}
      <Offcanvas open={showFilters} onClose={() => setShowFilters(false)}>
        <h2 className="text-xl font-semibold mb-4">Filtros</h2>

        <FiltersPanel
          date={date}
          setDate={setDate}          // si quieres permitir fecha dentro del panel tmb.
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