WITH raw_crm AS (
    SELECT * FROM RAW_BANKING_DATA.INBOUND_FILES.RAW_SALESFORCE_CRM
)

SELECT
    crm_payload:sf_contact_id::VARCHAR AS customer_id,
    crm_payload:linked_account_id::VARCHAR AS account_id,
    crm_payload:risk_score::NUMBER AS risk_score,
    crm_payload:personal_details.full_name::VARCHAR AS full_name,
    crm_payload:personal_details.email::VARCHAR AS email,
    crm_payload:personal_details.phone::VARCHAR AS phone,
    crm_payload:personal_details.address.city::VARCHAR AS city
FROM raw_crm