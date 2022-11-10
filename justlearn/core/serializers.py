from rest_framework import serializers

from .models import Advertisement, Exercise, Lesson, Problem, Skill, Student, Teacher


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class AdvertisementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = '__all__'


class TeacherProfilePicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}



class ExerciseSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = Exercise
        fields = ['id','lesson','file','timestamp']
        read_only_fields = ('id','timestamp')

class LessonSerializer(serializers.ModelSerializer):
    exercise_set = ExerciseSerializer(many=True, read_only = True)
    class Meta:
        model = Lesson
        fields = ['id','student','teacher','duration','date','meeting_link','topic','description','exercise_set']