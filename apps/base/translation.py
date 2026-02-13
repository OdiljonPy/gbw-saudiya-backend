from modeltranslation.translator import TranslationOptions,translator
from .models import (
    Product,
    Banner,
    Category
)

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Product,ProductTranslationOptions)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category,CategoryTranslationOptions)

class BannerTranslationOptions(TranslationOptions):
    fields = ('title','description')

translator.register(Banner,BannerTranslationOptions)