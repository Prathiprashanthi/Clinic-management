# Generated by Django 3.2.25 on 2024-05-02 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Last_login',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Login_Time', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'last_login',
            },
        ),
        migrations.CreateModel(
            name='PatientModel',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('patient_name', models.CharField(max_length=100)),
                ('patient_dob', models.DateField(max_length=20, null=True)),
                ('patient_age', models.IntegerField(null=True)),
                ('patient_email', models.EmailField(max_length=100)),
                ('patient_password', models.CharField(max_length=100)),
                ('patient_contact', models.CharField(max_length=15)),
                ('patient_city', models.TextField(null=True)),
                ('patient_image', models.ImageField(upload_to='user/images')),
                ('patient_status', models.CharField(default='pending', help_text='user_status', max_length=50, null=True)),
                ('Last_Login_Time', models.TimeField(auto_now_add=True, null=True)),
                ('Last_Login_Date', models.DateField(auto_now_add=True, null=True)),
                ('No_Of_Times_Login', models.IntegerField(default=0, null=True)),
                ('Message', models.TextField(max_length=250, null=True)),
            ],
            options={
                'db_table': 'patient_details',
            },
        ),
    ]
