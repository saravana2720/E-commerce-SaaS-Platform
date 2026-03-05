import { useState } from 'react';
import Layout from '../../components/Layout';
import api from '../../services/api';

export default function AdminProducts() {
  const [payload, setPayload] = useState({ name: '', slug: '', description: '', price_paise: 0, stock_qty: 0 });
  const createProduct = async () => {
    await api.post('/admin/product', payload);
    alert('Created');
  };
  return <Layout><h2>Add / Update Product</h2><textarea placeholder="json payload" onChange={(e) => setPayload(JSON.parse(e.target.value || '{}'))} /><button onClick={createProduct}>Save Product</button></Layout>;
}
