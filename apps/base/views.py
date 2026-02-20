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
    OrderSerializer
)
from .repository.get_products import get_products_list

class BannerViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: BannerSerializer()},
        tags=['Banner'],
        operation_description="Banner details"
    )
    def get_banner(self,request):
        language = request.headers.get("Accept-Language","ru")
        if language.startswith("uz"):
            activate("uz")
        elif language.startswith("en"):
            activate("en")
        elif language.startswith("ru"):
            activate("ru")
        elif language.startswith("ar"):
            activate("ar")
        else:
            activate("ru")


        banner = Banner.objects.all()
        serializer = BannerSerializer(banner, many=True,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)

class SponsorshipViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: SponsorshipSerializer()},
        tags=['Sponsorship'],
        operation_description="Sponsor details"
    )
    def get_sponsorship(self,request):
        sponsorship = Sponsorship.objects.all()
        serializer = SponsorshipSerializer(sponsorship,many=True,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)

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
        language = request.headers.get("Accept-Language", "ru")
        if language.startswith("uz"):
            activate("uz")
        elif language.startswith("en"):
            activate("en")
        elif language.startswith("ru"):
            activate("ru")
        elif language.startswith("ar"):
            activate("ar")
        else:
            activate("ru")
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
        operation_description="Product detail",
    )
    def get_product_detail(self,request,pk=None):
        language = request.headers.get("Accept-Language", "ru")
        if language.startswith("uz"):
            activate("uz")
        elif language.startswith("en"):
            activate("en")
        elif language.startswith("ru"):
            activate("ru")
        elif language.startswith("ar"):
            activate("ar")
        else:
            activate("ru")
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response({"message":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ProductSerializer()},
        tags=['Product'],
        operation_description="Product recommendation",
    )
    def get_product_recommendation(self,request,pk=None):
        language = request.headers.get("Accept-Language", "ru")
        if language.startswith("uz"):
            activate("uz")
        elif language.startswith("en"):
            activate("en")
        elif language.startswith("ru"):
            activate("ru")
        elif language.startswith("ar"):
            activate("ar")
        else:
            activate("ru")
        main_product = Product.objects.filter(id=pk).first()
        if not main_product:
            return Response({"message":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        products = Product.objects.filter(category=main_product.category)[:4]
        serializer = ProductSerializer(products,context={"request":request},many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


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
            )
        ]
    )
    def get_category_list(self,request):
        language = request.headers.get("Accept-Language", "ru")
        if language.startswith("uz"):
            activate("uz")
        elif language.startswith("en"):
            activate("en")
        elif language.startswith("ru"):
            activate("ru")
        elif language.startswith("ar"):
            activate("ar")
        else:
            activate("ru")
        search = request.query_params.get("search",None)
        category = Category.objects.all()
        if search:
            category = category.annotate(
                similarity=TrigramSimilarity('name', search)
            ).filter(similarity__gte=0.08)
        serializer = CategorySerializer(category,many=True,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)


class AboutUsViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: AboutUsSerializer()},
        tags=['AboutUs'],
        operation_description="About Us",
    )
    def get_about_us(self,request):
        language = request.headers.get("Accept-Language", "ru")
        if language.startswith("uz"):
            activate("uz")
        elif language.startswith("en"):
            activate("en")
        elif language.startswith("ru"):
            activate("ru")
        elif language.startswith("ar"):
            activate("ar")
        else:
            activate("ru")
        about_us = AboutUs.objects.all()
        serializer = AboutUsSerializer(about_us,context={"request":request},many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class OrderViewSet(ViewSet):
    @swagger_auto_schema(
        responses={200: OrderSerializer()},
        request_body=OrderSerializer(),
        tags=['Order'],
        operation_description="Order details",
    )
    def create_order(self,request):
        product = Product.objects.filter(id=request.data["product_id"]).first()
        if not product:
            return Response({"message":"Product not found"},status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data,status=status.HTTP_200_OK)