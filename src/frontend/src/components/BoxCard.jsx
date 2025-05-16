export default function BoxCard({ numero, tipo, disponibilidad }) {
  // Colores según disponibilidad
  const color = disponibilidad === 'Libre'
    ? 'bg-green-200'
    : disponibilidad === 'Ocupado'
    ? 'bg-red-200'
    : 'bg-gray-200';

  return (
    <div className={`p-4 rounded shadow ${color}`}>
      <h3 className="text-xl font-semibold">Box {numero}</h3>
      <p>Tipo: {tipo}</p>
      <p>Estado: {disponibilidad}</p>
    </div>
  );
}
