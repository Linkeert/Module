SELECT ticket_id
FROM tickets
WHERE text LIKE '%отлично%'
ORDER BY csat DESC;
