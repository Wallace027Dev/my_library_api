from app import ma
from app.models import Book, WishlistItem
from marshmallow import fields, post_load


class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    author = ma.auto_field(required=True)
    img_url = ma.auto_field(required=True)
    categories = fields.List(fields.String(), required=True)
    status_read = ma.auto_field(load_default='unread')
    rating = ma.auto_field(required=False, allow_none=True)
    
    @post_load
    def make_book(self, data, **kwargs):
        if 'categories' in data:
            data['categories_list'] = data.pop('categories')
        return Book(**data)


class WishlistItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WishlistItem
        load_instance = True

    id = ma.auto_field(dump_only=True)
    title = ma.auto_field(required=True)
    author = ma.auto_field(required=True)
    img_url = ma.auto_field(required=True)
    categories = fields.List(fields.String(), required=True)

    @post_load
    def make_wishlist_item(self, data, **kwargs):
        if 'categories' in data:
            data['categories_list'] = data.pop('categories')
        return WishlistItem(**data)


book_schema = BookSchema()
wishlist_item_schema = WishlistItemSchema()
