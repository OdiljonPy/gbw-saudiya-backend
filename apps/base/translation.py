from modeltranslation.translator import TranslationOptions,translator
from .models import (
    Product,
    Banner,
    Category,
    Statistics,
    AboutUs

)

class ProductTranslationOptions(TranslationOptions):
    fields = ('name','description' )

translator.register(Product,ProductTranslationOptions)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category,CategoryTranslationOptions)

class BannerTranslationOptions(TranslationOptions):
    fields = ('title','description')

translator.register(Banner,BannerTranslationOptions)

class StatisticsTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(Statistics,StatisticsTranslationOptions)

class AboutUsTranslationOptions(TranslationOptions):
    fields = ('name','subtitle','description')
translator.register(AboutUs,AboutUsTranslationOptions)