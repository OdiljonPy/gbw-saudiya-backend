from ..models import Category
from ..serializers import CategorySerializer
from django.core.paginator import Paginator
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count,Q

def get_categories_list(context:dict,page=1,size=20,search=None):
    category_query = Category.objects.all().order_by('id')
    if search:
        category_query = category_query.annotate(
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

    total_count = category_query.aggregate(total_count=Count('id'))['total_count']
    paginator = Paginator(category_query,size)
    categories = paginator.get_page(page)

    response ={
        'count':total_count,
        'total_pages':paginator.num_pages,
        'previous':categories.has_previous(),
        'next':categories.has_next(),
        'result':CategorySerializer(categories,many=True,context=context).data
    }
    return response

