import pandas as pd
import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas.io.sql as psql
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
def closest(lst, K):
    lst = np.asarray(lst)
    idx = (np.abs(lst - K)).argmin()
    print(idx.T)
    #return lst[idx]
    return idx.T
def validar(objects):
    try:
        connection = psycopg2.connect(user = "postgres",
                                    password = "admin",
                                    host = "localhost",
                                    port = "5432",
                                    database = "umls")

        #cursor = connection.cursor()
        cursorSelect = connection.cursor()
        cursorSimilarity = connection.cursor()
        cursorCosine = connection.cursor()
        #postgresql_resetValid="update umls.clef_emea_gsc set " +  labeler + " = 0 where " +  labeler + " = 1";
        #postgreSQL_select_gsc = "select testgsc.cui, testgsc.text as alignment, testgsc.text, testgsc.id_document from umls. clef_emea_gsc_test as testgsc where testgsc.labeler = 'pharmaconer'"
        postgreSQL_ngrams="select * from get_ngrams(%s)"
        #postgresql_similarity="SELECT vec.cui, vec.aui, vec.str, vec.embedding FROM umls.view_vectores as vec WHERE vec.cui = %s  ORDER BY vec.embedding <=> %s"
        #postgresql_similarity="SELECT vec.cui, vec.aui, vec.str, vec.embedding FROM umls.view_vectores as vec inner join umls.mrconso as conso on vec.cui = conso.cui and vec.aui = conso.aui WHERE conso.lat = 'SPA' AND vec.cui = %s  ORDER BY vec.embedding <=> %s"
        #postgresql_similarity="select vec.cui, vec.aui, vec.str, vec.embedding FROM umls.view_vectores as vec where  vec.lat = 'SPA'  ORDER BY vec.embedding <=> %s limit 3"
        postgresql_similarity= "select vec.cui, vec.aui, vec.str, vec.embedding FROM umls.mrconso as vec left join (select sty.cui, sty.tui , row_number()  over (partition by sty.cui order by sty.cui, sty.tui) as rn  from umls.mrsty sty ) stype on stype.cui = vec.cui and stype.rn = 1  where  (vec.lat = 'SPA' OR vec.lat = 'ENG') and (stype.tui= 'T109' OR stype.tui= 'T116')  ORDER BY vec.embedding <=> %s"
        #postgresql_similarity= "select vec.cui, vec.aui, vec.str, vec.embedding FROM umls.view_vectores as vec left join (select sty.cui, sty.tui , row_number()  over (partition by sty.cui order by sty.cui, sty.tui) as rn 	from umls.mrsty sty ) stype on stype.cui = vec.cui and stype.rn = 1  where  (vec.lat = 'SPA' OR vec.lat = 'ENG') and (stype.tui= 'T109' OR stype.tui= 'T116')  ORDER BY vec.embedding <=>
        postgresql_cosine="SELECT cosine_distance(%s, %s)"
        #postgresql_select_test = "select id_document, cui, text from umls.clef_emea_gsc_test where cui = %s and id_document = %s and labeler = %s"
        #postgresql_update="update umls.clef_emea_gsc set " +  labeler + " = %s where id_document = %s and cui = %s and (text is not null or text != '') "

        dfRes = pd.DataFrame(columns=['cui','aui', 'alignment','text', 'corrected', 'umls', 'id_document'])
        #cursor.execute(postgreSQL_select_gsc)

        #mobile_records = cursor.fetchall()
        cont = 0
        for row in objects:
            print(cont)
            print("text = ", row[1], )
            cont = cont + 1
            data= (row[1], )
            print('paso 000000')
            cursorSelect.execute(postgreSQL_ngrams,data)
            print('paso 11111')
            #scores={}
            dfScores = pd.DataFrame(columns=['cui', 'aui','score', 'text', 'textOri'])
            records = cursorSelect.fetchall()
            for rowEnt in records:
                sentence_embeddings = model.encode(rowEnt[0])
                sentence_embeddings_string=np.array2string(sentence_embeddings, separator=",", formatter={'float_kind':'{:e}'.format})
                data2 = (sentence_embeddings_string,)
                #data2 = (row[0],sentence_embeddings_string,)
                #print(sentence_embeddings_string)

                #print(postgresql_similarity)
                print('22222')
                cursorSimilarity.execute(postgresql_similarity, data2)
                print('33333')
                recordsSimilarity=cursorSimilarity.fetchall()
                for rowSim in recordsSimilarity:
                    data3 = (rowSim[3],sentence_embeddings_string,)
                    cursorCosine.execute(postgresql_cosine,data3)
                    cosine = cursorCosine.fetchone()[0]
                    new_row = {'cui':str(row[0]), 'aui':str(rowSim[1]),'score':cosine, 'text':rowSim[2], 'textOri':rowEnt[0] }
                    dfScores = pd.concat([dfScores,pd.DataFrame(new_row, index=[0])], ignore_index=True)
                    #print(dfScores)
                    #scores[rowSim[1]]=cosine
                    break
            #dfCandidates.to_csv('candidates.csv', encoding='utf-8', index=False)
            #print(dfCandidates)
            array = dfScores['score'].to_numpy()
            pos = closest(array, 0)
            #print(dfScores.iloc[pos])
            #print(dfScores.iloc[pos]['text'])
            new_rowFin = {'cui':str(row[0]), 'aui':dfScores.iloc[pos]['aui'], 'alignment':str(row[1]),'text':str(row[2]), 'corrected':dfScores.iloc[pos]['textOri'], 'umls':dfScores.iloc[pos]['text'], 'id_document':str(row[3]) }
            dfRes =  pd.concat([dfRes,pd.DataFrame(new_rowFin, index=[0])],ignore_index=True)
            print(dfRes)
            dfRes.to_csv('./static/data/similarity.csv', encoding='utf-8', sep = ',')
            #dfRes = pd.DataFrame(columns=['cui', 'alignment','text', 'corrected', 'umls'])
        #cursor.close()
        cursorSelect.close()
        #cursorUpdate.close();
        connection.commit()
        return dfRes
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                #cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

