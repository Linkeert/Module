SELECT TOP 1000
    o.order_id,
    o.price,
    o.place,
    c.username AS client_username,
    c.name AS client_name,
    c.age AS client_age,
    c.city AS client_city,
    t.csat,
    t.text AS ticket_text,
    t.date AS ticket_date
FROM
    orders o
JOIN
    clients c ON o.order_client_id = c.client_id
LEFT JOIN
    tickets t ON o.order_id = t.ticket_order_id;
