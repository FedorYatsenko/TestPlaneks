import os

from celery import shared_task
from django.core.files import File

from .models import Dataset, SchemaColumn
from .generator import CsvGenerator


@shared_task
def test(dataset_id: int):
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.status = Dataset.PROCESSING
    dataset.save()

    generator = CsvGenerator(columns=SchemaColumn.objects.filter(data_schema_id=dataset.data_schema_id).all())
    path = generator.generate(dataset)

    with open(path, 'rb') as f:
        file = File(f, name=os.path.basename(path))
        dataset.file = file

    dataset.status = Dataset.READY
    dataset.save()
