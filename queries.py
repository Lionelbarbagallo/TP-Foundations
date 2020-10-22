import pandas as pd
import psycopg2
import time
import sqlalchemy

time.sleep(120)

queries_dict = [
        {
            'query':'SELECT ordenes.cliente_id, sum(items_ordenes.precio_item) AS ventas FROM ordenes INNER JOIN items_ordenes ON ordenes.orden_id = items_ordenes.item_id GROUP BY ordenes.cliente_id ORDER BY sum(items_ordenes.precio_item) DESC LIMIT 1000', 
            'archivo':'/usr/src/app/mejores_clientes.csv'
            },
        {
            'query':'SELECT zip_codes.zip_code, zip_codes.ciudad, sum(items_ordenes.precio_item) AS ventas FROM ordenes INNER JOIN items_ordenes ON ordenes.orden_id = items_ordenes.item_id INNER JOIN clientes ON ordenes.cliente_id = clientes.cliente_id INNER JOIN zip_codes ON zip_codes.zip_code = cliente_zip_code  GROUP BY zip_codes.zip_code ORDER BY sum(items_ordenes.precio_item) DESC LIMIT 1000',
            'archivo':'/usr/src/app/ventas_zipcode.csv'  
            },
        {
            'query':'SELECT productos.producto_id, productos.categoria, sum(items_ordenes.precio_item) AS ventas_totales FROM items_ordenes INNER JOIN productos ON items_ordenes.producto_id = productos.producto_id GROUP BY productos.categoria, productos.producto_id ORDER BY sum(items_ordenes.precio_item) DESC LIMIT 1000',
            'archivo':'/usr/src/app/mas_vendidos.csv'
            },
        {
            'query':'WITH ventas_agregadas AS (SELECT productos.categoria, productos.producto_id, sum(items_ordenes.precio_item) OVER (PARTITION BY productos.categoria)  AS ventas_total_categoria, sum(items_ordenes.precio_item) OVER (PARTITION BY categoria, productos.producto_id) AS ventas_total_producto, row_number() OVER (PARTITION BY categoria, productos.producto_id) AS n_row, sum(items_ordenes.precio_item) OVER () AS ventas_totales FROM items_ordenes INNER JOIN  productos ON items_ordenes.producto_id = productos.producto_id) SELECT categoria, producto_id, ventas_total_categoria/ventas_totales AS share_categoria, ventas_total_producto/ventas_total_categoria AS share_prod_cat FROM ventas_agregadas WHERE n_row = 1 ORDER BY share_categoria DESC,  share_prod_cat  DESC LIMIT 1000',
            'archivo':'/usr/src/app/shares.csv'
            },
        {
            'query':"SELECT AVG(EXTRACT(DAYS FROM entrega_timestamp-entrega_estimada_timestamp)) AS dias_a_plazo, date_trunc('day', entrega_timestamp) AS daily FROM ordenes GROUP BY daily ORDER BY daily",
            'archivo':'/usr/src/app/tiempo_entregas.csv'
            }
        ]

if __name__ == "__main__": 

    engine = sqlalchemy.create_engine('postgresql://postgres:postgres@db:5432/postgres')
    
    for q in queries_dict:

        query = q['query']
        archivo = q['archivo']
        
        pd.read_sql(query, con=engine).to_csv(archivo, index=False)
    
    engine.dispose()
