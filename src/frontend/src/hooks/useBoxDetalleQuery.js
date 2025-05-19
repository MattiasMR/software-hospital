import { useQuery } from '@tanstack/react-query';

const formatDate = date => {
  const d = typeof date === 'string' ? new Date(date) : date;
  const year  = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day   = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const fetchBoxDetalle = async ({ queryKey }) => {
  const [_key, idBox, dateStr, token] = queryKey;
  const res = await fetch(
    `http://127.0.0.1:8000/api/boxes/${idBox}/detalle/?date=${dateStr}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );

  if (res.status === 401) {
    localStorage.removeItem('accessToken');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }

  if (!res.ok) {
    throw new Error(`Error ${res.status} al obtener detalle`);
  }

  return res.json();
};

export function useBoxDetalleQuery(idBox, date) {
  const token   = localStorage.getItem('accessToken') || '';
  const dateStr = formatDate(date);

  return useQuery({
    queryKey: ['boxDetalle', idBox, dateStr, token],
    queryFn: fetchBoxDetalle,
    staleTime: 1000 * 60,
    cacheTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
    refetchInterval: 5000,
    retry: 1,
  });
}
