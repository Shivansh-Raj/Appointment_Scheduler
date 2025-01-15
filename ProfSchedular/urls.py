
from django.contrib import admin
from django.urls import path, include
from schedule.views import createUser, getUser, getAllProfessorsInfo, scheduleAppointment, specifyTimeSlot, checkAppointments
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token', TokenObtainPairView.as_view(), name = "access token"),
    path('api/token/refresh', TokenRefreshView.as_view(), name = "refresh token"),
    path('api/user/register', createUser.as_view(), name = 'create user'),
    path('api/user/fetchInfo', getUser.as_view(), name = 'get user info'),
    path('api/getAllProfessors', getAllProfessorsInfo.as_view(), name = 'get user info'),
    path('api/schedule', scheduleAppointment.as_view(), name = 'schedule appointment'),
    path('api/schedule/cancel', scheduleAppointment.as_view(), name = 'schedule appointment'),
    path('api/specifySlot', specifyTimeSlot.as_view(), name = 'schedule appointment'),
    path('api/checkFreeSlots/<int:prof_id>', specifyTimeSlot.as_view(), name = 'schedule appointment'),
    path('api/allAppointments', checkAppointments.as_view(), name = 'schedule appointment'),
    # path('api/', include('schedule.urls'))
]
