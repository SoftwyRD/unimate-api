"""Selection Serializers"""

from core.models import (
    SubjectSection,
    Subject,
    Selection as SelectionModel,
    SectionSchedule as ScheduleModel,
    Weekday as WeekdayModel,
)
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ListSerializer,
)



class ScheduleSerializer(ModelSerializer):
    """Serializer for Schedule"""

    class Meta:
        model = ScheduleModel
        # fields = "__all__"
        exclude = ("section","id")
        # read_only_fields = ["id"]

    def create(self, validated_data):
        section = self.context.get('section')
        instance, created = ScheduleModel.objects.update_or_create(section=section, defaults=validated_data)
        return instance


class ScheduleListSerializer(ListSerializer):
    """Serializer for Schedule"""
    child = ScheduleSerializer()

    class Meta:
        model = ScheduleModel
        fields = "__all__"
        read_only_fields = ["id"]



class SelectionSerializer(ModelSerializer):
    """Serializer for Selection"""

    class Meta:
        model = SelectionModel
        fields = "__all__"
        read_only_fields = ["id", "created_on", "user"]


class SubjectSerializer(ModelSerializer):
    """Serializer for Subject"""

    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = ["id"]


class SubjectSectionSerializer(ModelSerializer):
    """Serializer for SubjectSection"""

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

    def run_validation(self, data):
        """Validate the data before saving it"""

        super().run_validation(data)
        return data

    def create(self, validated_data):
        """Create the subject section"""
        schedules = validated_data.pop("subject_schedule", [])

        subject_id = validated_data["subject"]
        subject = Subject.objects.get(id=subject_id)

        validated_data["subject"] = subject
        subject_section = SubjectSection.objects.create(**validated_data)

        for schedule in schedules:
            weekday = WeekdayModel.objects.get(id=schedule["weekday"])
            schedule["weekday"] = weekday
            schedule["section"] = subject_section
            ScheduleModel.objects.create(**schedule)

        return subject_section

    def update(self, instance, validated_data):
        """Update de subject section"""
        schedules = validated_data.pop('subject_schedule', [])

        if "subject" in validated_data:
            subject_id = validated_data["subject"]
            subject = Subject.objects.get(id=subject_id)
            validated_data["subject"] = subject

        return super().update(instance, validated_data)

    def get_selection(self, obj) -> str:
        """Get the selection name"""

        selection = obj.selection
        serializer = SelectionSerializer(selection, many=False)
        data = serializer.data
        selection = data["name"]
        return selection

    def get_subject_code(self, obj) -> str:
        """Get the subject code"""

        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_code = data["code"]
        return subject_code

    def get_subject_name(self, obj) -> str:
        """Get the subject name"""

        subject = obj.subject
        serializer = SubjectSerializer(subject, many=False)
        data = serializer.data
        subject_name = data["name"]
        return subject_name

    # def get_subject_schedule(self, obj) -> str:
    #     """Get the subject schedule"""

    #     schedule = obj.schedule
    #     serializer = ScheduleSerializer(schedule, many=True)
    #     data = serializer.data
    #     print(data)
    #     return data
