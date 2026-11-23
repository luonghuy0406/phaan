import { StrictMode, Suspense, lazy } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import CasePage from './pages/CasePage';
import { initAuth } from './lib/auth';
import { RequireAuth } from './components/auth';
import { SITE } from './lib/config';
import './styles/tokens.css';
import './styles/site.css';

// The board (gestures, ink, persistence) only loads when a case is opened.
const PlayPage = lazy(() => import('./pages/PlayPage'));
const RoomPlayPage = lazy(() => import('./pages/RoomPlayPage'));
const LobbyPage = lazy(() => import('./pages/LobbyPage'));
const JoinPage = lazy(() => import('./pages/JoinPage'));
const LoginPage = lazy(() => import('./pages/LoginPage'));

initAuth();
const solo = <PlayPage />;

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Suspense fallback={<div className="board-loading">Đang tải…</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/ho-so/:id" element={<CasePage />} />
          <Route path="/choi/:id" element={SITE.requireLoginForSolo ? <RequireAuth>{solo}</RequireAuth> : solo} />
          <Route path="/dang-nhap" element={<LoginPage />} />
          <Route path="/tham-gia" element={<RequireAuth><JoinPage /></RequireAuth>} />
          <Route path="/phong/:roomId" element={<RequireAuth><LobbyPage /></RequireAuth>} />
          <Route path="/phong/:roomId/choi" element={<RequireAuth><RoomPlayPage /></RequireAuth>} />
          <Route path="*" element={<Home />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  </StrictMode>,
);
