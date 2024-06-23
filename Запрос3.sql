SELECT order_client_id AS frequent_customer,
       MAX(price) AS max_sum
FROM orders
WHERE place IN ('Теремок', 'Вкусно и точка')
  AND price BETWEEN 2000 AND 10000
GROUP BY order_client_id
HAVING COUNT(order_id) > 5;
