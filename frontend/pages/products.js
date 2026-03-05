import Link from 'next/link';
import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import api from '../services/api';

export default function Products() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get('/products').then((res) => setItems(res.data.items));
  }, []);

  return (
    <Layout>
      <h2>Products</h2>
      {items.map((p) => (
        <div key={p.id}>
          <Link href={`/products/${p.id}`}>{p.name}</Link> - ₹{(p.price_paise / 100).toFixed(2)}
        </div>
      ))}
    </Layout>
  );
}
