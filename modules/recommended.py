import pandas as pd
from flask import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_recommendations(connection):
    data = pd.read_csv('products.csv')
    user_history = ['Saia midi plissada', 'Camiseta polo Nike', 'Suéter de cashmere', 'Legging Adidas', 'Conjunto de moletom Puma', 'Bermuda cargo Timberland', 'Gravata borboleta preta', 'Chapéu Fedora de feltro', 'Chinelo slide', 'Presilha de cabelo com pérola', 'Relógio de pulso analógico', 'Biquíni de crochê', 'Camiseta estampada tie-dye', 'Camisa xadrez flanela', 'Vestido tubinho preto']

    # Passo 2: Pré-processamento dos Dados
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(data['name'] + ' ' + data['brand'])  # Concatenação de name e brand

    # Passo 3: Cálculo da Similaridade
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    user_product_indices = [data[data['name'] == product]['id'].values[0] for product in user_history]

    sim_scores = []
    for index in user_product_indices:
        sim_scores.extend(list(enumerate(cosine_sim[index])))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] not in user_product_indices]  # Excluir produtos do histórico

    recommended_indices = [i[0] for i in sim_scores][:10]  # Recomendar os 10 produtos mais similares
    recommendations = data[['name', 'brand', 'category', 'price', 'imgUrl', 'saleQtd']].iloc[recommended_indices]

    return Response(recommendations.to_json(orient="records"), mimetype='application/json')
