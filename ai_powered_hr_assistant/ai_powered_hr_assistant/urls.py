# from django.contrib import admin
# from django.urls import path, re_path
# from .views import create_admin, post_job_ad, dashboard, register, user_login, user_logout, get_all_jobs, apply_job, upload_cv
# #  get_all_applicants, recognize_employees_bulk, create_applicants,

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('create-admin/', create_admin, name='create_admin'),
#     # path('create-applicants/', create_applicants, name='create_applicants'),
#     # path('create-job/', create_job, name='create_job'),
#     # path('get-applicants/', get_all_applicants, name='get_all_applicants'),
#     path('get-jobs/', get_all_jobs, name='get_all_jobs'),
#     # path('recognize-employee/', recognize_employees_bulk, name='recognize_employee'),
#     path('register/', register, name='register'),
#     path('login/', user_login, name='login'),
#     path('logout/', user_logout, name='logout'),
#     path('post-job/', post_job_ad, name='post_job'),
#     path('upload-cv/', upload_cv, name='upload_cv'),
#     path('dashboard/',dashboard, name='dashboard'),
#     re_path(r'^apply-job/(?P<job_id>[a-f0-9]{24})/$', apply_job, name='apply_job'), # Update to handle ObjectId
# ]



from django.urls import path
from .views import create_admin, register, user_login, user_logout, upload_cv, JobAdListCreate, JobAdDetail, apply_job, get_all_job_applications

urlpatterns = [
    path('create-admin/', create_admin, name='create_admin'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('upload-cv/', upload_cv, name='upload_cv'),
    path('jobs/', JobAdListCreate.as_view(), name='job_list_create'),
    path('jobs/<int:pk>/', JobAdDetail.as_view(), name='job_detail'),
    path('apply-job/<int:job_id>/', apply_job, name='apply_job'),
    path('job-applications/', get_all_job_applications, name='get_all_job_applications')
]