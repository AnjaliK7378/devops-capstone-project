"""
Package: service
"""
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ---
# IMPORT 'MODELS' AND INITIALIZE DATABASE
# We import models FIRST so that 'models.init_db(app)' can be called
# pylint: disable=wrong-import-position
from service import models  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T  S E R V I C E  R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

# ---
# IMPORT 'ROUTES' AND OTHER MODULES *AFTER* DATABASE IS READY
# We import these LAST to avoid circular dependencies
# pylint: disable=wrong-import-position
from service import routes  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Register the blueprints
app.register_blueprint(routes.bp)

app.logger.info("Service initialized!")