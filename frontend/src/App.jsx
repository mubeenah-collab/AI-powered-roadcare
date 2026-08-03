import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import CitizenLayout from './layouts/CitizenLayout';
import AdminLayout from './layouts/AdminLayout';
import HomePage from './pages/HomePage';
import ReportDamagePage from './pages/ReportDamagePage';
import TrackComplaintPage from './pages/TrackComplaintPage';
import AdminDashboardPage from './pages/AdminDashboardPage';
import AdminAnalyticsPage from './pages/AdminAnalyticsPage';
import AdminComplaintsPage from './pages/AdminComplaintsPage';

export function App() {
  return (
    <Router>
      <Routes>
        {/* Citizen & Public Portal Routes */}
        <Route path="/" element={<CitizenLayout />}>
          <Route index element={<HomePage />} />
          <Route path="report" element={<ReportDamagePage />} />
          <Route path="track" element={<TrackComplaintPage />} />
        </Route>

        {/* Administrator Portal Routes */}
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<AdminDashboardPage />} />
          <Route path="analytics" element={<AdminAnalyticsPage />} />
          <Route path="complaints" element={<AdminComplaintsPage />} />
        </Route>

        {/* Fallback Catch-All Route */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
