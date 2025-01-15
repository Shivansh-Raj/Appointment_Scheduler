from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Availability, Appointment


User = get_user_model()

class userSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model= User
        fields = '__all__'
    def create(self, validated_data):
        # print(validated_data)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class availabilitySerializer(serializers.ModelSerializer):
    Professor_Name= serializers.StringRelatedField()
    profId = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_Professor = True), source = 'Professor_id')
    class Meta:
        model = Availability
        fields = ['id','Professor_Name','profId','date','start','end','isBooked']
        extra_kwards = {
            'isBooked': {'read_only':True}
        }
    def create(self, validated_data):
        Professor_id = validated_data.get('prof') 
        date = validated_data.get('date')
        start_time = validated_data.get('start')
        end_time = validated_data.get('end')

        already_added = Availability.objects.filter(Professor_id = Professor_id, date=date)
        for slot in already_added:
            if (
                (start_time >= slot.start and start_time < slot.end) or  
                (end_time > slot.start and end_time <= slot.end) or      
                (start_time <= slot.start and end_time >= slot.end)      
            ):
                raise serializers.ValidationError("Slots are overlapping!!!")
        add_slot = Availability(**validated_data)
        add_slot.save()
        return add_slot
    


class appointmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    stuId = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_Student = True), source = 'student')
    professor = serializers.StringRelatedField()
    profId = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_Professor = True), source = 'professor')

    class Meta:
        model = Appointment
        fields = [
            'id', 'student', 'stuId', 'professor', 'profId',
            'availability', 'availability_id', 'status', 'created_at'
        ]

    def create(self, validated_data):
        availabilityData = validated_data.get('availability')
        if availabilityData and availabilityData.isBooked:
            raise serializers.ValidationError("This slot is already BOOKED!!")
        if availabilityData:
            availabilityData.isBooked = True
            availabilityData.save()

        appointment = super().create(validated_data)
        return appointment

    def update(self, instance, validated_data):
        availabilityData = validated_data.get('availability')
        if availabilityData and availabilityData.isBooked:
            raise serializers.ValidationError("This slot is already BOOKED!!")
        if availabilityData:
            availabilityData.isBooked = True
            availabilityData.save()

        appointment = super().update(instance, validated_data)
        return appointment
    
    
        
