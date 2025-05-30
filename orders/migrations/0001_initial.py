# Generated by Django 5.2 on 2025-05-19 06:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivery_type', models.CharField(choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')], max_length=20)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.TimeField()),
                ('comment', models.TextField(blank=True, help_text='Дополнительная информация для доставки', verbose_name='Комментарий')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('pending', 'Ожидание'), ('confirmed', 'Успешно'), ('rejected', 'Неуспешно')], default='pending', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user', '-created_at'], name='orders_orde_user_id_0ae59f_idx'),
        ),
    ]
