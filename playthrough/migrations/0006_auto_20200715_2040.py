# Generated by Django 3.0.4 on 2020-07-15 20:40

from django.db import migrations, models
import django.db.models.deletion
import genki.validators


class Migration(migrations.Migration):

    dependencies = [
        ('playthrough', '0005_auto_20200715_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='completion_role',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='game', to='playthrough.RoleTemplate'),
        ),
        migrations.AlterField(
            model_name='roletemplate',
            name='colour',
            field=models.CharField(help_text="The role's colour in hex.", max_length=6, validators=[genki.validators.hex_validator]),
        ),
    ]
