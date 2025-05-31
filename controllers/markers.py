from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

markers_bp = Blueprint('markers', __name__)

@markers_bp.route('/markers', methods=['GET'])
def get_markers():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM markers")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)

@markers_bp.route('/markers', methods=['POST'])
def add_marker():
    data = request.get_json()
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO markers (title, lat, lng, popupContent, audioUrl, imageUrl, tags, author, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['title'], data['lat'], data['lng'], data['popupContent'],
        data['audioUrl'], data['imageUrl'], data['tags'], data['author'], data['date']
    ))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Marcador guardado correctamente'})
