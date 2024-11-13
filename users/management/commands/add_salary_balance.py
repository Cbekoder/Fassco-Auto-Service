from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import Employee

class Command(BaseCommand):
    help = 'Add salary amount to balance for employees with position "other" on the 1st of the month'

    def handle(self, *args, **options):
        current_date = timezone.now().date()
        if current_date.day == 1:
            employees = Employee.objects.filter(position="other")
            for employee in employees:
                employee.balance += employee.salary
                employee.save()
            self.stdout.write(self.style.SUCCESS("Successfully added salary to balance for 'other' employees"))
