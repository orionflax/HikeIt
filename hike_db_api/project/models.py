from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY,FLOAT

db = SQLAlchemy()

class Routes(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True)
    # Define a two-dimensional array using ARRAY. 
    # For other databases, you'll need to use the appropriate data type or JSON.
    route_mappings = db.Column(ARRAY(db.Integer, dimensions=2), nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    ascent = db.Column(db.Integer, nullable=False)
    max_height = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    average_location = db.Column(ARRAY(db.FLOAT,dimensions=1),nullable=False)
    
    def __repr__(self):
        return f'<Routes {self.name}>'
    
    def __init__(self, route_mappings, distance, ascent, max_height, name):
        self.route_mappings = route_mappings
        self.distance = distance
        self.ascent = ascent
        self.max_height = max_height
        self.name = name
