from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with a set of data for testing purposes"

    def handle(self, *args, **options):
        self.fill_colleges()
        self.fill_users()
        self.fill_careers()
        self.fill_college_subjects()
        self.fill_sections()
        self.fill_syllabuses()
        self.fill_syllabuses_subjects()
        self.fill_weekdays()

    def fill_careers(self):
        call_command("loaddata", "careers")

    def fill_colleges(self):
        call_command("loaddata", "colleges")

    def fill_college_subjects(self):
        call_command("loaddata", "college_subjects")

    def fill_sections(self):
        call_command("loaddata", "sections")

    def fill_syllabuses(self):
        call_command("loaddata", "syllabuses")

    def fill_syllabuses_subjects(self):
        call_command("loaddata", "syllabuses_subjects")

    def fill_users(self):
        call_command("loaddata", "users")

    def fill_weekdays(self):
        call_command("loaddata", "weekdays")
