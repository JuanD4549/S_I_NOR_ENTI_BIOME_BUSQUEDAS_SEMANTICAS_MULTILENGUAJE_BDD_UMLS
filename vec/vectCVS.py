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
    cuiAll = pd.read_csv('allClef.csv')
    #print(cuiAll['cui'])
    # Inicializar el modelo Sentence-BERT
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    # Vectorizar la columna de texto
    print("se esta vectorizando")
    cuiAll['vector'] = cuiAll['str'].apply(lambda x: model.encode([x])[0])
    # Crear una columna temporal para almacenar los vectores como texto
    cuiAll['embedding'] = cuiAll['vector'].apply(lambda x: np.array2string(x, separator=',', formatter={'float_kind': '{:f}'.format}))

    for index, row in cuiAll.iterrows():
        print("se actualizara el cui: " + row['cui'] + " / " + row['str'])
        # Actualizar la tabla en la base de datos con los vectores
        update_query = "UPDATE umls.mrconso SET embedding = %s WHERE str= %s AND aui=%s"
        cursor.execute(update_query, (row['embedding'], row['str'],row['aui']))
        print("se actualizo el cui: " + row['cui'] + " / " + row['str'])
except Exception as ex:
    print(ex)
finally:
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


