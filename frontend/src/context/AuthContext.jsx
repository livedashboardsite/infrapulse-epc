import { createContext, useState, useContext, useEffect } from 'react';
import { auth, signInWithEmailAndPassword, createUserWithEmailAndPassword, onAuthStateChanged, signOut } from '../config/firebase';
import { mockCompanies } from '../data/mock_initial';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [company, setCompany] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      setUser(firebaseUser);
      setLoading(false);
    });
    return unsubscribe;
  }, []);

  const loginDemo = (companyId) => {
    const selectedCompany = mockCompanies.find(c => c.id === companyId);
    setUser({ email: `demo@${companyId}.com`, uid: companyId });
    setCompany(selectedCompany);
  };

  const logout = async () => {
    try {
      await signOut(auth);
      setUser(null);
      setCompany(null);
    } catch (error) {
      setUser(null);
      setCompany(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, company, loading, loginDemo, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
