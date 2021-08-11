from django.contrib import admin

from .models import DataSchema, SchemaColumn

admin.site.register(DataSchema)
admin.site.register(SchemaColumn)
