from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

markers_bp = Blueprint('markers', __name__)

@markers_bp.route('/markers', methods=['GET'])
def get_markers():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM markers")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convertir campo tags (string) a lista
        for marker in result:
            if 'tags' in marker and marker['tags']:
                marker['tags'] = [tag.strip() for tag in marker['tags'].split(',')]
            else:
                marker['tags'] = []

        return jsonify(result)
    except Exception as e:
        print(f"Error en /markers: {e}")
        return jsonify({"error": str(e)}), 500


@markers_bp.route('/markers', methods=['POST'])
def add_marker():
    try:
        data = request.get_json()

        # Validación básica
        required_fields = ['title', 'lat', 'lng', 'popupContent', 'date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido faltante: {field}'}), 400

        # Convierte lista de tags a string si es necesario
        tags = data.get('tags', [])
        if isinstance(tags, list):
            tags = ','.join(tags)
        else:
            tags = tags or ''  # en caso de None

        # Campos opcionales
        audioUrl = data.get('audioUrl') or ''
        imageUrl = data.get('imageUrl') or ''
        author = data.get('author') or ''

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO markers (title, lat, lng, popupContent, audioUrl, imageUrl, tags, author, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['title'], data['lat'], data['lng'], data['popupContent'],
            audioUrl, imageUrl, tags, author, data['date']
        ))
        conn.commit()

        # Recuperar el ID insertado
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Marcador guardado correctamente',
            'id': new_id
        }), 201

    except Exception as e:
        print(f"Error en POST /markers: {e}")
        return jsonify({'error': str(e)}), 500

@markers_bp.route('/markers/<int:id>', methods=['PUT'])
def update_marker(id):
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE markers SET
                title = %s,
                lat = %s,
                lng = %s,
                popupContent = %s,
                audioUrl = %s,
                imageUrl = %s,
                tags = %s,
                author = %s,
                date = %s
            WHERE id = %s
        """, (
            data['title'], data['lat'], data['lng'], data['popupContent'],
            data['audioUrl'], data['imageUrl'],
            ','.join(data['tags']),  # Guardamos la lista como string
            data.get('author', ''),  # Por si falta author en el frontend
            data['date'], id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Marcador actualizado correctamente'})
    except Exception as e:
        print(f"Error al actualizar marcador: {e}")
        return jsonify({'error': str(e)}), 500

@markers_bp.route('/markers/<int:id>', methods=['DELETE'])
def delete_marker(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM markers WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Marcador eliminado correctamente'})
    except Exception as e:
        print(f"Error al eliminar marcador: {e}")
        return jsonify({'error': str(e)}), 500

