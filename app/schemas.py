from app import ma
from app.models import Book, WishlistItem


class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    author = ma.auto_field(required=True)
    img_url = ma.auto_field(required=True)
    category = ma.auto_field(required=True)
    status_read = ma.auto_field(load_default='unread')
    rating = ma.auto_field(required=False, allow_none=True)

class WishlistItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WishlistItem
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    author = ma.auto_field(required=True)
    img_url = ma.auto_field(required=True)
    category = ma.auto_field(required=True)

book_schema = BookSchema()
wishlist_item_schema = WishlistItemSchema()
