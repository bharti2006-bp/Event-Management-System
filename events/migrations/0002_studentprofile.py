from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=30, unique=True)),
                ('semester', models.CharField(choices=[('1', 'Semester 1'), ('2', 'Semester 2'), ('3', 'Semester 3'), ('4', 'Semester 4'), ('5', 'Semester 5'), ('6', 'Semester 6'), ('7', 'Semester 7'), ('8', 'Semester 8')], max_length=2)),
                ('year', models.CharField(choices=[('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'), ('4', '4th Year'), ('5', '5th Year')], max_length=1)),
                ('branch', models.CharField(choices=[('CSE', 'Computer Science & Engineering'), ('IT', 'Information Technology'), ('ECE', 'Electronics & Communication Engineering'), ('EE', 'Electrical Engineering'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('CH', 'Chemical Engineering'), ('BT', 'Biotechnology'), ('MBA', 'Master of Business Administration'), ('MCA', 'Master of Computer Applications'), ('OTHER', 'Other')], max_length=10)),
                ('course', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student Profile',
                'verbose_name_plural': 'Student Profiles',
            },
        ),
    ]
