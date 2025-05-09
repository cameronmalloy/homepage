from flask import Flask, render_template
from dotenv import load_dotenv
from routes.search import search_bp 
from routes.graph import graph_bp

# def create_app():
app = Flask(__name__)

# Register all blueprints
app.register_blueprint(search_bp)
app.register_blueprint(graph_bp)

# load environment variables
load_dotenv()

# Future: You can load config files, logging, or extensions here
# app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    # app = create_app()
    app.run(debug=True)

# def create_app():
#     app = Flask(__name__)
    
#     # Import and register blueprints
#     from routes.graph import graph_bp
#     app.register_blueprint(graph_bp)
    
#     # Ensure the templates directory exists
#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
#     os.makedirs(templates_dir, exist_ok=True)
    
#     # Ensure the static directory exists
#     static_dir = os.path.join(os.path.dirname(__file__), 'static')
#     os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
#     os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
    
#     # Create main route
#     @app.route('/')
#     def index():
#         return render_template('index.html')
    
    # return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)