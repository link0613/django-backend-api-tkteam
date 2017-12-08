import pprint, os, uuid
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from . import utils
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.clickjacking import xframe_options_exempt

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
UPLOAD_DIR = utils.rreplace(SITE_ROOT, '/app', settings.STATIC_URL + 'uploads', 1)

def custom404(request):
    return JsonResponse(data={
        'success': False,
        'message': 'The resource was not found'
    }, status=404)

def index(request):
    return HttpResponse('Teleport API')

def allowed_image_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['pdf', 'doc', 'docx'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def is_valid_file(type, filename):
    if type == 'file':
        return allowed_file(filename)
    if type == 'image':
        return allowed_image_file(filename)


@csrf_exempt
def upload(request, userProjectId):
    import pprint
    pprint.pprint(userProjectId)
    pprint.pprint(request.POST)
    pprint.pprint(request.FILES)

    result = {
        "success" : True
    }


    # file = request.FILES['file']

    # if file and is_valid_file(type, file.name):
    #     filename = file.name
    #     name, ext = os.path.splitext(filename)
    #     filename = str(uuid.uuid4()) + ext
    #
    #     full_filename = os.path.join(UPLOAD_DIR, loc, filename)
    #
    #     fout = open(full_filename, 'wb+')
    #
    #     file_content = ContentFile( request.FILES['file'].read() )
    #
    #     try:
    #         for chunk in file_content.chunks():
    #             fout.write(chunk)
    #         fout.close()
    #
    #         result = {
    #             'success': True,
    #             'url': settings.STATIC_URL + 'uploads/' + loc + '/' + filename,
    #             'filename': filename
    #         }
    #     except:
    #         result = {
    #             'success': False
    #         }
    # else:
    #     result = {
    #         'success': False,
    #         'message': 'Invalid file'
    #     }

    return JsonResponse(result, safe=False)
