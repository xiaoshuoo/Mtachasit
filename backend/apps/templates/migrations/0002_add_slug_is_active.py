from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Template = apps.get_model('templates', 'GutierrezTemplate')
    existing_slugs = set(
        Template.objects.exclude(slug__isnull=True).exclude(slug__exact='').values_list('slug', flat=True)
    )

    def unique_slug(base: str) -> str:
        base = slugify(base) or 'template'
        candidate = base
        counter = 2
        while candidate in existing_slugs:
            candidate = f"{base}-{counter}"
            counter += 1
        existing_slugs.add(candidate)
        return candidate

    for obj in Template.objects.all():
        if not obj.slug:
            obj.slug = unique_slug(obj.title)
            obj.save(update_fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [
        ('templates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gutierreztemplate',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='gutierreztemplate',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='gutierreztemplate',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]

