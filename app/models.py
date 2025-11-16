from app import db


class BaseBook:
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.title} by {self.author}>"


class Book(BaseBook, db.Model):
    __tablename__ = 'books'
    
    status_read = db.Column(
        db.Enum('read', 'reading', 'unread', name='status_read_enum'), 
        default='unread',
        nullable=False
    )
    rating = db.Column(db.Integer, nullable=True)
    __table_args__= (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range_check'),
    )


class WishlistItem(BaseBook, db.Model):
    __tablename__ = 'wishlist_items'
