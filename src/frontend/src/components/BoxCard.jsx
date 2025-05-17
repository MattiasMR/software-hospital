export default function BoxCard({
  id,
  numero,
  tipo,
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

  // Color dinámico para el porcentaje
  let colorPct = "#16a34a"; // verde
  if (porcentajeOcupacion >= 80) colorPct = "#dc2626";      // rojo
  else if (porcentajeOcupacion >= 50) colorPct = "#eab308"; // amarillo

  return (
    <div
      className="bg-white rounded-2xl aspect-square p-6 flex flex-col justify-between shadow-md cursor-pointer hover:shadow-xl transition"
      onClick={onClick}
    >
      <h3 className="text-xl font-bold text-center">Box {displayNum}</h3>
      <div className="flex flex-col items-center space-y-2">
        <span className={`inline-block h-3 w-3 rounded-full ${dotColor}`} />
        {disponibilidad === 'Ocupado' && medico
          ? <p className="text-sm font-medium">Médico: {medico}</p>
          : <p className="text-sm font-medium">{disponibilidad}</p>
        }
      </div>
      {/* Nueva barra de ocupación profesional */}
      <div className="mt-2">
        <div className="w-full h-2 rounded-2xl bg-green-400 relative overflow-hidden">
          <div
            className="absolute left-0 top-0 h-full bg-red-500 transition-all duration-500"
            style={{ width: `${porcentajeOcupacion}%` }}
          />
        </div>
        <div className="flex justify-center text-xs mt-1">
          <span className="font-semibold" >
            Ocupación: {porcentajeOcupacion}%
          </span>
        </div>
      </div>
    </div>
  );
}
