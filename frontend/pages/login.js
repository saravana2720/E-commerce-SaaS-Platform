import { useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import useAuth from '../hooks/useAuth';
import api from '../services/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const auth = useAuth();
  const router = useRouter();

  const submit = async () => {
    const res = await api.post('/auth/login', { email, password });
    auth.login(res.data);
    router.push('/products');
  };

  return <Layout><h2>Login</h2><input placeholder="email" onChange={(e) => setEmail(e.target.value)} /><input type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} /><button onClick={submit}>Login</button></Layout>;
}
