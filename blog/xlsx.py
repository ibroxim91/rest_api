from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_renderer_xlsx.mixins import XLSXFileMixin
from drf_renderer_xlsx.renderers import XLSXRenderer
from .models import *
from .serializers import PostSerializer
from rest_framework import permissions
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from rest_framework.decorators import api_view,permission_classes


@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def generate_pdf( request):
    report = Post.objects.all()
    template_path = 'index.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Report.pdf"'
    html = render_to_string(template_path, {'report': report})
    pisaStatus = pisa.CreatePDF(html, dest=response)

    # save pdf file
    f = open("file.pdf",'w+b')
    pisaStatus2 = pisa.CreatePDF(html, dest=f)
    f.close()
    ###

    return response

# export data to excel for django rest framework
class MyExcelViewSet(XLSXFileMixin,ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = (XLSXRenderer,)
    permission_classes = (permissions.IsAdminUser,)
    filename = 'posts_excel.xlsx'

    column_header = {
        'titles': [
            "ID",
            "TITLE",
            "SLUG",
            "STATUS"
        ],
        'column_width': [10, 30, 17,10],
        'height': 25,
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': True,
                'color': 'FF000000',
            },
        },
    }
    body = {
        'style': {
            'fill': {
                'fill_type': 'solid',
                'start_color': 'FFCCFFCC',
            },
            'alignment': {
                'horizontal': 'center',
                'vertical': 'center',
                'wrapText': True,
                'shrink_to_fit': True,
            },
            'border_side': {
                'border_style': 'thin',
                'color': 'FF000000',
            },
            'font': {
                'name': 'Arial',
                'size': 14,
                'bold': False,
                'color': 'FF000000',
            }
        },
        'height': 40,
    }

