class Blueprint:

    @staticmethod
    def init_app(app):
        from .auth import auth
        app.register_blueprint(auth, url_prefix='/auth')

        from .account import account
        app.register_blueprint(account, url_prefix='/account')

        from .posts import posts
        app.register_blueprint(posts, url_prefix='/posts')

        from app.utils import build_response
        @app.errorhandler(404)
        @app.errorhandler(405)
        def handle_404(_):
            return build_response(404, 'Invalid request path or method.')
        
        from app.validator import ValidationError
        @app.errorhandler(ValidationError)
        def handle_validation_error(err):
            return build_response(400, str(err))
        
        @app.errorhandler(Exception)
        def handle_exceptions(err):
            # Log errors to a logging service here
            # Returning generic message to user so we don't leak any secrets
            print(err)
            return build_response(500, 'Server error occurred.')