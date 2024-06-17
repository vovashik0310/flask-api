from flask import Flask, request, Response, jsonify, g
import pickle
# from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import sqlite3

# SWAGGER_URL="/swagger"
# API_URL="/static/swagger.json"

# swagger_ui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         "app_name" : 'Model API'
#     }
# )

app = Flask(__name__)
DATABASE = 'doctors.db'

CORS(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None :
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if  db is not None:
        db.close()
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def home():
    return jsonify({
        "Message" : "app up and running successfully"
    })

@app.route('/api/get-data', methods=['POST'])
def get_data():
    try:
        db = get_db()
        cursor = db.cursor()
        category = request.args['category']
        categories = category.split(',')
        if len(categories) == 0 : categories.append("None")
        print(categories)
        placeholders = ','.join('?' * len(categories))
        print(placeholders)
        sql = f"SELECT * FROM doctor_table WHERE category IN ({placeholders}) AND address like '%NJ%' order by distance ;"
        print(sql)
        cursor.execute(sql, categories)
        data = cursor.fetchall()
        return jsonify([dict(row) for row in data])
    except Exception as e:
        # Log the exception or handle it as per your application's needs
        print(f"Error fetching data: {e}")
        return jsonify({'error': 'Failed to fetch data'}), 500


# @app.route("/get-possible", methods = ["post"])
# def get_possible():
#     required_fields = {
#         "artist_id",
#         "genre_id",
#         "instrumentation_id",  # Assuming this is the intended field
#         "venue_id",
#         "artist_state",
#         "artist_performance",
#         "artist_vocals",
#         "venue_state",
#         "venue_type",
#         "venue_capacity"
#     }
#     missing_fields = []
#     print(request.json)
#     for field in required_fields:
#         if field not in request.json:
#             missing_fields.append(field)
#     if missing_fields :
#         message = f"Missing required fields: {', '.join(missing_fields)}"
#         return Response(message, status=400)
    
#     artist_id = request.json['artist_id']
#     print(artist_id)
#     genre_id = request.json['genre_id']
#     instrumentation_id = request.json['instrumentation_id']
#     venue_id = request.json['venue_id']
#     artist_state = request.json['artist_state']
#     artist_performance = request.json['artist_performance']
#     artist_vocals = request.json['artist_vocals']
#     venue_state = request.json['venue_state']
#     venue_type = request.json['venue_type']
#     venue_capacity = request.json['venue_capacity']

#     possible_value = calculate_possible(
#         artist_id, 
#         genre_id, 
#         instrumentation_id,
#         venue_id,
#         artist_state,
#         artist_performance,
#         artist_vocals,
#         venue_state,
#         venue_type,
#         venue_capacity
#     )

#     return possible_value

if __name__ == "__main__":
    app.run(debug=True, user_reloader=True)

