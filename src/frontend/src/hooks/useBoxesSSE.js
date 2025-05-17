import { useState, useEffect } from 'react';

export default function useBoxesSSE(date) {
  const [boxes, setBoxes] = useState([]);

  useEffect(() => {
    const params = date
      ? `?date=${date.toISOString().slice(0, 10)}`
      : '';
    const evtSource = new EventSource(
      `http://127.0.0.1:8000/api/boxes/stream/${params}`
    );

    evtSource.onmessage = e => {
      try {
        setBoxes(JSON.parse(e.data));
      } catch (err) {
        setBoxes([]);
      }
    };

    evtSource.onerror = err => {
      evtSource.close();
    };

    return () => {
      evtSource.close();
    };
  }, [date]);

  return boxes;
}
