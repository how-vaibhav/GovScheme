# Generated migration - Change age field from IntegerField to CharField with age ranges

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schemesapp', '0026_scheme_application_deadline_scheme_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='age',
            field=models.CharField(
                choices=[
                    ('18-25', '18-25 years'),
                    ('26-35', '26-35 years'),
                    ('36-45', '36-45 years'),
                    ('46-55', '46-55 years'),
                    ('56-65', '56-65 years'),
                    ('65+', '65 years and above'),
                ],
                default='18-25',
                max_length=20
            ),
        ),
    ]
