// src/hooks/useBoxDetalleQuery.js
import { useQuery } from '@tanstack/react-query';

const formatDate = date => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return [
    d.getFullYear(),
    String(d.getMonth()+1).padStart(2,'0'),
    String(d.getDate()).padStart(2,'0'),
  ].join('-');
};

async function fetchBoxDetalle({ queryKey }) {
  const [_key, idBox, dateStr, token] = queryKey;
  const res = await fetch(
    `http://127.0.0.1:8000/api/boxes/${idBox}/detalle-v2/?date=${dateStr}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  if (!res.ok) throw new Error(`Error ${res.status} al obtener detalle`);
  return res.json();
}

export function useBoxDetalleQuery(idBox, date) {
  const token = localStorage.getItem('accessToken') || '';
  const dateStr = formatDate(date);
  return useQuery({
    queryKey: ['boxDetalleV2', idBox, dateStr, token],
    queryFn: fetchBoxDetalle,
    staleTime: 60_000,
    refetchInterval: 5000,
  });
}
