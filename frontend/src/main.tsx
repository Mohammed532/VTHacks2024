import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from "react-router-dom"

import Landing from './Landing.tsx'
import Home from './pages/Home/'

import './index.css'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Landing />,
  },
  {
    path: "home",
    element: <Home />
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
