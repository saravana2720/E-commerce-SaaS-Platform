import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import api from '../../services/api';

export default function AdminOrders() {
  const [items, setItems] = useState([]);
  useEffect(() => { api.get('/admin/orders').then((r) => setItems(r.data.items)); }, []);
  return <Layout><h2>Orders</h2>{items.map((o) => <div key={o.id}>#{o.id} {o.status} ₹{(o.total_paise/100).toFixed(2)}</div>)}</Layout>;
}
