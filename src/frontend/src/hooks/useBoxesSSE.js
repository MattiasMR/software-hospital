import { useState, useEffect } from 'react';

export default function useBoxesSSE() {
  const [boxes, setBoxes] = useState([]);

  useEffect(() => {
    // Conecta al endpoint SSE
    const evtSource = new EventSource('http://127.0.0.1:8000/api/boxes/stream/');

    evtSource.onmessage = e => {
      try {
        setBoxes(JSON.parse(e.data));
      } catch (err) {
        console.error('Error parseando SSE:', err);
      }
    };

    evtSource.onerror = err => {
      console.error('Error SSE:', err);
      // si quieres reconectar automáticamente:
      // evtSource.close();
      // setTimeout(() => {/* reabrir EventSource */}, 5000);
    };

    return () => {
      evtSource.close();
    };
  }, []);

  return boxes;
}
