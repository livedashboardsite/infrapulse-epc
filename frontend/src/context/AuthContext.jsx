import { createContext, useState, useContext, useEffect } from 'react';
import { auth, signInWithEmailAndPassword, createUserWithEmailAndPassword, onAuthStateChanged, signOut } from '../config/firebase';
import { mockCompanies } from '../data/mock_initial';

const AuthContext = createContext();
const AUTH_MODE = import.meta.env.VITE_AUTH_MODE || 'demo';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(AUTH_MODE === 'firebase');

  useEffect(() => {
    if (AUTH_MODE !== 'firebase') {
      setLoading(false);
      return;
    }
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      if (firebaseUser) {
        setUser(firebaseUser);
      }
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  const loginWithEmail = async (email, password) => {
    if (AUTH_MODE !== 'firebase') return;
    await signInWithEmailAndPassword(auth, email, password);
  };

  const registerWithEmail = async (email, password) => {
    if (AUTH_MODE !== 'firebase') return;
    await createUserWithEmailAndPassword(auth, email, password);
  };

  const loginDemo = (companyId) => {
    const selectedCompany = mockCompanies.find(c => c.id === companyId);
    setUser({ email: `demo@${companyId}.com`, uid: companyId });
    setCompany(selectedCompany);
  };

  const logout = async () => {
    if (AUTH_MODE === 'firebase') {
      try {
        await signOut(auth);
      } catch (error) {
        // fall through
      }
    }
    setUser(null);
    setCompany(null);
  };

  return (
    <AuthContext.Provider value={{ user, company, loading, loginDemo, loginWithEmail, registerWithEmail, logout, authMode: AUTH_MODE }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
