from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('icon', models.CharField(default='fas fa-folder', max_length=50, verbose_name='Иконка')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Категория лекций',
                'verbose_name_plural': 'Категории лекций',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название лекции')),
                ('content', models.TextField(verbose_name='Содержание лекции')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lectures', to='lectures.lecturecategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Лекция',
                'verbose_name_plural': 'Лекции',
                'ordering': ['-created_at'],
            },
        ),
    ]


