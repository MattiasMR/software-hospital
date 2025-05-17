// src/components/BoxCard.jsx
export default function BoxCard({ numero, tipo, disponibilidad }) {
  const color =
    disponibilidad === 'Libre'
      ? 'bg-green-200'
      : disponibilidad === 'Ocupado'
      ? 'bg-red-200'
      : 'bg-gray-200';

  return (
    <div className={`p-4 rounded-2xl shadow ${color}`}>
      <h3 className="text-xl font-semibold mb-2">Box {numero}</h3>
      <p className="text-sm mb-1"><strong>Tipo:</strong> {tipo}</p>
      <p className="text-sm"><strong>Estado:</strong> {disponibilidad}</p>
    </div>
  );
}
