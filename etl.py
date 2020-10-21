import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import time

dict_dataset =[
        {
            'archivo':'olist_geolocation_dataset.csv',
            'cols_index':[3,4],
            'nombres_cols':['ciudad','estado'],
            'pk':'ciudad',
            'tabla':'ciudades'
                },
        {
            'archivo':'olist_geolocation_dataset.csv',
            'cols_index':[0,1,2,3],
            'nombres_cols':['zip_code','lat', 'long','ciudad'],
            'pk':'zip_code',
            'tabla':'zip_codes'
                },
        {
            'archivo':'olist_customers_dataset.csv',
            'cols_index':[0,1,2],
            'nombres_cols':['cliente_id','cliente_id_unico', 'cliente_zip_code'],
            'pk':'cliente_id',
            'tabla':'clientes'
                },
        {
            'archivo':'olist_sellers_dataset.csv',
            'cols_index':[0,1],
            'nombres_cols':['vendedor_id','vendedor_zip_code'],
            'pk':'vendedor_id',
            'tabla':'vendedores'
                },
        {
            'archivo':'product_category_name_translation.csv',
            'cols_index':[0,1],
            'nombres_cols':['categoria_port','categoria_ingles'],
            'pk':'categoria_port',
            'tabla':'traduccion_nombre'
                },
        {
            'archivo':'olist_products_dataset.csv',
            'cols_index':[0,1,2,3,4,5,6,7,8],
            'nombres_cols':['producto_id','categoria', 'nombre_largo','descripcion_prod_largo','cantidad_fotos',
            'prod_peso_grs','prod_largo_cm','prod_alto_cm','prod_ancho_cm'],
            'pk':'producto_id',
            'tabla':'productos'
                },
        {
            'archivo':'olist_orders_dataset.csv',
            'cols_index':[0,1,2,3,4,5,6,7],
            'nombres_cols':['orden_id','cliente_id', 'status','compra_timestamp','aprobado_timestamp',
            'entrega_transporte_timestamp', 'entrega_timestamp','entrega_estimada_timestamp'],
            'pk':'orden_id',
            'tabla':'ordenes'
                },
        {
            'archivo':'olist_order_items_dataset.csv',
            'cols_index':[0,1,2,3,4,5,6],
            'nombres_cols':['item_id','item_numero_orden', 'producto_id','vendedor_id','fecha_entrega_maxima', 
            'precio_item','precio_flete_item'], 
            'pk':'item_id', 
            'tabla':'items_ordenes'
                },
        {
            'archivo':'olist_order_payments_dataset.csv',
            'cols_index':[0,1,2,3,4],
            'nombres_cols':['pago_id','numero_subpago', 'medio_pago','numero_cuotas','importe_pago'],
            'pk':'pago_id',
            'tabla':'pagos'
            },
        {
            'archivo':'olist_order_reviews_dataset.csv',
            'cols_index':[0,1,2,3,4,5,6],
            'nombres_cols':['review_id','orden_id','review_score','titulo','mensaje','fecha_creacion','fecha_respuesta'],
            'pk':'review_id',
            'tabla':'reviews'
                }
    ]

def etl_dataset(parametros,con):
    """
    Esta función se encarga de pasar un archivo .csv a una tabla de una base de datos SQL.
    
    Args:

        -parametros (diccionario): es un objeto diccionario que contiene las instrucciones para leer el .csv y subirlo a la base de datos.

            Los pares de claves-valores que deben proveerse en este diccionario son los siguientes:
                archivo (str): indica el archivo .csv a leer
                cols_index (lista): es una lista de enteros que indica los índices de las columnas a leer del archivo .csv
                nombres_cols (lista): es una lista de strings que contiene los nombres que se le asignarán a las columnas (y deben coincidir con los de la tabla en la db)
                pk (str): es el nombre de la columna que se utilizará como Primary Key.
                tabla (str): es el nombre de la tabla en la base de datos a la que se subirá el .csv procesado.

        -con (engine): este argumento recibe una instancia de un objeto tipo Engine para conectarse a la base de Datos. Para más detalle sobre este objeto, referimos a 
        la documentación de SQLAlchemy https://docs.sqlalchemy.org/en/13/core/engines.html

    Returns:
        -None
    """
    archivo=parametros['archivo']
    cols_index=parametros['cols_index']
    col_names=parametros['nombres_cols']
    pk=parametros['pk']
    tabla=parametros['tabla']
    
    df = pd.read_csv(archivo, usecols=cols_index, header=0, names=col_names)
    df.drop_duplicates(subset=[pk]).to_sql(tabla, con=con, index=False, if_exists='append')

if __name__ == "__main__":

    engine = create_engine('postgresql://postgres:postgres@db:5432/postgres')

    for i in dict_dataset:
        try:
            etl_dataset(i,engine)
        except:
            pass
    engine.dispose()
