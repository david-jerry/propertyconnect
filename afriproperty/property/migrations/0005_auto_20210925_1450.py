# Generated by Django 3.1.13 on 2021-09-25 13:50

import afriproperty.property.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_auto_20210925_0558'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('property_features', models.CharField(blank=True, choices=[('Air Conditioning', 'Air Conditioning'), ('Swimming Pool', 'Swimming Pool'), ('Central Heating', 'Central Heating'), ('Laundry Room', 'Laundry Room'), ('Parking Lot', 'Parking Lot'), ('Exercise Room', 'Exercise Room'), ('Central Cooling', 'Central Cooling'), ('Srorage Room', 'Srorage Room'), ('Treated Water', 'Treated Water'), ('Gym', 'Gym'), ('Alarm', 'Alarm')], default='Swimming Pool', max_length=17, null=True, unique=True, verbose_name='Property Features (Optional)')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('image', django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', help_text='image size: 520x397.', keep_meta=True, null=True, quality=80, size=[520, 397], upload_to=afriproperty.property.models.property_images)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='property',
            name='property_expire',
            field=models.IntegerField(blank=True, default=0, help_text='use 100 if it a land that is being purchased. and any figure when it is a rentage. NOTE: An additional 2 months is given to a property before it is reactivated as availble for purchase after its last purchased date', null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='property_sold',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='property',
            name='property_features',
        ),
        migrations.AlterField(
            model_name='propertyblueprint',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format='JPEG', help_text='image size: 1000x576.', keep_meta=True, null=True, quality=70, size=[1000, 576], upload_to=afriproperty.property.models.blueprint_image),
        ),
        migrations.DeleteModel(
            name='PropertyImageField',
        ),
        migrations.AddField(
            model_name='propertyimage',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyimage', to='property.property'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_features',
            field=models.ManyToManyField(blank=True, help_text='Select all features that apply for the house', null=True, to='property.PropertyFeature'),
        ),
    ]
