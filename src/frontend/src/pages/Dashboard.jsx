import useBoxesStatus from '../hooks/useBoxesStatus';
import BoxCard from '../components/BoxCard';

export default function Dashboard() {
  const boxes = useBoxesStatus(5000);

  return (
    <div className="p-6 grid grid-cols-2 gap-4">
      {boxes.map(box => (
        <BoxCard
          key={box.idBox}
          numero={box.numeroBox}
          tipo={box.tipoBox.tipoBox}
          disponibilidad={box.disponibilidad.disponibilidad}
        />
      ))}
    </div>
  );
}
