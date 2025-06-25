import styles from '../styles/QuickStats.module.css';

export default function QuickStats() {
  return (
    <div className={styles.statsRow}>
      <div className={styles.statCard}>
        <div className={styles.label}>Spent this month</div>
        <div className={styles.value}>$1,200</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.label}>Savings progress</div>
        <div className={styles.value}>67%</div>
      </div>
      <div className={styles.statCard}>
        <div className={styles.label}>Bills due</div>
        <div className={styles.value}>3</div>
      </div>
    </div>
  );
}
