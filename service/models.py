"""
Models for Your Service

This module contains the model definitions for your service
"""
from . import db

class Account(db.Model):
    """
    Class that represents an Account
    """
    id = db.Column(db.Integer, primary_key=True)
    # Add your other model fields (e.g., name, email) here

    def __repr__(self):
        return f"<Account {self.id}>"

    def serialize(self):
        """Serializes a Account into a dictionary"""
        return {
            "id": self.id,
            # Add your other fields here
        }

    def deserialize(self, data):
        """
        Deserializes a Account from a dictionary
        """
        try:
            self.id = data["id"]
            # Add your other fields here
        except KeyError as error:
            raise ValueError(f"Invalid Account data: missing {error.args[0]}")
        except TypeError:
            raise ValueError("Invalid Account data: data must be a dictionary")
        return self

######################################################################
#  D A T A B A S E   I N I T I A L I Z E R
######################################################################

def init_db(app):
    """Initializes the database tables"""
    app.logger.info("Initializing database...")
    with app.app_context():
        db.create_all()