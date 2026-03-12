import { LoginForm } from '../components/LoginForm';
import { useTheme } from '../contexts/ThemeContext';
import '../styles/AuthPage.css';

export const LoginPage = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="auth-page">
      <button className="theme-toggle" onClick={toggleTheme}>
        {theme === 'light' ? '🌙' : '☀️'}
      </button>
      <div className="auth-page-content">
        <div className="auth-page-header">
          <h1>Agentic Sales Outreach</h1>
          <p>Welcome back! Login to continue</p>
        </div>
        <LoginForm />
      </div>
    </div>
  );
};
