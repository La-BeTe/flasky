
class Blueprint:

    @staticmethod
    def init_app(app):
        from .auth import auth
        app.register_blueprint(auth, url_prefix='/auth')

        from .account import account
        app.register_blueprint(account, url_prefix='/account')

        from app.utils import build_response
        @app.errorhandler(404)
        @app.errorhandler(405)
        def handle_404(_):
            return build_response(404, 'Invalid request path or method.')
        
        @app.errorhandler(Exception)
        def handle_exceptions(err):
            # Log errors to a logging service here
            # Returning generic message to user so wee don't leak any secrets
            print(err)
            return build_response(500, 'Server error occurred.')