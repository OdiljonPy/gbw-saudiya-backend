from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.postgres.search import TrigramSimilarity
from django.utils.translation import activate
from .models import (
    Banner,
    Sponsorship,
    Message,
    Product,
    Category,
    AboutUs,
    Order
)
from .serializers import (
    BannerSerializer,
    SponsorshipSerializer,
    MessageSerializer,
    ProductSerializer,
    CategorySerializer,
    AboutUsSerializer,
    OrderSerializer,
    CategoryDetailSerializer
)
from .repository.get_products import get_products_list
from .repository.get_categories import get_categories_list
class BannerViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: BannerSerializer()},
        tags=['Banner'],
        operation_description="Banner details"
    )
    def get_banner(self,request):
        banner = Banner.objects.order_by("-created_at").first()
        serializer = BannerSerializer(banner,context={"request":request})
        return Response({'result':serializer.data},status=status.HTTP_200_OK)

class SponsorshipViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: SponsorshipSerializer()},
        tags=['Sponsorship'],
        operation_description="Sponsor details"
    )
    def get_sponsorship(self,request):
        sponsorship = Sponsorship.objects.all()
        serializer = SponsorshipSerializer(sponsorship,many=True,context={"request":request})
        return Response({'result':serializer.data},status=status.HTTP_200_OK)

class MessageViewSet(ViewSet):
    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={200: MessageSerializer()},
        tags=['Message'],
        operation_description="Message create",

    )
    def create_message(self,request):
        serializer = MessageSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class ProductViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Product details",
        responses={200: ProductSerializer()},
        tags=['Product'],
        manual_parameters=[
            openapi.Parameter(
                name = "page",
                in_= openapi.IN_QUERY,
                description = "Page",
                type = openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name = "size",
                in_= openapi.IN_QUERY,
                description = "Size",
                type = openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name = "category_id",
                in_= openapi.IN_QUERY,
                description = "Category id",
                type = openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name = "search",
                in_= openapi.IN_QUERY,
                description = "Search",
                type = openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name = "type",
                in_= openapi.IN_QUERY,
                description = "Type",
                enum = ["new","min","max"],
                type = openapi.TYPE_STRING,
            ),

        ],
    )
    def get_products_by_category(self,request):
        page = request.query_params.get("page",1)
        size = request.query_params.get("size",20)
        category_id = request.query_params.get("category_id",None)
        search = request.query_params.get("search",None)
        type = request.query_params.get("type",None)
        products = get_products_list(context={"request":request},
                                     page=page,
                                     size=size,
                                     category_id=category_id,
                                     search = search,
                                    type=type
                                     )
        return Response(products,status=status.HTTP_200_OK)


    @swagger_auto_schema(
        responses={200: ProductSerializer()},
        tags=['Product'],
        operation_description="Product recommendation",
    )
    def get_product_recommendation(self,request,pk=None):
        main_product = Product.objects.filter(id=pk).first()
        if not main_product:
            return Response({"message":"Product not found"},status=status.HTTP_404_NOT_FOUND)

        recommendations = Product.objects.filter(category=main_product.category).exclude(id=pk)[:4]

        main_serializer = ProductSerializer(main_product,context={"request":request})
        rec_serializer = ProductSerializer(recommendations,many=True,context={"request":request})

        response = main_serializer.data
        response["recommendations"] = rec_serializer.data
        return Response({'result':response},status=status.HTTP_200_OK)






class CategoryViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: CategorySerializer()},
        tags=['Category'],
        operation_description="Category details",
        manual_parameters=[
            openapi.Parameter(
                name = "search",
                in_= openapi.IN_QUERY,
                description = "Search",
                type = openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name = "page",
                in_= openapi.IN_QUERY,
                description = "Page",
                type = openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                name = "size",
                in_= openapi.IN_QUERY,
                description = "Size",
                type = openapi.TYPE_INTEGER,
            )
        ]
    )
    def get_category_list(self,request):
        search = request.query_params.get("search",None)
        page = request.query_params.get("page",1)
        size = request.query_params.get("size",20)
        categories = get_categories_list(context={"request":request},
                                         page=page,
                                         size=size,
                                         search=search)
        return Response(categories,status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: CategoryDetailSerializer()},
        tags=['Category'],
        operation_description="Category details",
    )
    def get_category_detail(self,request,pk=None):
        category = Category.objects.filter(id=pk).first()
        if not category:
            return Response({"message":"Category not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryDetailSerializer(category,context={"request":request})
        return Response({'result':serializer.data},status=status.HTTP_200_OK)

class AboutUsViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: AboutUsSerializer()},
        tags=['AboutUs'],
        operation_description="About Us",
    )
    def get_about_us(self,request):
        about_us = AboutUs.objects.order_by('-created_at').first()
        serializer = AboutUsSerializer(about_us,context={"request":request})
        return Response({'result':serializer.data},status=status.HTTP_200_OK)

class OrderViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: OrderSerializer()},
        request_body=OrderSerializer(),
        tags=['Order'],
        operation_description="Order details",
    )
    def create_order(self,request):
        serializer = OrderSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)