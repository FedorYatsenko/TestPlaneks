import os

from django.db import models
from django.conf import settings


class DataSchema(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.id}, {self.name}, {self.created_at})"


class SchemaColumn(models.Model):
    class Meta:
        db_table = 'SchemaColumn'
        constraints = [
            models.UniqueConstraint(fields=['data_schema', 'name'], name='unique column in data_schema')
        ]
    FULL_NAME = 'FN'
    JOB = 'JB'
    EMAIL = 'EM'
    PHONE_NUMBER = 'PM'
    DATE = 'DT'
    DATA_TYPES_CHOICES = [
        (FULL_NAME, 'Full name'),
        (JOB, 'Job'),
        (EMAIL, 'Email'),
        (PHONE_NUMBER, 'Phone number'),
        (DATE, 'Date'),
    ]

    id = models.AutoField(primary_key=True)
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)

    name = models.CharField(max_length=256)
    order = models.IntegerField()
    data_type = models.CharField(max_length=2, choices=DATA_TYPES_CHOICES, default=FULL_NAME)

    unique_together = ['data_schema', 'name']


class Dataset(models.Model):
    DIRECTORY = os.path.join(settings.MEDIA_ROOT, 'datasets')

    NEW = 'N'
    PROCESSING = 'P'
    READY = 'R'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (READY, 'Ready'),
    ]

    SEMICOLON = ';'
    COMMA = ','
    BAR = ','
    COLON = ':'
    TAB = '\t'
    SPACE = ' '

    DELIMITER_CHOICES = [
        (SEMICOLON, 'Semicolon (;)'),
        (COMMA, 'Comma (,)'),
        (BAR, 'Bar (|)'),
        (COLON, 'Colon (:)'),
        (TAB, 'Tab (\\t)'),
        (SPACE, 'Space ( )'),
    ]

    QUOTE = "'"
    DOUBLE_QUOTES = '"'

    QUOTE_CHOICES = [
        (QUOTE, 'Quote (\')'),
        (DOUBLE_QUOTES, 'Double quotes (")'),
    ]

    id = models.AutoField(primary_key=True)
    data_schema = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NEW)

    count = models.IntegerField(default=100)
    delimiter = models.CharField(max_length=1, choices=DELIMITER_CHOICES, default=SEMICOLON)
    quote_char = models.CharField(max_length=1, choices=QUOTE_CHOICES, default=DOUBLE_QUOTES)

    file = models.FilePathField(path=DIRECTORY, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def is_ready(self):
        return self.status == self.READY
