from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('kind', models.IntegerField(choices=[(0, 'fundacja'), (1, 'organizacja pozarządowa'), (2, 'zbiórka lokalna')], default=0)),
                ('categories', models.ManyToManyField(to='charitydonation_app.Category')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('address', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Numer telefonu jest nieprawidłowy.', regex='(^|\\W)(\\(?(\\+|00)?48\\)?)?[ -]?\\d{3}[ -]?\\d{3}[ -]?\\d{3}(?!\\w)')])),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('[0-9]{2}\\-[0-9]{3}', message='Kod pocztowy jest nieprawidłowy.')])),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField(blank=True)),
                ('is_taken', models.BooleanField(default=False)),
                ('taken_date', models.DateField(blank=True, null=True)),
                ('categories', models.ManyToManyField(to='charitydonation_app.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charitydonation_app.Institution')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
