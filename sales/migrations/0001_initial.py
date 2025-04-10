# Generated by Django 4.2 on 2025-04-05 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
            ],
            options={
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('date_of_sale', models.DateField()),
                ('payment_method', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('shipping_cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='products_categor_fce6e6_idx'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='sales.customer'),
        ),
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together={('order', 'product')},
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['date_of_sale'], name='orders_date_of_ac2a13_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['region'], name='orders_region_6e49bf_idx'),
        ),
    ]
