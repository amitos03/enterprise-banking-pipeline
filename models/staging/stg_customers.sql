with source as (
    select * from {{ source('clean_banking', 'vw_flattened_customer_profiles') }}
),

renamed as (
    select
        account_id,
        customer_type,
        account_status,
        customer_name as full_name,
        customer_email as email_address,
        customer_city as city
    from source
)

select * from renamed