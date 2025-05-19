import { useQuery } from '@tanstack/react-query';

const formatDate = date => {
  const year  = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day   = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const fetchBoxes = async (dateStr, token) => {
  
  const res = await fetch(
    `http://127.0.0.1:8000/api/boxes/status/?date=${dateStr}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );

  if (res.status === 401) {
    // 🚨 Al primer 401: limpiamos y redirigimos
    localStorage.removeItem('accessToken');
    window.location.href = '/login';
    // Lanzamos para que React Query no procese más esta promesa
    throw new Error('Unauthorized');
  }

  if (!res.ok) {
    throw new Error(`Error ${res.status} al obtener boxes`);
  }

  return res.json();
};
export { fetchBoxes, formatDate };
export function useBoxesQuery(date) {
  const token   = localStorage.getItem('accessToken') || '';
  const dateStr = formatDate(date);

  return useQuery({
    queryKey: ['boxes', dateStr],
    queryFn: () => fetchBoxes(dateStr, token),
    staleTime: 1000 * 60,
    cacheTime: 1000 * 60 * 15,
    refetchOnWindowFocus: false,
    refetchInterval: 1000,
    retry: 1,
    keepPreviousData: true,
  });
}
