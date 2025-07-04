import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import AIGreeting from './components/AIGreeting';
import BalanceCard from './components/BalanceCard';
import QuickStats from './components/QuickStats';
import SpendingBreakdown from './components/SpendingBreakdown';
import QuickActions from './components/QuickActions';
import ChatArea from './components/ChatArea';
import BottomNav from './components/BottomNav';
import './App.css';
import PromptEditor from "./PromptEditor";
import PromptPractice from './components/PromptPractice';

// Dummy components for each page (replace with your real content as you build)
function HomePage() {
  return (
    <>
      <AIGreeting />
      <BalanceCard />
      <QuickStats />
      <SpendingBreakdown />
      <QuickActions />
    </>
  );
}
function StatsPage() {
  return <div style={{ padding: 32 }}>📊 Stats Page (Coming Soon)</div>;
}
function ChatPage() {
  return <ChatArea />;
}
function GoalsPage() {
  return <div style={{ padding: 32 }}>🎯 Goals Page (Coming Soon)</div>;
}
function ProfilePage() {
  return <div style={{ padding: 32 }}>👤 Profile Page (Coming Soon)</div>;
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/stats" element={<StatsPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/goals" element={<GoalsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/admin" element={<PromptEditor />} /> {/* <-- Admin route for prompt editing */}
          <Route path="/practice" element={<PromptPractice />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
        <BottomNav />
      </div>
    </Router>
  );
}

export default App;
