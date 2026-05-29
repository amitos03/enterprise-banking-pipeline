with source as (
    select * from {{ source('raw_banking', 'raw_transactions') }}
),

renamed as (
    select
        transaction_id,
        account_id,
        transaction_amount as amount,
        transaction_date as txn_date,
        status as transaction_status
    from source
)

select * from renamed