from rest_framework.serializers import ModelSerializer, SerializerMethodField
from selection.models import SectionSchedule, SubjectSection, Weekday
from selection.serializers import (
    ScheduleSerializer,
    SelectionSerializer,
    SubjectSerializer,
)


class SubjectSectionSerializer(ModelSerializer):
    subject_code = SerializerMethodField()
    subject_name = SerializerMethodField()
    selection = SerializerMethodField()
    subject_schedule = ScheduleSerializer(many=True, required=False)

    class Meta:
        model = SubjectSection
        fields = [
            "id",
            "selection",
            "section",
            "subject",
            "subject_code",
            "subject_name",
            "professor",
            "taken",
            "subject_schedule",
        ]
        extra_kwargs = {
            "subject": {
                "write_only": True,
            }
        }
        read_only_fields = ["id"]

    def create(self, validated_data):
        schedules = validated_data.pop("subject_schedule", [])

        # subject_id = validated_data["subject"]
        # print("DATA")
        # print (validated_data)

        # subject = Subject.objects.get(id=subject_id)

        # validated_data["subject"] = subject.id
        subject_section = SubjectSection.objects.create(**validated_data)

        for schedule in schedules:
            weekday = Weekday.objects.get(id=schedule["weekday"].id)
            schedule["weekday"] = weekday
            schedule["section"] = subject_section
            SectionSchedule.objects.create(**schedule)

        return subject_section

    def update(self, instance, validated_data):
        schedules = validated_data.pop("subject_schedule", [])

        # if "subject" in validated_data:
        #     subject_id = validated_data["subject"]
        #     subject = Subject.objects.get(id=subject_id)
        #     validated_data["subject"] = subject
        return super().update(instance, validated_data)

    def get_selection(self, obj) -> str:
        selection = obj.selection
        serializer = SelectionSerializer(selection, many=False)
        data = serializer.data
        selection = data["name"]
        return selection

    def get_subject_code(self, obj) -> str:
        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_code = data["code"]
        return subject_code

    def get_subject_name(self, obj) -> str:
        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_name = data["name"]
        return subject_name

    # def get_subject_schedule(self, obj) -> str:
    #

    #     schedule = obj.schedule
    #     serializer = ScheduleSerializer(schedule, many=True)
    #     data = serializer.data
    #     print(data)
    #     return data
