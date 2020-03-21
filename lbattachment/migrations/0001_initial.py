import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import lbattachment.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LBAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attach_file', models.FileField(max_length=255, upload_to=lbattachment.models.upload_attachment_file_path)),
                ('filename', models.CharField(max_length=255)),
                ('suffix', models.CharField(blank=True, default=b'', max_length=8)),
                ('is_img', models.BooleanField(default=False)),
                ('num_downloads', models.IntegerField(default=0)),
                ('description', models.TextField(blank=True, default=b'')),
                ('is_active', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
