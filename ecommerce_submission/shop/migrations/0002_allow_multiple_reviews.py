from django.db import migrations


class Migration(migrations.Migration):
    """Allow buyers to submit reviews for the same product over time."""

    dependencies = [('shop', '0001_initial')]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='one_review_per_buyer_product',
        ),
    ]
