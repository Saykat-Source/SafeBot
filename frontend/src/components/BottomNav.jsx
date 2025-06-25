import { Link, useLocation } from 'react-router-dom';
import styles from '../styles/BottomNav.module.css';

export default function BottomNav() {
  const location = useLocation();
  return (
    <nav className={styles.nav}>
      <Link
        to="/"
        className={`${styles.tab} ${location.pathname === '/' ? styles.active : ''}`}
      >
        🏠
        <span>Home</span>
      </Link>
      <Link
        to="/stats"
        className={`${styles.tab} ${location.pathname === '/stats' ? styles.active : ''}`}
      >
        📊
        <span>Stats</span>
      </Link>
      <Link
        to="/chat"
        className={`${styles.tab} ${location.pathname === '/chat' ? styles.active : ''}`}
      >
        💬
        <span>Chat</span>
      </Link>
      <Link
        to="/goals"
        className={`${styles.tab} ${location.pathname === '/goals' ? styles.active : ''}`}
      >
        🎯
        <span>Goals</span>
      </Link>
      <Link
        to="/profile"
        className={`${styles.tab} ${location.pathname === '/profile' ? styles.active : ''}`}
      >
        👤
        <span>Profile</span>
      </Link>
    </nav>
  );
}
