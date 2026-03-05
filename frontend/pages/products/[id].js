import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import Layout from '../../components/Layout';
import api from '../../services/api';

export default function ProductDetail() {
  const { query } = useRouter();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    if (query.id) api.get(`/products/${query.id}`).then((res) => setProduct(res.data));
  }, [query.id]);

  const addToCart = async () => {
    await api.post('/cart/add', { product_id: product.id, quantity: 1 });
    alert('Added to cart');
  };

  if (!product) return <Layout>Loading...</Layout>;
  return (
    <Layout>
      <h2>{product.name}</h2>
      <p>{product.description}</p>
      <p>₹{(product.price_paise / 100).toFixed(2)}</p>
      <button onClick={addToCart}>Add to cart</button>
    </Layout>
  );
}
