import styles from '../styles/QuickActions.module.css';

export default function QuickActions() {
  return (
    <div className={styles.actionsRow}>
      <button className={styles.action}>Set Budget</button>
      <button className={styles.action}>Track Bills</button>
      <button className={styles.action}>Round-Up Savings</button>
      <button className={styles.action}>Check Credit Score</button>
    </div>
  );
}
