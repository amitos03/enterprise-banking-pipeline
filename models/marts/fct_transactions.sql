with transactions as (
    select * from {{ ref('stg_transactions') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

final as (
    select
        t.transaction_id,
        t.account_id,
        c.full_name as customer_name,
        c.customer_type,
        c.city as customer_city,
        t.amount as transaction_amount,
        t.txn_date as transaction_date,
        t.transaction_status
    from transactions t
    left join customers c 
        on t.account_id = c.account_id
)

select * from final