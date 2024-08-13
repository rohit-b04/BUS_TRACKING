from Buses import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class bus_info(db.Model):
    bus_id = db.Column(db.String(length=60), primary_key=True)
    current_stop=db.Column(db.String(length=60), nullable=False)
    dest_stop=db.Column(db.String(length=70), nullable=True)
    req_time_to_arrive_at_cur = db.Column(db.String(length=60), nullable=False)
    route_id=db.Column(db.String(length=70), db.ForeignKey('bus_routes.route_id'), nullable=False)
    #relations=db.Column(db.String(length=70), db.ForeignKey('bus_id'))
    def __repr__(self):
        return f'bus_info {self.current_stop}'

class bus_routes(db.Model):
    route_id=db.Column(db.String(length=70), nullable=False, primary_key=True)
    from_stop=db.Column(db.String(length=70), nullable=False)
    to_stop=db.Column(db.String(length=70), nullable=False)

