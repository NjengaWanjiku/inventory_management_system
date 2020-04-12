from app import db

class InventoryModel(db.Model): 
    __tablename__  = 'new_inventories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    inv_type = db.Column(db.String(100), nullable=False)
    buying_price = db.Column(db.Float)
    selling_price = db.Column(db.Float, nullable=False)