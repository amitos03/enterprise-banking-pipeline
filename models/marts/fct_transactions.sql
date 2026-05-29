WITH transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
)

SELECT
    t.*,
    c.customer_id,
    c.risk_score,
    c.full_name,
    c.city
FROM transactions t
LEFT JOIN customers c 
    ON t.account_id = c.account_id