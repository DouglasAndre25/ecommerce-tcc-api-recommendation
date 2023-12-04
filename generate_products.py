import random
import pandas as pd
import faker
import ast

# Arquivo de produtos
arquivo_csv = 'flipkart_com-ecommerce_sample.csv'

# Leitura dos dados
fake = faker.Faker()
df = pd.read_csv(arquivo_csv)

# Lista de categorias de produtos
categories = ['female', 'male', 'unissex']
seasons = ['spring', 'summer', 'fall', 'winter']
times = ['day', 'night']

products = []

for index, row in df.iterrows():
    image_urls_str = row['image']
    image_urls = ast.literal_eval(image_urls_str) if isinstance(image_urls_str, str) else []
    first_image_url = image_urls[0] if len(image_urls) > 0 else ""
    
    product = {
        "name": str(row['product_name']).replace("'", "").replace('"', ''),
        "brand": str(row['brand']).replace("'", "").replace('"', ''),
        "category": f"{random.choice(categories)}, {random.choice(seasons)}, {random.choice(times)}",
        "price": row['retail_price'],
        "imgUrl": first_image_url,
        "saleQtd": random.randint(0, 500),
        "description": fake.paragraph(),
    }
    products.append(product)

with open("product_data.txt", "w", encoding="utf-8") as file:
    for product in products:
        line = f"('{product['name']}', '{product['brand']}', '{product['category']}',"
        line += f" '{product['price']}', '{product['imgUrl']}', {product['saleQtd']}, '{product['description']}'),\n"
        file.write(line)

print("Data successfully saved to file 'product_data.txt'")