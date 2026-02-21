from ..models import Category
from ..serializers import CategorySerializer
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity


def get_categories_list(context:dict,page=1,size=20,search=None):
    category_query = Category.objects.all()
    if search:
        category_query = category_query.annotate(
            similarity=TrigramSimilarity('name', search)
        ).filter(similarity__gte=0.08)

    total_count = category_query.aggregate(total_count=Count('id'))['total_count']
    paginator = Paginator(category_query,size)
    categories = paginator.get_page(page)

    response = {
        'totalElements': total_count,
        'totalPages': paginator.num_pages,
        'size': size,
        'number': page,
        'numberOfElements': len(categories),
        'first': not categories.has_previous(),
        'last': not categories.has_next(),
        'empty': total_count == 0,
        'content': CategorySerializer(categories, many=True, context=context).data

    }

    return response