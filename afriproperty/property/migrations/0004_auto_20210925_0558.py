# Generated by Django 3.1.13 on 2021-09-25 04:58

import afriproperty.property.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_property_property_near_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_bathrooms',
            field=models.IntegerField(choices=[(1, '1  Room'), (2, '2  Rooms'), (3, '3  Rooms'), (4, '4  Rooms'), (5, '5  Rooms'), (0, 'More than 5 Rooms')], default=1, null=True, verbose_name='Bath Rooms'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_latitude',
            field=models.FloatField(default=0.0, help_text='You can find this on google maps by inputing the actual property address and right clicking on the location pointer to reveal the latitude', null=True, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)], verbose_name='Map Latitude'),
        ),
        migrations.AddField(
            model_name='property',
            name='property_longitude',
            field=models.FloatField(default=0.0, help_text='You can find this on google maps by inputing the actual property address and right clicking on the location pointer to reveal the longitude', null=True, validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180.0)], verbose_name='Map Longitude'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_features',
            field=models.CharField(blank=True, choices=[('Air Conditioning', 'Air Conditioning'), ('Swimming Pool', 'Swimming Pool'), ('Central Heating', 'Central Heating'), ('Laundry Room', 'Laundry Room'), ('Parking Lot', 'Parking Lot'), ('Exercise Room', 'Exercise Room'), ('Central Cooling', 'Central Cooling'), ('Srorage Room', 'Srorage Room'), ('Treated Water', 'Treated Water'), ('Gym', 'Gym'), ('Alarm', 'Alarm')], default='Swimming Pool', max_length=17, null=True, verbose_name='Property Features (Optional)'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_location',
            field=models.CharField(help_text='eg. 123 Close, Street  !!! PS: Do not attach a state or country when listing this property !!!', max_length=500, null=True, verbose_name='Street Address'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_near_location',
            field=models.CharField(help_text='eg. 123 Close, Street  !!! PS: Do not attach a state or country when listing this property !!!', max_length=500, null=True, verbose_name='Property Closest building street address'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_price_type',
            field=models.CharField(choices=[('Annually', 'Annually'), ('Monthly', 'Monthly'), ('Sq/Ft', 'Sq/Ft')], default='Annually', max_length=15, null=True, verbose_name='Property Price Type'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_rooms',
            field=models.IntegerField(choices=[(1, '1  Room'), (2, '2  Rooms'), (3, '3  Rooms'), (4, '4  Rooms'), (5, '5  Rooms'), (0, 'More than 5 Rooms')], default=1, null=True, verbose_name='Rooms'),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_state',
            field=models.CharField(help_text='eg. Abuja  !!! PS: this should just be the state !!!', max_length=500, null=True, verbose_name='State of properties'),
        ),
        migrations.CreateModel(
            name='PropertyVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('video', models.FileField(help_text='Your video should be 40Seconds Long, 20MB in size max', upload_to=afriproperty.property.models.property_video)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyvideo', to='property.property')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyBlueprint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('type', models.CharField(choices=[('Ground Floor', 'Ground Floor'), ('First Floor', 'First Floor'), ('Second Floor', 'Second Floor'), ('Third Floor', 'Third Floor'), ('Fourth Floor', 'Fourth Floor'), ('Penthouse', 'Penthouse'), ('Garage', 'Garage'), ('Pool House', 'Pool House')], default='First Floor', max_length=50, null=True, verbose_name='Blueprint')),
                ('image', models.FileField(upload_to=afriproperty.property.models.blueprint_image)),
                ('floor_area', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Area Sq/Ft')),
                ('floor_detail', tinymce.models.HTMLField()),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyplan', to='property.property')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
