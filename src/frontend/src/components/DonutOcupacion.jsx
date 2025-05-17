import { PieChart } from "react-minimal-pie-chart";
import { Tooltip } from "react-tooltip";
import { useRef } from "react";

export default function DonutOcupacion({ porcentaje }) {
  const safePorcentaje = Math.max(0, Math.min(100, Number(porcentaje) || 0));
  const tooltipId = useRef("donut-tooltip-" + Math.random());

  return (
    <div className="w-40 flex flex-col items-center">
      <div
        data-tooltip-id={tooltipId.current}
        data-tooltip-content={
          `Ocupado: ${safePorcentaje}%\nLibre: ${100 - safePorcentaje}%`
        }
      >
        <div className="w-40 flex flex-col items-center relative">
          <div className="relative" style={{ width: 130, height: 130 }}>
            <PieChart
              data={[
                {
                  title: "Ocupado",
                  value: safePorcentaje,
                  color: "#ef4444",
                },
                {
                  title: "Libre",
                  value: 100 - safePorcentaje,
                  color: "#22c55e",
                },
              ]}
              lineWidth={18}
              rounded
              startAngle={-90}
              totalValue={100}
              style={{ height: "130px", width: "130px", cursor: "pointer" }}
              segmentsStyle={{ cursor: "pointer" }}
            />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none select-none"
              style={{ fontSize: "1.4em", fontWeight: "bold", color: "#333" }}>
              {safePorcentaje}%
            </div>
          </div>
          <Tooltip id={tooltipId.current} />
          <span className="text-center text-sm mt-2 text-gray-700">
            PO (porcentaje ocupación)
          </span>
        </div>
      </div>
      <Tooltip id={tooltipId.current} />
    </div>
  );
}
