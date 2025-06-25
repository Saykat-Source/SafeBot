import styles from '../styles/AIGreeting.module.css';

export default function AIGreeting() {
  return (
    <div className={styles.greetingCard}>
      <span className={styles.avatar} role="img" aria-label="AI">🤖</span>
      <div>
        <div className={styles.greeting}>G'day, Sarah!</div>
        <div className={styles.subtitle}>Your money mate</div>
      </div>
    </div>
  );
}
