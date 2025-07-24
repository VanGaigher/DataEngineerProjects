WITH orders AS (
    SELECT
        *
    FROM {{ref('stg_orders')}}
),

aggregated AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        MIN(order_date) AS first_order,
        MAX(order_date) AS last_order,
        DATEDIFF('day', MIN(order_date),MAX(order_date)) AS days_between,
        COUNT_IF(status = 'cancelado') AS total_cancelled
    FROM orders
    GROUP BY customer_id
),

churned_flag AS (
    SELECT
        COLUMNS(*),
        CASE WHEN DATEDIFF('day', last_order, CURRENT_DATE) > 90 THEN 1
            ELSE 0
        END AS is_churned
    FROM aggregated
)

SELECT
    *
FROM churned_flag