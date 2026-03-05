import { useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import api from '../services/api';

export default function Signup() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const submit = async () => {
    await api.post('/auth/signup', { name, email, password });
    router.push('/login');
  };

  return <Layout><h2>Signup</h2><input placeholder="name" onChange={(e) => setName(e.target.value)} /><input placeholder="email" onChange={(e) => setEmail(e.target.value)} /><input type="password" placeholder="password" onChange={(e) => setPassword(e.target.value)} /><button onClick={submit}>Create account</button></Layout>;
}
