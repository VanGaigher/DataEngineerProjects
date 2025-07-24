{{ config(materialized='view') }}

WITH source AS (
    SELECT 
        * 
    FROM {{ ref('products') }}
),

renamed AS (
    SELECT
        product_id,
        REGEXP_REPLACE(LOWER(product_name), '\b(\w)', '\U\1') AS product_name,
        category,
        CAST(custo AS NUMERIC) AS cost,
        CAST(price AS NUMERIC) AS price,
        ROUND(price - cost, 2) AS margin
    FROM source
)

SELECT 
    * 
FROM renamed
