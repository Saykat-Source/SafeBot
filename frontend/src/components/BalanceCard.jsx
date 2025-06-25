import styles from '../styles/BalanceCard.module.css';

export default function BalanceCard() {
  return (
    <section className={styles.card}>
      <div className={styles.balanceLabel}>Account Balance</div>
      <div className={styles.balance}>$2,847.50</div>
      <div className={styles.leftToSpend}>💰 $420 left to spend</div>
    </section>
  );
}
