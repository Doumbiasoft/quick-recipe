from app.extensions import Flask, db,DebugToolbarExtension,Session,Object2Json,numpy,render_template,CURR_USER_KEY,session,g
from config import Config
from app.models.users import User
def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize the session extension
    Session(app)
    DebugToolbarExtension(app)

    """Initialize Flask extensions here"""
    db.init_app(app)


    """------------------END----------------------------------------------"""

    """Register blueprint here"""
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.search import bp as search_bp
    app.register_blueprint(search_bp, url_prefix='/search')

    """------------------END----------------------------------------------"""
    
    @app.before_request
    def add_user_to_g():
        """If we're logged in, add curr user to Flask global."""

        #set expiration time
        #session.permanent = True
        #app.permanent_session_lifetime = timedelta(minutes=1)
        #session.modified = True
       #------end expiration time setting ------

        if CURR_USER_KEY in session:
            g.user = User.query.get(session[CURR_USER_KEY])
        else:
            g.user = None

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(401)
    def access_denied(e):
        return render_template('401.html'), 401


    @app.context_processor
    def utility_simplenamespace():
        def obj_to_json(obj):
            return Object2Json(obj)
        return dict(obj_to_json=obj_to_json)

    @app.context_processor
    def utility_processor():
        def generate_float_range(x:float,y:float):
            return numpy.arange(x, y)
        return dict(generate_float_range=generate_float_range)


    return app