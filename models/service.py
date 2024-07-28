from init import db, ma

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)
    service_price = db.Column(db.Float, nullable=False)

class ServiceSchema(ma.Schema):
    class Meta:
        fields = ("id", "service_name", "description", "service_price")

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
