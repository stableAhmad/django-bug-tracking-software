# Generated by Django 4.0.5 on 2022-10-12 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_project_name'),
        ('report', '0018_alter_report_belongs_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='belongs_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]
