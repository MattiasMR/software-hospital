import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import bg from '../assets/images/login-bg.png';
import logo from '../assets/images/hospital-logo.png';
import errorIcon from '../assets/images/error-icon.png';
import WhiteCard from '../components/WhiteCard';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  // Si ya hay token, salta directo a dashboard
  // useEffect(() => {
  //   if (localStorage.getItem('accessToken')) {
  //     navigate('/dashboard');
  //   }
  // }, [navigate]);

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/token/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        if (res.status === 401) {
          throw new Error("Credenciales inválidas");
        }
        const payload = await res.json().catch(() => null);
        throw new Error(payload?.detail || 'Error inesperado');
      }
      const { access } = await res.json();
      localStorage.setItem('accessToken', access);
      setSubmitting(false);
      navigate('/resumen');
    } catch (err) {
      setError(err.message || "Error de red");
      setSubmitting(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center">

      <div
        className="absolute inset-0 w-full h-full bg-cover bg-center opacity-70"
        style={{ backgroundImage: `url(${bg})` }}
      />


      <div className="relative z-10 w-[90%] max-w-[600px] px-4">
        <WhiteCard className='p-20'>
          
          <div className="flex justify-center mb-6">
            <img src={logo} alt="Hospital logo" className="w-70" />
          </div>

          {error && (
            <div className="flex items-center bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 text-sm" role="alert">
              <img src={errorIcon} alt="Error" className="h-5 w-5 mr-3" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 flex flex-col items-center" autoComplete="on">
            <input
              type="text"
              autoComplete="username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Nombre de usuario"
              required
              disabled={submitting}
              className="w-full px-4 py-3 bg-gray-200 rounded-full text-sm outline-none"
              aria-label="Nombre de usuario"
            />
            <input
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Contraseña"
              required
              disabled={submitting}
              className="w-full px-4 py-3 bg-gray-200 rounded-full text-sm outline-none"
              aria-label="Contraseña"
            />
            <button
              type="submit"
              className="w-[calc(100%-5rem)] px-4 py-3 bg-cyan-500 text-white rounded-full font-semibold hover:bg-cyan-600 transition disabled:opacity-50"
              disabled={submitting}
            >
              {submitting ? "Iniciando sesión..." : "Inicio de sesión"}
            </button>
          </form>

          <div className="text-center mt-6">
            <a href="#" className="text-sm text-gray-700 underline pointer-events-none opacity-60">
              ¿Olvidó su contraseña?
            </a>
          </div>
        </WhiteCard>
      </div>
    </div>
  );
}
