#T047
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import psycopg2

# Establecer la conexión a la base de datos PostgreSQL
try:
    conn = psycopg2.connect(
        host="localhost",
        database="umls",
        user="postgres",
        password="admin",
        )
    print("Conexión exitosa")
    cursor = conn.cursor()
    # Obtener los datos de la columna de la tabla en un DataFrame de pandas
    queryCUI = "SELECT cui FROM umls.mrsty WHERE tui='T047' AND vectstatus= false LIMIT 1"
    cuiAll = pd.read_sql_query(queryCUI, conn)

    print(cuiAll['cui'])
    # Inicializar el modelo Sentence-BERT
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    for cui in cuiAll['cui']:
        print("se vectoriza el cui: " + cui)
        query = "SELECT str FROM umls.mrconso WHERE cui= %(cui)s AND (lat='ENG' OR lat='SPA') AND vectstatus= false"
        df = pd.read_sql_query(query,conn,params={"cui":cui})
        #print(df)
        # Vectorizar la columna de texto
        df['vector'] = df['str'].apply(lambda x: model.encode([x])[0])

        # Crear una columna temporal para almacenar los vectores como texto
        df['embedding'] = df['vector'].apply(lambda x: np.array2string(x, separator=',', formatter={'float_kind': '{:f}'.format}))

        # Actualizar la tabla en la base de datos con los vectores
        for index, row in df.iterrows():
            vector_text = row['embedding']
            reference_value = row['str']
            update_query = "UPDATE umls.mrconso SET embedding = %s, vectstatus= TRUE WHERE str= %s"
            cursor.execute(update_query, (vector_text, reference_value))
            print("se actualizo el cui: " + reference_value)
        update_query = "UPDATE umls.mrsty SET vectstatus= TRUE WHERE tui ='T047' AND cui= %s"
        cursor.execute(update_query, (cui))
        print("se actualizo la tabla mrsty: " + cui)
except Exception as ex:
    print(ex)
finally:
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


