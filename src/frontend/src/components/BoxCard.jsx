export default function BoxCard({
  id,
  numero,
  disponibilidad,
  medico,
  porcentajeOcupacion = 0,
  onClick
}) {
  let dotColor = 'bg-gray-400';
  if (disponibilidad === 'Ocupado') dotColor = 'bg-red-500';
  else if (disponibilidad === 'Libre') dotColor = 'bg-green-500';
  else if (disponibilidad === 'Inhabilitado') dotColor = 'bg-yellow-500';

  const displayNum = numero ?? id;

  // Color dinámico para la barra porcentaje
  let colorPct = "#16a34a"; // verde
  if (porcentajeOcupacion >= 80) colorPct = "#dc2626";      // rojo
  else if (porcentajeOcupacion >= 50) colorPct = "#eab308"; // amarillo

  return (
    <div
      className="bg-white rounded-2xl aspect-square p-6 flex flex-col justify-between shadow-md cursor-pointer hover:shadow-xl transition"
      onClick={onClick}
    >
      <h3 className="text-xl font-bold text-center mb-2">Box {displayNum}</h3>
      <div className="flex items-center justify-center gap-2 mb-4">
        <span className={`inline-block h-3 w-3 rounded-full ${dotColor}`} />
        <span className="text-sm font-medium">{disponibilidad}</span>
      </div>
      <div className="mt-auto">
        <div className="w-full h-2 rounded-2xl bg-green-400 relative overflow-hidden">
          <div
            className="absolute left-0 top-0 h-full bg-red-500 transition-all duration-500"
            style={{ width: `${porcentajeOcupacion}%` }}
          />
        </div>
        <div className="flex justify-center text-m mt-1">
          <span>
            Ocupación: {porcentajeOcupacion}%
          </span>
        </div>
      </div>
    </div>
  );
}
