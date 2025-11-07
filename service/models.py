"""
Models for Account

All of the models are stored in this module
"""
import logging
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from . import db
logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Account.init_db(app)


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    def create(self):
        """
        Creates a Account to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Account to the database
        """
        logger.info("Updating %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Account from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def init_db(app):
        """Initializes the database tables"""
        app.logger.info("Initializing database...")
        with app.app_context():
            db.create_all()  # <-- THIS IS THE FIX

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


######################################################################
#  A C C O U N T   M O D E L
######################################################################
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'balance': self.balance
        }