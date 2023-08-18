import random
import faker

# Cria uma instância do gerador de dados fictícios
fake = faker.Faker()

# Lista de categorias de produtos
categories = ['female', 'male', 'unissex']
seasons = ['spring', 'summer', 'fall', 'winter']
times = ['day', 'night']

# Gera 10.000 produtos
num_products = 10000
products = []

for _ in range(num_products):
    product = {
        "name": fake.word().capitalize(),
        "brand": fake.company(),
        "category": f"{random.choice(categories)}, {random.choice(seasons)}, {random.choice(times)}",
        "price": round(random.uniform(10, 200), 2),
        "imgUrl": fake.image_url(),
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