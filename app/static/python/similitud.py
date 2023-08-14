import pandas as pd
import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
def closest(lst, K):
    lst = np.asarray(lst)
    idx = (np.abs(lst - K)).argmin()
    print(idx.T)
    return idx.T
def validar(objects):
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "admin",
                                    host = "localhost",
                                    port = "5432",
                                    database = "umls")

        cursorSelect = connection.cursor()
        cursorSimilarity = connection.cursor()
        cursorCosine = connection.cursor()
        postgreSQL_ngrams="select * from get_ngrams(%s)"
        postgresql_similarity= "select vec.cui, vec.aui, vec.str, vec.embedding FROM umls.mrconso as vec left join (select sty.cui, sty.tui , row_number()  over (partition by sty.cui order by sty.cui, sty.tui) as rn  from umls.mrsty sty ) stype on stype.cui = vec.cui and stype.rn = 1  where  (vec.lat = 'SPA' OR vec.lat = 'ENG') and (stype.tui= 'T109' OR stype.tui= 'T116')  ORDER BY vec.embedding <=> %s"
        postgresql_cosine="SELECT cosine_distance(%s, %s)"

        dfRes = pd.DataFrame(columns=['cui','aui', 'alignment','text', 'corrected', 'umls', 'id_document'])
        cont = 0
        for row in objects:
            print("text = ", row[1],)
            cont = cont + 1
            data= (row[1],)
            print('paso get_ngrams')
            cursorSelect.execute(postgreSQL_ngrams,data)
            print('paso finish')
            dfScores = pd.DataFrame(columns=['cui', 'aui','score', 'text', 'textOri'])
            records = cursorSelect.fetchall()
            print('Records')
            print(records)
            for rowEnt in records:
                print("vectorizar = ", rowEnt[0])
                sentence_embeddings = model.encode(rowEnt[0])
                sentence_embeddings_string=np.array2string(sentence_embeddings, separator=",", formatter={'float_kind':'{:e}'.format})
                data2 = (sentence_embeddings_string,)
                print('consulta de similitud')
                cursorSimilarity.execute(postgresql_similarity, data2)
                print('fin consulta de similitud')
                recordsSimilarity=cursorSimilarity.fetchall()
                print('Resultado busqueda')
                print(recordsSimilarity)
                for rowSim in recordsSimilarity:
                    print('vector a comparar')
                    print(rowSim[3])
                    data3 = (rowSim[3],sentence_embeddings_string,)
                    print('Calculo del coseno')
                    cursorCosine.execute(postgresql_cosine,data3)
                    print('Fin del calculo del coseno')
                    cosine = cursorCosine.fetchone()[0]
                    print('valor del coseno: ' + cosine)
                    new_row = {'cui':str(row[0]), 'aui':str(rowSim[1]),'score':cosine, 'text':rowSim[2], 'textOri':rowEnt[0] }
                    dfScores = pd.concat([dfScores,pd.DataFrame(new_row, index=[0])], ignore_index=True)
                    break
            array = dfScores['score'].to_numpy()
            pos = closest(array, 0)
            new_rowFin = {'cui':str(row[0]), 'aui':dfScores.iloc[pos]['aui'], 'alignment':str(row[1]),'text':str(row[2]), 'corrected':dfScores.iloc[pos]['textOri'], 'umls':dfScores.iloc[pos]['text'], 'id_document':str(row[3]) }
            dfRes =  pd.concat([dfRes,pd.DataFrame(new_rowFin, index=[0])],ignore_index=True)
            print(dfRes)
            dfRes.to_csv('./static/data/similarity.csv', encoding='utf-8', sep = ',')
        cursorSelect.close()
        connection.commit()
        return dfRes
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        if(connection):
            connection.close()
            print("PostgreSQL connection is closed")

