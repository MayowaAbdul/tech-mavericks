# Generated by Django 5.1.2 on 2024-11-20 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundraising', '0015_withdrawal_account_name_alter_withdrawal_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='campaign_purpose',
            field=models.CharField(choices=[('Child Education', 'child education'), ('Child Healthcare', 'child healthcare')], default='Child Education', max_length=50),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]
