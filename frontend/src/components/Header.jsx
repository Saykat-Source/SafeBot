import styles from '../styles/Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <button className={styles.menu}>☰</button>
      <div className={styles.title}>FinPal AU</div>
      <div className={styles.actions}>
        <button className={styles.icon}>🔔</button>
        <button className={styles.icon}>⚙️</button>
      </div>
    </header>
  );
}
