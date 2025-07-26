{{ config(materialized='view') }}

WITH source AS (
    SELECT 
        * 
    FROM {{ ref('products') }}
),

renamed AS (
    SELECT
        product_id,
        INITCAP(LOWER(product_name)) AS product_name, -- Alteração aqui
        category,
        CAST(custo AS NUMERIC) AS cost,
        CAST(price AS NUMERIC) AS price,
        ROUND(CAST(price - custo AS NUMERIC), 2) AS margin
    FROM source
)

SELECT 
    * 
FROM renamed
