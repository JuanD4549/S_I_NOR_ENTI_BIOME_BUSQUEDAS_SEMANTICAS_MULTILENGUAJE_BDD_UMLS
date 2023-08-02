from sentence_transformers import SentenceTransformer

# Cargar el modelo multilingüe de Sentence-BERT
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# Lista de oraciones a vectorizar
sentences = ["Azithromycin"]

# Vectorizar las oraciones usando el modelo
sentence_embeddings = model.encode(sentences)

# Imprimir los vectores resultantes
for sentence, embedding in zip(sentences, sentence_embeddings):
    print("Oración:", sentence)
    print("Vector de embeddings:", embedding)
    print()
