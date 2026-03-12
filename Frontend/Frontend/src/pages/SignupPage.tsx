import { SignupForm } from '../components/SignupForm';
import { useTheme } from '../contexts/ThemeContext';
import '../styles/AuthPage.css';

export const SignupPage = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="auth-page">
      <button className="theme-toggle" onClick={toggleTheme}>
        {theme === 'light' ? '🌙' : '☀️'}
      </button>
      <div className="auth-page-content">
        <div className="auth-page-header">
          <h1>Agentic Sales Outreach</h1>
          <p>Create your account to get started</p>
        </div>
        <SignupForm />
      </div>
    </div>
  );
};
