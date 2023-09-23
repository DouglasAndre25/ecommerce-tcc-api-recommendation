import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from modules.recommended import get_recommendations

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)

@app.get('/api/recommended/<int:user_id>')
def recommended(user_id):
    category = request.args.get('category')
    param = request.args.get('param')
    recommendations = get_recommendations(connection, user_id, category, param)
    return recommendations