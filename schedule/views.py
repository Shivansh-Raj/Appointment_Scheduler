from django.shortcuts import render
from .serializers import userSerializer, appointmentSerializer, availabilitySerializer
from rest_framework import generics, status
from rest_framework.views import APIView, Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, Appointment, Availability
from django.contrib.auth import authenticate
# Create your views here.

class createUser(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = userSerializer
    permission_classes = [AllowAny]

class getUser(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            # The authenticated user's info is available in `request.user`
            user = request.user
            # Serialize user data
            serializer = userSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class getAllProfessorsInfo(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        professors = CustomUser.objects.filter(is_Professor=True)
        if professors:
            serializer = userSerializer(professors, many = True)
            response_data = [
                {
                    "Professor Name": professor['username'],
                    "Professor's Id": professor['id']
                }
                for professor in serializer.data
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        return Response("There is no Professor at the moment!!", status=status.HTTP_404_NOT_FOUND)


class scheduleAppointment(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = request.user.id
        professor = request.data.get('profId')
        student_user = CustomUser.objects.get(id=student)
        professor_user = CustomUser.objects.get(id=professor)

        if not student_user.is_Student:
            return Response({"error": "Selected user is not a student."}, status=status.HTTP_400_BAD_REQUEST)
        if not professor_user.is_Professor:
            return Response({"error": "Selected user is not a professor."}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data['student'] = request.user.username
        data['stuId'] = request.user.id
        serializer = appointmentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'data':data,
            'errors':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            appointment_id = request.data['appointment_id']
            if request.user.is_Professor:
                try:
                    appointment = Appointment.objects.get(id=appointment_id)
                    if (appointment.professor.id != request.user.id):
                        raise Response("You are not authorized to cancel this appointment.", status=status.HTTP_403_FORBIDDEN)
                except Appointment.DoesNotExist:
                    return Response("Appointment not found.", status=status.HTTP_404_NOT_FOUND)
                try:
                    availability = Availability.objects.get(id=appointment.availability.id)
                except Availability.DoesNotExist:
                    return Response("Availability slot not found.", status=status.HTTP_404_NOT_FOUND)
                appointment.status = 'Cancelled'
                availability.isBooked = False
                appointment.save()
                availability.save()
                return Response("Successfully cancelled the appointment", status=status.HTTP_202_ACCEPTED)
            else:
                return Response("You can't reschedule or delete an appointement!!")
        except KeyError:
            return Response("Missing appointment_id in the request.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class specifyTimeSlot(APIView):
    def get(self, request, prof_id):
        try: 
            Prof = CustomUser.objects.get(id = prof_id)
            if not Prof.is_Professor:
                raise ValueError("The provided user is not a professor.")
            slots = Availability.objects.filter(Professor_id=prof_id, isBooked=False)
            serializer = availabilitySerializer(slots, many = True)
            if slots:
                return Response(serializer.data)
            return Response("The professor has no Free Slot at the moment!!")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # "The provided user is not a professor."


    def post(self, request):
        data = request.data 
        if request.user.is_Student:
            return Response({
                'errors':"You don't have this right!!"
            }, status=status.HTTP_400_BAD_REQUEST)
        data['profId'] = request.user.id 
        data['Professor_Name'] = request.user.username
        serializer = availabilitySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({
            'data':data,
            'errors':serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        

class checkAppointments(APIView):
    def get(self, request):
        user = request.user
        try:
            appointments = Appointment.objects.filter(student= user, status = 'Booked')
            if (user.is_Professor):
                appointments = Appointment.objects.filter(professor= user, status = 'Booked')
            if appointments.exists():
                serializer = appointmentSerializer(appointments, many = True)
                # if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("You have no pending appointments", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)