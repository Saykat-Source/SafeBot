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

// ... (dummy components as before)

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <Routes>
          <Route path="/" element={<PromptPractice />} /> {/* <-- Prompt Checker is now the home page */}
          <Route path="/stats" element={<StatsPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/goals" element={<GoalsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/admin" element={<PromptEditor />} />
          <Route path="/practice" element={<PromptPractice />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
        <BottomNav />
      </div>
    </Router>
  );
}

export default App;
