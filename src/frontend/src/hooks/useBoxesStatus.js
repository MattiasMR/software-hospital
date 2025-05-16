import { useState, useEffect, useRef } from 'react';

export default function useBoxesStatus(intervalMs = 1000) {
  const [boxes, setBoxes] = useState([]);
  const intervalRef = useRef(null); 

  const fetchBoxes = async () => {
    const token = localStorage.getItem('accessToken');
    if (!token) return;

    try {
      const res = await fetch('http://127.0.0.1:8000/api/boxes/status/', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setBoxes(await res.json());
    } catch (err) {
      console.error('Error fetching boxes status:', err);
    }
  };

  useEffect(() => {
    fetchBoxes();                            // llamada inmediata
    intervalRef.current = setInterval(fetchBoxes, intervalMs);
    return () => clearInterval(intervalRef.current);
  }, [intervalMs]);

  return boxes;
}
