import styles from '../styles/SpendingBreakdown.module.css';

export default function SpendingBreakdown() {
  return (
    <section className={styles.breakdownCard}>
      <div className={styles.title}>Spending Breakdown</div>
      <div className={styles.chartPlaceholder}>
        {/* Chart will go here in the future */}
        <span role="img" aria-label="pie chart" style={{ fontSize: '2.2rem' }}>🥧</span>
      </div>
      <ul className={styles.categoryList}>
        <li><span className={styles.category}>🍔 Food</span> <span className={styles.amount}>$420</span></li>
        <li><span className={styles.category}>🚗 Transport</span> <span className={styles.amount}>$180</span></li>
        <li><span className={styles.category}>🏠 Bills</span> <span className={styles.amount}>$650</span></li>
        <li><span className={styles.category}>🛒 Shopping</span> <span className={styles.amount}>$290</span></li>
      </ul>
    </section>
  );
}
