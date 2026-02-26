from ..models import Category
from ..serializers import CategorySerializer
from django.core.paginator import Paginator
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from django.utils.translation import get_language

def get_categories_list(context:dict,page=1,size=20,search=None):
    category_query = Category.objects.all().order_by('id')
    if search:
        lang = get_language()
        search_field = f"name_{lang}"
        category_query = category_query.annotate(
            similarity=TrigramSimilarity(search_field, search)
        ).filter(similarity__gte=0.1)

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

