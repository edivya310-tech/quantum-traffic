import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { TrafficProvider } from './context/TrafficContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <TrafficProvider>
        <App />
      </TrafficProvider>
    </BrowserRouter>
  </StrictMode>,
)
