from django.urls import reverse
from django.views import generic
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .tasks import test
from .models import DataSchema, Dataset
from .forms import ColumnFormset, DatasetForm


class HomeView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = 'home.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        return DataSchema.objects.\
            filter(created_by=self.request.user).\
            order_by('-created_at')


class SchemaView(LoginRequiredMixin, generic.FormView, generic.DetailView):
    template_name = 'schema.html'

    model = DataSchema
    queryset = DataSchema.objects.prefetch_related('schemacolumn_set').order_by('schemacolumn__order')

    form_class = DatasetForm

    def get_object(self, queryset=None):
        obj = super(SchemaView, self).get_object(queryset=queryset)
        if obj.created_by != self.request.user:
            raise Http404()
        return obj

    def get_success_url(self):
        return reverse('datasets')

    def get_context_data(self, **kwargs):
        context = super(SchemaView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.data_schema = self.object
        form.instance.created_by = self.request.user
        form.save()
        test.delay(form.instance.id)
        return super(SchemaView, self).form_valid(form)


class SchemaCreateView(LoginRequiredMixin, generic.CreateView):
    model = DataSchema
    template_name = 'create.html'
    fields = ['name']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["columns"] = ColumnFormset(self.request.POST)
        else:
            data["columns"] = ColumnFormset()
        return data

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        context = self.get_context_data()
        columns = context["columns"]

        if columns.is_valid():
            self.object = form.save()
            columns.instance = self.object
            columns.save()
        else:
            form.add_error(None, columns.errors)
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')


class DatasetView(LoginRequiredMixin, generic.ListView):
    template_name = 'datasets.html'
    context_object_name = 'datasets'

    def get_queryset(self):
        return Dataset.objects.\
            select_related('data_schema').\
            filter(created_by=self.request.user).\
            order_by('-created_at')


@login_required()
def download(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)

    if dataset.created_by != request.user:
        raise Http404('File not found')

    return redirect(dataset.file.url)
