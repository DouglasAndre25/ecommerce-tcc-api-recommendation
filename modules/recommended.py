import csv
import pandas as pd
from flask import Response
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def get_query(category, param):
    querys = {
        'gender': f"SELECT id, name, brand, category, price, \"imgUrl\", \"saleQtd\" FROM \"product\" WHERE \"category\" LIKE '{param}%' ORDER BY \"saleQtd\" DESC;",
        'seasonOrDayTime': f"SELECT id, name, brand, category, price, \"imgUrl\", \"saleQtd\" FROM \"product\" WHERE \"category\" LIKE '%{param}%' ORDER BY \"saleQtd\" DESC;",
    }

    return querys[category]

def get_recommendations(connection, user_id, category, param):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT p.name, p.brand FROM \"productHistory\" ph INNER JOIN product p ON p.id = ph.product_id INNER JOIN \"user\" u ON u.id = ph.user_id WHERE \"user_id\" = {user_id};")
            user_history_data = cursor.fetchall()
            cursor.execute(get_query(category, param))
            products = cursor.fetchall()
            # Transformar os dados em listas de dicionários
            user_history = [f"{item[0]} {item[1]}" for item in user_history_data]
            products_data = [{
                "productId": product[0],
                "name": f"{product[1]}",
                "brand": f"{product[2]}",
                "category": f"{product[3]}",
                "price": product[4],
                "imgUrl": f"{product[5]}",
                "saleQtd":  product[6],
            } for product in products]

            with open('products.csv', 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                
                # Escrevendo o cabeçalho (nomes das colunas)
                csv_writer.writerow(["id", "name", "brand", "category", "price", "imgUrl", "saleQtd", "productId"])
                
                # Escrevendo os dados
                for row, product in enumerate(products_data):
                    # Dividindo a string em colunas separadas
                    csv_writer.writerow([row, product['name'], product['brand'], product['category'], product['price'], product['imgUrl'], product['saleQtd'], product['productId']])

    data = pd.read_csv('products.csv')

    # Passo 2: Pré-processamento dos Dados
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    transform = data['name'] + ' ' + data['brand']
    tfidf_matrix = tfidf_vectorizer.fit_transform(transform.values.astype('U'))  # Concatenação de name e brand

    # Passo 3: Cálculo da Similaridade
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    user_product_indices = []
    for product in user_history:
        matching_rows = data[data['name'] + ' ' + data['brand'] == product]
        if not matching_rows.empty:
            user_product_indices.append(matching_rows['id'].values[0])

    sim_scores = []
    for index in user_product_indices:
        sim_scores.extend(list(enumerate(cosine_sim[index])))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] not in user_product_indices]  # Excluir produtos do histórico

    recommended_indices = [i[0] for i in sim_scores][:10]  # Recomendar os 10 produtos mais similares
    recommendations = data[['name', 'brand', 'category', 'price', 'imgUrl', 'saleQtd']].iloc[recommended_indices]

    return Response(recommendations.to_json(orient="records"), mimetype='application/json')
