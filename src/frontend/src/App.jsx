import { BrowserRouter, Routes, Route, Navigate, useParams, useLocation } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Reportes from './pages/Reportes';
import DetalleBox from './pages/DetalleBox';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('accessToken');
  return token ? children : <Navigate to="/login" replace />;
}

function DetalleBoxPage() {
  const { idBox } = useParams();
  const params = new URLSearchParams(useLocation().search);
  const fecha = params.get("date") || new Date().toISOString().slice(0, 10);
  return <DetalleBox idBox={idBox} fecha={fecha} />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
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

        {/* Redirige cualquier otra ruta a login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
