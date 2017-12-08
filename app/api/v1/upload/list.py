
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..utils import *
from app.models import TimeLogs
from app.serializers import TimeLogMediaSerializer
import os, uuid, pprint, datetime
from django.conf import settings
from django.core.files.base import ContentFile

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
UPLOAD_DIR = rreplace(SITE_ROOT, '/app/api/v1/upload', settings.STATIC_URL + 'uploads', 1)

class FileUploadView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    # def dispatch(self, request, *args, **kwargs):
    #     p = request.POST  # Force evaluation of the Django request
    #     return super(APIView, self).dispatch(request, *args, **kwargs)

    def getTimeLog(self, _timeLogId):
        try:
            return TimeLogs.objects.get(id=_timeLogId)
        except TimeLogs.DoesNotExist:
            return None

    def allowed_image_file(self, filename):
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    def post(self, request, jobId, taskId): #, *args, **kwargs):
        timelog = self.getTimeLog(request.POST['timelog'])

        if not timelog:
            return errorResponse('Time log does not exist.')
        elif not isJobAssigned(request.user.id, jobId):
            return errorResponse('Job not accessible.')
        else:
            file = request.FILES['file']
            if file and self.allowed_image_file(file.name):
                filename = file.name
                name, ext = os.path.splitext(filename)
                filename = str(uuid.uuid4()) + ext

                full_filename = os.path.join(UPLOAD_DIR, filename)

                fout = open(full_filename, 'wb+')

                file_content = ContentFile( request.FILES['file'].read() )

                try:
                    for chunk in file_content.chunks():
                        fout.write(chunk)
                    fout.close()

                    data = {
                        "image": settings.SERVER_HOST + settings.STATIC_URL + 'uploads/' + filename,
                        "timelog": request.POST['timelog']
                    }

                    serializer = TimeLogMediaSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()

                    timelog.end_date = datetime.datetime.now()
                    timelog.save()

                    result = {
                        'success': True
                    }
                except:
                    result = {
                        'success': False
                    }
            else:
                result = {
                    'success': False,
                    'message': 'Invalid file'
                }

            return JsonResponse(result, safe=False)
