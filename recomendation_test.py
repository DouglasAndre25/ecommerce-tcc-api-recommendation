# 1. Importe as bibliotecas necessárias
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

# 2. Crie uma lista de recomendações e uma lista base de produtos
lista_base = [
    "Mast & Harbour Solid Single Breasted Casual Womens Blazer - Mast & Harbour",
    "Katalogue Women, Girls Heels - Katalogue",
    "ab posters minions cartoons Art PVC Pencil Box - ab posters",
    "Anasazi Womens Solid Casual Shirt - Regular",
    "Reebok Training & Gym Shoes - notRegistered",
    "AdroitZ Premium Phone Socket Holder For Nokia N9 - AdroitZ",
    "Disney Minii Mouse_spiderman Redamption Combo Set - notRegistered",
    "Amante Womens Boy Short Panty - Amante",
    "Strak Full Sleeve Striped Mens Sweatshirt - notRegistered",
    "Tootpado Art Plastic Punches & Punching Machines - notRegistered",
    "Times 374TMS374 Party-Wedding Analog Watch  - For Women - notRegistered",
    "Tradition India Floral Single Quilts & Comforters Multicolor - Tradition India",
    "Famaya Girls Leggings - Famaya",
    "Dremel 2615.023.132 Plastic Friction Work Bench Cabinet - Dremel",
    "YNA Aviator Sunglasses - notRegistered",
    "Get Glamr Designer Suede Brogues Corporate Casuals - notRegistered",
    "DailyObjects Back Cover for Apple iPad 2, 3, 4 - DailyObjects",
    "Aaradhi Divya Mantra Yellow Aventurine Guru Bead Meditation Mala Stone Necklace - Aaradhi",
    "Timewel 1100-N1944_B Analog Watch  - For Women - notRegistered",
    "palito PLO 166 Analog Watch  - For Girls, Women - palito"
]
lista_recomendacoes = [
    "Wrangler Regular Fit Mens Jeans - Regular",
    "Glus Wedding Lingerie Set - notRegistered",
    "Colat COLAT_MW20 Sheen Analog Watch  - For Men, Women, Boys, Girls - notRegistered",
    "Swag 670038 Analog Watch  - For Boys - notRegistered",
    "Rochees RW50 Analog Watch  - For Boys - notRegistered",
    "Felix Y 39 Analog Watch  - For Boys, Men - notRegistered",
    "Titan 1639SL03 Analog Watch  - For Boys, Men - notRegistered",
    "Q&Q VQ13-008 Analog Watch  - For Girls, Boys - notRegistered",
    "Franck Bella FB74C Analog Watch  - For Boys, Men - notRegistered",
    "Franck Bella FB0128B Analog Watch  - For Men, Boys - notRegistered",
    "Maserati Time R8851116001 Analog Watch  - For Boys - notRegistered",
    "Cobra Paris CO6394A1 Analog Watch  - For Men, Boys - notRegistered",
    "Camerii WM64 Elegance Analog Watch  - For Men, Boys - notRegistered",
    "Aries Gold G 729 S-BK Analog Watch  - For Men, Boys - notRegistered",
    "Skmei AD1031-Black Formal Analog-Digital Watch  - For Men, Boys - notRegistered",
    "Escort E-1700-906_Blk Analog Watch  - For Men, Boys - notRegistered",
    "Kms Ironman_Look_Led_Black11 Digital Watch  - For Men, Women, Girls, Boys - notRegistered",
    "Silver Streak Mens Printed Casual Denim Shirt - Slim",
    "Costa Swiss CS-2001 Analog Watch  - For Boys, Men - notRegistered",
    "Rorlig RR-030 Essentials Analog Watch  - For Men, Boys - notRegistered"
]

# 3. Pré-processe os textos dos produtos usando a técnica TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_base = tfidf_vectorizer.fit_transform(lista_base)
tfidf_matrix_recomendacoes = tfidf_vectorizer.transform(lista_recomendacoes)

# 4. Calcule a similaridade entre os produtos da lista de recomendações e da lista base
cosine_similarities = linear_kernel(tfidf_matrix_recomendacoes, tfidf_matrix_base)

# 6. Encontre o maior valor de similaridade do cosseno para cada produto na lista de recomendações
maiores_similaridades = cosine_similarities.max(axis=1)

print("As maiores similaridades do cosseno para cada produto na lista de recomendações são:")
for i, produto in enumerate(lista_recomendacoes):
    print(f"{produto}: {maiores_similaridades[i]}")

print('-----------------------------------------------------------')
print('A média de valores do coseno é: ', np.mean(maiores_similaridades))