# from flask import Flask

# def create_app():
#     app = Flask(__name__, 
#             template_folder=os.path.join(basedir, 'templates'),
#             static_folder=os.path.join(basedir, 'static'))
#     # app.config['SECRET_KEY'] = 'your-secret-key'
    
#     # Register blueprints
#     from .views import views
#     from .auth import auth
    
#     app.register_blueprint(views, url_prefix='/')
#     app.register_blueprint(auth, url_prefix='/')
    
#     return app