from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.utils import timezone
from datetime import timedelta
from .models import Product, Order, OrderItem
from .serializers import (
    RevenueAnalysisSerializer,
    TopProductsSerializer,
    OrderSerializer
)
from .utils import load_sales_data_from_csv
import os

class DataRefreshView(APIView):
    def post(self, request):
        """
        Trigger data refresh from CSV file
        """
        csv_file_path = os.path.join(os.path.dirname(__file__), 'data/sales_data.csv')
        
        if not os.path.exists(csv_file_path):
            return Response(
                {"error": "CSV file not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        overwrite = request.data.get('overwrite', False)
        success, message = load_sales_data_from_csv(csv_file_path, overwrite)
        
        if success:
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

class RevenueAnalysisView(APIView):
    def post(self, request):
        """
        Calculate revenue metrics with optional grouping
        """
        serializer = RevenueAnalysisSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        start_date = data['start_date']
        end_date = data['end_date']
        group_by = data.get('group_by')
        
        items = OrderItem.objects.filter(
            order__date_of_sale__range=(start_date, end_date)
        ).annotate(
            total_revenue=ExpressionWrapper(
                F('quantity') * F('unit_price') * (1 - F('discount')),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
        
        if group_by is None:
            # Total revenue for the period
            total_revenue = items.aggregate(
                total=Sum('total_revenue')
            )['total'] or 0
            
            return Response({
                "start_date": start_date,
                "end_date": end_date,
                "total_revenue": total_revenue
            })
        
        elif group_by == 'product':
            # Group by product
            results = items.values(
                'product__product_id', 'product__name'
            ).annotate(
                total_revenue=Sum('total_revenue')
            ).order_by('-total_revenue')
            
            return Response({
                "start_date": start_date,
                "end_date": end_date,
                "group_by": "product",
                "results": list(results)
            })
        
        elif group_by == 'category':
            # Group by category
            results = items.values(
                'product__category'
            ).annotate(
                total_revenue=Sum('total_revenue')
            ).order_by('-total_revenue')
            
            return Response({
                "start_date": start_date,
                "end_date": end_date,
                "group_by": "category",
                "results": list(results)
            })
        
        elif group_by == 'region':
            # Group by region
            results = items.values(
                'order__region'
            ).annotate(
                total_revenue=Sum('total_revenue')
            ).order_by('-total_revenue')
            
            return Response({
                "start_date": start_date,
                "end_date": end_date,
                "group_by": "region",
                "results": list(results)
            })

class TopProductsView(APIView):
    def post(self, request):
        """
        Get top N products by quantity sold with optional filters
        """
        serializer = TopProductsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        start_date = data['start_date']
        end_date = data['end_date']
        limit = data['limit']
        category = data.get('category')
        region = data.get('region')
        
        items = OrderItem.objects.filter(
            order__date_of_sale__range=(start_date, end_date)
        )
        
        if category:
            items = items.filter(product__category=category)
        
        if region:
            items = items.filter(order__region=region)
        
        top_products = items.values(
            'product__product_id', 'product__name', 'product__category'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(
                ExpressionWrapper(
                    F('quantity') * F('unit_price') * (1 - F('discount')),
                    output_field=DecimalField(max_digits=12, decimal_places=2)
                )
            )
        ).order_by('-total_quantity')[:limit]
        
        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "category_filter": category,
            "region_filter": region,
            "limit": limit,
            "top_products": list(top_products)
        })

class CustomerAnalysisView(APIView):
    def post(self, request):
        """
        Basic customer analysis metrics
        """
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {"error": "Both start_date and end_date are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Number of unique customers
        customer_count = Order.objects.filter(
            date_of_sale__range=(start_date, end_date)
        ).values('customer').distinct().count()
        
        # Number of orders
        order_count = Order.objects.filter(
            date_of_sale__range=(start_date, end_date)
        ).count()
        
        # Average order value
        order_values = OrderItem.objects.filter(
            order__date_of_sale__range=(start_date, end_date)
        ).annotate(
            item_value=ExpressionWrapper(
                F('quantity') * F('unit_price') * (1 - F('discount')),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        ).aggregate(
            total_revenue=Sum('item_value')
        )
        
        avg_order_value = (order_values['total_revenue'] or 0) / order_count if order_count > 0 else 0
        
        return Response({
            "start_date": start_date,
            "end_date": end_date,
            "customer_count": customer_count,
            "order_count": order_count,
            "average_order_value": round(avg_order_value, 2)
        })