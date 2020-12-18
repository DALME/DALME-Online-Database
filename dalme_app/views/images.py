from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from dalme_app.models import rs_resource, rs_collection_resource, rs_resource_data, rs_user
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ._common import DALMEListView, DALMEDetailView


@method_decorator(login_required, name='dispatch')
class ImageList(DALMEListView):
    page_title = 'DAM Images'
    dt_config = 'images'
    breadcrumb = [('Sources', ''), ('DAM Images', '/images')]


@method_decorator(login_required, name='dispatch')
class ImageDetail(DALMEDetailView):
    model = rs_resource
    template_name = 'dalme_app/image_detail.html'
    breadcrumb = [('Sources', ''), ('DAM Images', '/images')]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tables = []
        image_data = {
            'DAM Id': self.object.ref,
            'Created': timezone.localtime(self.object.creation_date).strftime('%d-%b-%Y@%H:%M'),
            'Creator': rs_user.objects.get(ref=self.object.created_by).fullname if rs_user.objects.filter(ref=self.object.created_by).exists() else self.object.created_by,
            'Record modified': timezone.localtime(self.object.modified).strftime('%d-%b-%Y@%H:%M'),
            'File modified': timezone.localtime(self.object.file_modified).strftime('%d-%b-%Y@%H:%M'),
            'Filesize': self.object.file_size,
            'Image?': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.has_image else '<i class="fa fa-times-circle dt_checkbox_false"></i>'
        }

        context.update({
            'image_data': image_data,
            'image_url': self.object.get_image_url('scr'),
        })

        if rs_resource_data.objects.filter(resource=self.object.ref).order_by('resource_type_field').exists():
            attribute_data = []
            attributes = rs_resource_data.objects.filter(resource=self.object.ref).order_by('resource_type_field')
            for a in attributes:
                value = a.value
                name = a.resource_type_field.name
                label = a.resource_type_field.title
                d = {
                    'name': name,
                    'label': label,
                    'value': value,
                }
                attribute_data.append(d)
            context['attribute_data'] = attribute_data

        if rs_collection_resource.objects.filter(resource=self.object.ref).exists():
            collections = []
            col_list = rs_collection_resource.objects.filter(resource=self.object.ref)
            for col in col_list:
                path = ''
                if col.collection.theme:
                    path += col.collection.theme
                    if col.collection.theme2:
                        path += ' ≫ '+col.collection.theme2
                        if col.collection.theme3:
                            path += ' ≫ '+col.collection.theme3
                d = {
                    'id': col.collection.ref,
                    'name': col.collection.name,
                    'creator': rs_user.objects.get(ref=col.collection.user).fullname if rs_user.objects.filter(ref=col.collection.user).exists() else col.collection.user,
                    'path': path
                }
                collections.append(d)
            context['collections'] = collections
            tables.append(['collections', 'fa-th-large', 'Collections'])

        if tables != []:
            context.update({
                'tables': tables,
                'table_options': {
                    'responsive': 'true',
                    'dom': '''"<'sub-card-header d-flex'<'card-header-title'>fr><'card-body't>"''',
                    'stateSave': 'true',
                    'select': {'style': 'single'},
                    'scrollY': 150,
                    'deferRender': 'true',
                    'scroller': 'true',
                    'language': {
                        'searchPlaceholder': 'Search',
                        'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                        },
                    }
            })

        return context

    def get_page_title(self):
        return 'DAM Image: {}'.format(str(self.object.ref))

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404
