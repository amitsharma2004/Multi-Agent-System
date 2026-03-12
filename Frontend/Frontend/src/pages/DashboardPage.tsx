import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useTheme } from '../contexts/ThemeContext';
import '../styles/Dashboard.css';

export const DashboardPage = () => {
  const { user, logout } = useAuthStore();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Dashboard</h1>
        <div className="header-actions">
          <button className="theme-toggle" onClick={toggleTheme}>
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </header>
      
      <div className="dashboard-content">
        <div className="welcome-card">
          <h2>Welcome, {user?.full_name}!</h2>
          <p>Email: {user?.email}</p>
          <p>Role: {user?.role}</p>
        </div>
        
        <div className="info-card">
          <h3>🚀 Coming Soon</h3>
          <p>Lead management and AI agent features will be available here.</p>
        </div>
      </div>
    </div>
  );
};
