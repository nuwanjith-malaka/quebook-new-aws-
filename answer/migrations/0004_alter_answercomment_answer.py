# Generated by Django 4.0 on 2022-03-02 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('answer', '0003_alter_answer_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercomment',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='answer.answer'),
        ),
    ]
