-- Daily sales
SELECT DATE(created_at) AS day, SUM(total_paise)/100.0 AS revenue_inr
FROM orders
WHERE status IN ('paid','shipped','delivered')
GROUP BY day
ORDER BY day DESC;

-- Monthly revenue
SELECT DATE_TRUNC('month', created_at) AS month, SUM(total_paise)/100.0 AS revenue_inr
FROM orders
WHERE status IN ('paid','shipped','delivered')
GROUP BY month
ORDER BY month DESC;

-- Top selling products
SELECT p.name, SUM(oi.quantity) AS total_units
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.name
ORDER BY total_units DESC
LIMIT 10;

-- Inventory alerts
SELECT p.name, i.stock_qty, i.reorder_level
FROM inventory i
JOIN products p ON p.id = i.product_id
WHERE i.stock_qty <= i.reorder_level
ORDER BY i.stock_qty ASC;
