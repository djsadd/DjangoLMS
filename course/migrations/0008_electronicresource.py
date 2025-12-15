from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_course_semester'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectronicResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(blank=True, help_text='Upload a document or archive. Leave empty if you only provide a link.', null=True, upload_to='library/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'zip', 'rar'])])),
                ('link', models.URLField(blank=True, help_text='Optional external link to the resource.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'Electronic Resource',
                'verbose_name_plural': 'Electronic Resources',
            },
        ),
    ]
