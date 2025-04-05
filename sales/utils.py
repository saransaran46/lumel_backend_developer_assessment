import csv
import logging
from datetime import datetime
from django.db import transaction
from .models import Customer, Product, Order, OrderItem

logger = logging.getLogger(__name__)

def load_sales_data_from_csv(file_path, overwrite=False):
    """
    Load sales data from CSV file into the database
    """
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            
            with transaction.atomic():
                if overwrite:
                    # Clear existing data if overwrite is True
                    OrderItem.objects.all().delete()
                    Order.objects.all().delete()
                    Product.objects.all().delete()
                    Customer.objects.all().delete()
                    logger.info("Existing data cleared for fresh import")
                
                for row in reader:
                    # Create or update Customer
                    customer, _ = Customer.objects.update_or_create(
                        customer_id=row['Customer ID'],
                        defaults={
                            'name': row['Customer Name'],
                            'email': row['Customer Email'],
                            'address': row['Customer Address']
                        }
                    )
                    
                    # Create or update Product
                    product, _ = Product.objects.update_or_create(
                        product_id=row['Product ID'],
                        defaults={
                            'name': row['Product Name'],
                            'category': row['Category'],
                            'description': row.get('Product Description', '')
                        }
                    )
                    
                    # Create or update Order
                    order, created = Order.objects.update_or_create(
                        order_id=row['Order ID'],
                        defaults={
                            'customer': customer,
                            'date_of_sale': datetime.strptime(row['Date of Sale'], '%Y-%m-%d').date(),
                            'payment_method': row['Payment Method'],
                            'region': row['Region'],
                            'shipping_cost': float(row['Shipping Cost'])
                        }
                    )
                    
                    # Create or update OrderItem
                    OrderItem.objects.update_or_create(
                        order=order,
                        product=product,
                        defaults={
                            'quantity': int(row['Quantity Sold']),
                            'unit_price': float(row['Unit Price']),
                            'discount': float(row['Discount'])
                        }
                    )
                    
                    row_count += 1
                    
                    if row_count % 1000 == 0:
                        logger.info(f"Processed {row_count} rows")
                
                logger.info(f"Successfully loaded {row_count} rows from CSV")
                return True, f"Successfully loaded {row_count} rows"
    
    except Exception as e:
        logger.error(f"Error loading CSV data: {str(e)}")
        return False, str(e)