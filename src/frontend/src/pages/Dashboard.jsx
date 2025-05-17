import React from 'react';
import useBoxesSSE from '../hooks/useBoxesSSE';
import BoxCard from '../components/BoxCard';

export default function Dashboard() {
  const boxes = useBoxesSSE();  // ya no recibe interval

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* header, logout, título... */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {boxes.map(box => (
          <BoxCard
            key={box.idBox}
            numero={box.numeroBox}
            tipo={box.tipoBox}
            disponibilidad={box.disponibilidad}
          />
        ))}
      </div>
    </div>
  );
}
