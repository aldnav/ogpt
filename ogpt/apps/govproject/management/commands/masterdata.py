from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Creates master data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Writing master data..."))
        content_type = ContentType.objects.get_for_model(Site)
        frontend_access, _ = Permission.objects.get_or_create(
            name="Frontend Access",
            codename="frontend_access",
            content_type=content_type,
        )
        staff_user_data = settings.STAFF_USER_DATA
        for user_data in staff_user_data:
            user, _ = User.objects.get_or_create(
                email=user_data[0],
                username=user_data[1],
                first_name=user_data[2],
                last_name=user_data[3],
                is_superuser=True,
                is_staff=True,
            )
            user.set_password(user_data[4])
            user.save()
            user.user_permissions.add(frontend_access)
        self.stdout.write(self.style.SUCCESS("Successfully created master data!"))
