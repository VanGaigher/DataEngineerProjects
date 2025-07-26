WITH base AS (
    SELECT
        *
    FROM {{ref('stg_customers')}}
),

churn_data AS (
    SELECT
        *
    FROM {{ref('int_churn_prediction_data')}}
)

SELECT
    b.customer_id,
    b.name,
    b.email,
    b.signup_date,
    c.total_orders,
    c.total_cancelled,
    c.days_between,
    c.is_churned
FROM base b
LEFT JOIN churn_data c ON b.customer_id = c.customer_id