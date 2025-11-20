import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import GalaxyClassification from './pages/GalaxyClassification'
import ConstellationRecognition from './pages/ConstellationRecognition'
import CelestialPositioning from './pages/CelestialPositioning'
import SpaceEngine from './pages/SpaceEngine'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'

function AppRoutes() {
  const { isAuthenticated } = useAuth()

  return (
    <Routes>
      <Route path="/login" element={
        isAuthenticated ? <Navigate to="/" /> : <Login />
      } />
      <Route path="/register" element={
        isAuthenticated ? <Navigate to="/" /> : <Register />
      } />
      <Route path="/" element={
        <ProtectedRoute>
          <Home />
        </ProtectedRoute>
      } />
      <Route path="/galaxy" element={
        <ProtectedRoute>
          <GalaxyClassification />
        </ProtectedRoute>
      } />
      <Route path="/constellation" element={
        <ProtectedRoute>
          <ConstellationRecognition />
        </ProtectedRoute>
      } />
      <Route path="/positioning" element={
        <ProtectedRoute>
          <CelestialPositioning />
        </ProtectedRoute>
      } />
      <Route path="/space-engine" element={
        <ProtectedRoute>
          <SpaceEngine />
        </ProtectedRoute>
      } />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App

