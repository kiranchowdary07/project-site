# Generated by Django 2.1.3 on 2019-02-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

   

    dependencies = [
       ('mysite', '0018_ppic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_limit', models.IntegerField()),
                ('c_limit', models.IntegerField()),
                ('l_limit', models.IntegerField()),
            ],
        ),
    ]
