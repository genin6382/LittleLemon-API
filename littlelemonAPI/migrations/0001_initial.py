# Generated by Django 3.2.25 on 2024-06-19 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('title', models.CharField(db_index=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=5)),
                ('featured', models.BooleanField(db_index=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='menu_items', to='littlelemonAPI.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(db_index=True, default=0)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.DateTimeField(db_index=True)),
                ('delivery_crew', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deliveries', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='littlelemonAPI.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='littlelemonAPI.order')),
            ],
            options={
                'unique_together': {('order', 'menu_item')},
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='littlelemonAPI.menuitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'menu_item')},
            },
        ),
    ]
