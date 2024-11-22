-- explore the number of items in each store with more than a month of days recorded
SELECT vendor, COUNT(*)
FROM 
(
    SELECT 
        p.id AS product_id,
        p.vendor,
        (JULIANDAY(MAX(r.nowtime)) - JULIANDAY(MIN(r.nowtime))) AS time_diff
    FROM 
        product p
    JOIN 
        raw r 
        ON p.id = r.product_id
    GROUP BY 
        p.id, p.vendor
) AS time_diffs
WHERE time_diff > 90
GROUP BY vendor