# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-06 14:47
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import papers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='last name')),
                ('street_line_1', models.CharField(max_length=30, verbose_name='street_line_1')),
                ('street_line_2', models.CharField(max_length=30, verbose_name='street_line_2')),
                ('city', models.CharField(max_length=30, verbose_name='city')),
                ('state', models.CharField(max_length=30, verbose_name='state')),
                ('zip_code', models.IntegerField()),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='phone number')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('user_type', models.IntegerField(choices=[(0, 'Author'), (1, 'PCM'), (2, 'PCC'), (3, 'Admin')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=papers.models.concat_media_path)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('abstract', models.TextField(blank=True, max_length=1000, null=True, verbose_name='abstract')),
                ('submission_date', models.DateTimeField(editable=False)),
                ('version', models.IntegerField(default=1)),
                ('rate', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
            ],
        ),
        migrations.CreateModel(
            name='PaperAssigned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Paper')),
            ],
        ),
        migrations.CreateModel(
            name='PaperAuthors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Paper')),
            ],
        ),
        migrations.CreateModel(
            name='PaperRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Paper', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=2000, verbose_name='comment')),
                ('rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Paper')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('papers.customuser',),
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('papers.customuser',),
        ),
        migrations.CreateModel(
            name='PCC',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('papers.customuser',),
        ),
        migrations.AddField(
            model_name='reviews',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='reviewer'),
        ),
        migrations.AddField(
            model_name='paperrequests',
            name='pcm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='PCM',
            fields=[
                ('author_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='papers.Author')),
            ],
            options={
                'abstract': False,
            },
            bases=('papers.author',),
        ),
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together=set([('paper', 'reviewer')]),
        ),
        migrations.AlterUniqueTogether(
            name='paperrequests',
            unique_together=set([('paper', 'pcm')]),
        ),
        migrations.AddField(
            model_name='paperauthors',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='papers.Author'),
        ),
        migrations.AddField(
            model_name='paper',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='papers.Author'),
        ),
        migrations.AlterUniqueTogether(
            name='paperauthors',
            unique_together=set([('paper', 'author')]),
        ),
        migrations.AddField(
            model_name='paper',
            name='pcm_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='FirstPCM_Assigned', to='papers.PCM'),
        ),
        migrations.AddField(
            model_name='paper',
            name='pcm_three',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ThirdPCM_Assigned', to='papers.PCM'),
        ),
        migrations.AddField(
            model_name='paper',
            name='pcm_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='SecondPCM_Assigned', to='papers.PCM'),
        ),
        migrations.AlterUniqueTogether(
            name='paper',
            unique_together=set([('title', 'author', 'version')]),
        ),
    ]
