import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask
from modules.recommended import get_recommendations

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)

@app.get('/api/recommended')
def recommended():
    recommendations = get_recommendations(connection)
    return recommendations