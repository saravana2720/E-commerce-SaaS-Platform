import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import api from '../../services/api';

export default function Analytics() {
  const [data, setData] = useState(null);
  useEffect(() => { api.get('/admin/analytics/revenue').then((r) => setData(r.data)); }, []);
  if (!data) return <Layout>Loading...</Layout>;
  return <Layout><h2>Revenue Analytics</h2><p>Total revenue: ₹{(data.total_revenue_paise/100).toFixed(2)}</p></Layout>;
}
