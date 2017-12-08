from django.conf.urls import url, include
from .api.v1 import auth, timelogs, upload, users, job

urlpatterns = [
    url(r'^auth/login$', auth.LoginView.as_view()),
    url(r'^auth/logout$', auth.LogoutView.as_view()),
    url(r'^auth/register$', auth.RegistrationView.as_view()),
    url(r'^auth/resend-activation$', auth.ResendVerificationView.as_view()),
    # url(r'^auth/login-admin$', auth.AdminLoginView.as_view()),
    url(r'^auth/activate$', auth.ActivationView.as_view()),

    url(r'^jobs$', job.JobList.as_view()),
    url(r'^jobs/(?P<jobId>[-\w]+)/tasks$', job.TaskList.as_view()),
    url(r'^jobs/(?P<jobId>[-\w]+)/freelancers$', job.FreelancersList.as_view()),

    url(r'^timelogs/(?P<jobId>[-\w]+)/(?P<taskId>[-\w]+)/(?P<action>[-\w]+)$', timelogs.NewTimeLog.as_view()),
    url(r'^timelogs/(?P<userId>[-\w]+)$', timelogs.TimeLogsList.as_view()),

    url(r'^uploads/(?P<jobId>[-\w]+)/(?P<taskId>[-\w]+)$', upload.FileUploadView.as_view()),

    url(r'^users$', users.UserListView.as_view()),
    url(r'^users/select-task$', users.SelectTaskView.as_view()),
]
