import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import bg from '../assets/images/login-bg.png';
import logo from '../assets/images/hospital-logo.png';
import errorIcon from '../assets/images/error-icon.png';
import WhiteCard from '../components/WhiteCard';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        const payload = await res.json();
        throw new Error(payload.detail || 'Credenciales inválidas');
      }
      const { access } = await res.json();
      localStorage.setItem('accessToken', access);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center">
      {/* Imagen de fondo */}
      <div
        className="absolute inset-0 w-full h-full bg-cover bg-center opacity-70"
        style={{ backgroundImage: `url(${bg})` }}
      />

      {/* Contenedor de la tarjeta */}
      <div className="relative z-10 w-[90%] max-w-[600px] px-4">
        <WhiteCard>
          <div className="flex justify-center mb-6">
            <img src={logo} alt="Hospital logo" className="w-44" />
          </div>

          {error && (
            <div className="flex items-center bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6 text-sm">
              <img src={errorIcon} alt="Error" className="h-5 w-5 mr-3" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              autoComplete="username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Correo electrónico"
              required
              className="w-full px-4 py-3 bg-gray-200 rounded-full text-sm outline-none"
            />
            <input
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Contraseña"
              required
              className="w-full px-4 py-3 bg-gray-200 rounded-full text-sm outline-none"
            />
            <button
              type="submit"
              className="w-full py-3 bg-cyan-500 text-white rounded-full font-semibold hover:bg-cyan-600 transition"
            >
              Inicio de sesión
            </button>
          </form>

          <div className="text-center mt-6">
            <a href="#" className="text-sm text-gray-700 underline">
              ¿Olvidó su contraseña?
            </a>
          </div>
        </WhiteCard>
      </div>
    </div>
  );
}
