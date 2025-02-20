{{ config(materialized='table') }}

with veiculos_dbt_data as (
    select 
        codigo,
        latitude,
        longitude,
        velocidade

    from veiculos
    
)

select * from veiculos_dbt_data