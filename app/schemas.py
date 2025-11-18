from app import ma
from app.models import Book, WishlistItem
from marshmallow import fields, validate, post_load, post_dump
from marshmallow.fields import Method
from app.enums import BookCategory


class BookSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    author = fields.String(required=True)
    img_url = fields.String(required=True)
    categories = Method("get_categories", deserialize="load_categories")
    status_read = fields.String(load_default='unread')
    rating = fields.Integer(
        required=False,
        allow_none=True,
        validate=validate.Range(min=1, max=5)
    )
    
    def get_categories(self, obj):
        """Serializa categories_list para a saída"""
        return obj.categories_list if hasattr(obj, 'categories_list') else []
    
    def load_categories(self, value):
        """Valida e retorna as categorias na entrada"""
        if not isinstance(value, list):
            raise validate.ValidationError("Categories deve ser uma lista")
        for cat in value:
            if cat not in BookCategory.list():
                raise validate.ValidationError(f"Categoria inválida: {cat}")
        return value


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
