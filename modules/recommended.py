import csv
import pandas as pd
from flask import Response, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def set_products_csv(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, brand, category, price, \"imgUrl\", \"saleQtd\" FROM \"product\" ORDER BY \"saleQtd\" DESC;")
            products = cursor.fetchall()
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

def get_query(category, param, ids):
    querys = {
        'gender': f"SELECT p.* FROM product p JOIN unnest(ARRAY[{ids}]) WITH ORDINALITY t(id, ord) ON p.id = t.id WHERE category LIKE '{param}%' ORDER BY t.ord LIMIT 20;",
        'seasonOrDayTime': f"SELECT p.* FROM product p JOIN unnest(ARRAY[{ids}]) WITH ORDINALITY t(id, ord) ON p.id = t.id WHERE category LIKE '%{param}%' ORDER BY t.ord LIMIT 20;",
        'region': f"""
            WITH avg_saleqtd AS (
                SELECT AVG(p."saleQtd") AS avg_saleqtd
                FROM product p
            )
            SELECT p.* FROM product p JOIN unnest(ARRAY[{ids}]) WITH ORDINALITY t(id, ord) ON p.id = t.id
                    JOIN "productBag" ph ON ph."product_id" = p.id
                    JOIN "bag" b ON b."id" = ph."bag_id"
                    JOIN "user" u ON u."id" = b."user_id"
                    JOIN "address" ad ON ad."user_id" = u."id"
                    JOIN avg_saleqtd avgq ON p."saleQtd" > avgq.avg_saleqtd
                    WHERE b."completedPurchase" = True AND ad."state" = '{param}'
                    ORDER BY t.ord LIMIT 20;""",
        'age': f"""
            WITH avg_saleqtd AS (
                SELECT AVG(p."saleQtd") AS avg_saleqtd
                FROM product p
            )
            SELECT p.* FROM product p JOIN unnest(ARRAY[{ids}]) WITH ORDINALITY t(id, ord) ON p.id = t.id
                    JOIN "productBag" ph ON ph."product_id" = p.id
                    JOIN "bag" b ON b."id" = ph."bag_id"
                    JOIN "user" u ON u."id" = b."user_id"
                    JOIN "address" ad ON ad."user_id" = u."id"
                    JOIN avg_saleqtd avgq ON p."saleQtd" > avgq.avg_saleqtd
                    WHERE b."completedPurchase" = True AND EXTRACT(YEAR FROM u."birthday") > {list(map(int, param.split("-")))[0] if category == 'age' else ''} AND EXTRACT(YEAR FROM u."birthday") < {list(map(int, param.split("-")))[1] if category == 'age' else ''}
                    ORDER BY t.ord LIMIT 20;
        """
    }

    return querys[category]


def get_recommendations(connection, user_id, category, param):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT p.name, p.brand FROM \"productHistory\" ph INNER JOIN product p ON p.id = ph.product_id INNER JOIN \"user\" u ON u.id = ph.user_id WHERE \"user_id\" = {user_id} ORDER BY ph.\"updatedAt\" DESC LIMIT 20;")
            user_history_data = cursor.fetchall()
            if len(user_history_data) <= 0:
                return Response(json.dumps([]), mimetype='application/json')
            # Transformar os dados em listas de dicionários
            user_history = [f"{item[0]} {item[1]}" for item in user_history_data]

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

    # Passo 4: Calcula a similaridade conforme o histórico do usuário
    sim_scores = []
    for index in user_product_indices:
        sim_scores.extend(list(enumerate(cosine_sim[index])))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [score for score in sim_scores if score[0] not in user_product_indices]  # Excluir produtos do histórico

    recommended_indices = [i[0] for i in sim_scores] # Recomendar os produtos mais similares

    # Passo 5: Pega os ids do produto e pega a query do banco de dados conforme os parametros da url
    recommendations = data[['productId']].iloc[recommended_indices]
    recommendations_id = [i[0] for i in recommendations.to_numpy()]
    recomendations_query = get_query(category, param, ', '.join(str(id) for id in recommendations_id))

    # Passo 6: Executa a query no banco de dados
    with connection.cursor() as cursor:
        cursor.execute(recomendations_query)
        recommendations_data = cursor.fetchall()
        recommendations = [{'id': row[0], 'name': row[1], 'brand': row[2], 'category': row[3], 'price': row[4], 'imgUrl': row[5], 'saleQtd': row[6], 'description': row[7] } for row in recommendations_data]

    return Response(json.dumps(recommendations), mimetype='application/json')
