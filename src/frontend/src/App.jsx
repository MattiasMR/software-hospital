// src/App.jsx

import { BrowserRouter, Routes, Route, Navigate, useParams, useLocation } from 'react-router-dom';
import Login      from './pages/Login';
import Dashboard  from './pages/Dashboard';
import Reportes   from './pages/Reportes';
import DetalleBox from './pages/DetalleBox';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('accessToken');
  // 1️⃣ si no hay token, renderiza <Navigate> en render y sal
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function DetalleBoxPage() {
  // La página detalle se monta una sola vez con estos params
  const { idBox } = useParams();
  const params    = new URLSearchParams(useLocation().search);
  const date      = params.get('date') || new Date().toISOString().slice(0, 10);
  return <DetalleBox idBox={idBox} fecha={date} />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ruta pública de login */}
        <Route path="/login" element={<Login />} />

        {/* rutas protegidas */}
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/reportes"
          element={
            <PrivateRoute>
              <Reportes />
            </PrivateRoute>
          }
        />
        <Route
          path="/detalle-box/:idBox"
          element={
            <PrivateRoute>
              <DetalleBoxPage />
            </PrivateRoute>
          }
        />

        {/* cualquier otra ruta → login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
);
}
