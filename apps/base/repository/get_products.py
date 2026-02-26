from ..models import Product
from ..serializers import ProductSerializer
from django.core.paginator import Paginator
from django.db.models import Count,Q
from django.contrib.postgres.search import TrigramSimilarity

def get_products_list(context:dict,page=1,size=20,category_id=None,search=None,type=None):
    product_query = Product.objects.all()
    if category_id:
        product_query = product_query.filter(category_id=category_id)

    if search:
        product_query = product_query.annotate(
            sim_uz=TrigramSimilarity('name_uz', search),
            sim_ru=TrigramSimilarity('name_ru', search),
            sim_en=TrigramSimilarity('name_en', search),
            sim_ar=TrigramSimilarity('name_ar', search),
        ).filter(
            Q(sim_uz__gte=0.1) |
            Q(sim_ru__gte=0.1) |
            Q(sim_en__gte=0.1) |
            Q(sim_ar__gte=0.1)
        )

    if type == 'new':
        product_query = product_query.order_by('-created_at')
    if type == 'min':
        product_query = product_query.order_by('price')
    if type == 'max':
        product_query = product_query.order_by('-price')



    total_count = product_query.aggregate(total_count=Count('id'))['total_count']
    paginator = Paginator(product_query,size)
    products = paginator.get_page(page)

    response = {
        'count': total_count,
        'total_pages': paginator.num_pages,
        'previous': products.has_previous(),
        'next': products.has_next(),
        'result': ProductSerializer(products,many=True,context=context).data
    }
    return response