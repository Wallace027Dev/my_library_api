from app import ma
from app.models import Book, WishlistItem
from marshmallow import fields, validate, post_load, post_dump
from app.enums import BookCategory


class BookSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    img_url = fields.String(required=True)
    categories = fields.List(
        fields.String(
            validate=validate.OneOf(
                BookCategory.list()
            )),
        required=True
    )
    status_read = fields.String(load_default='unread')
    rating = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1, max=5)
    )
    
    @post_dump
    def dump_book(self, data, **kwargs):
        # Sempre sobrescreve categories com a lista do objeto
        obj = self.context.get('obj')
        if obj and hasattr(obj, 'categories_list'):
            data['categories'] = obj.categories_list
        return data


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
        categories = data.pop('categories', None)
        item = WishlistItem(**data)
        if categories:
            item.categories_list = categories
        return item

    @post_dump
    def dump_wishlist_item(self, data, **kwargs):
        # Sempre sobrescreve categories com a lista do objeto
        obj = kwargs.get('obj')
        if obj:
            data['categories'] = obj.categories_list
        return data


book_schema = BookSchema()
wishlist_item_schema = WishlistItemSchema()
