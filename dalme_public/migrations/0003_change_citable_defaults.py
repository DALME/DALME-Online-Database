from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_public', '0002_auto_20201016_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='citable',
            field=models.BooleanField(default=True, help_text='Check this box to show the "Cite" menu for this page.'),
        ),
        migrations.AlterField(
            model_name='collections',
            name='citable',
            field=models.BooleanField(default=True, help_text='Check this box to show the "Cite" menu for this page.'),
        ),
        migrations.AlterField(
            model_name='essay',
            name='citable',
            field=models.BooleanField(default=True, help_text='Check this box to show the "Cite" menu for this page.'),
        ),
        migrations.AlterField(
            model_name='featuredinventory',
            name='citable',
            field=models.BooleanField(default=True, help_text='Check this box to show the "Cite" menu for this page.'),
        ),
        migrations.AlterField(
            model_name='featuredobject',
            name='citable',
            field=models.BooleanField(default=True, help_text='Check this box to show the "Cite" menu for this page.'),
        )
    ]
