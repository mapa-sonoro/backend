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

        for marker in result:
            if 'tags' in marker and marker['tags']:
                marker['tags'] = marker['tags'].split(',')
            else:
                marker['tags'] = []


        return jsonify(result)
    except Exception as e:
        print(f"Error en /markers: {e}")
        return jsonify({"error": str(e)}), 500


@markers_bp.route('/markers', methods=['POST'])
def add_marker():
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO markers (title, lat, lng, popupContent, audioUrl, imageUrl, tags, author, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['title'], data['lat'], data['lng'], data['popupContent'],
            data['audioUrl'], data['imageUrl'],
            ','.join(data['tags']),
            data.get('author', ''),  
            data['date']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Marcador guardado correctamente'})
    except Exception as e:
        print(f"Error al agregar marcador: {e}")
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
            ','.join(data['tags']),
            data.get('author', ''),
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

@markers_bp.route('/markers/<int:id>', methods=['GET'])
def get_marker(id):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM markers WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            # Convertir la columna 'tags' a lista
            if 'tags' in result and result['tags']:
                result['tags'] = result['tags'].split(',')
            else:
                result['tags'] = []

            return jsonify(result)
        else:
            return jsonify({'error': 'Marcador no encontrado'}), 404
    except Exception as e:
        print(f"Error al obtener marcador {id}: {e}")
        return jsonify({'error': str(e)}), 500

