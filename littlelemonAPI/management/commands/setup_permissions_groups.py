from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'My custom command description'

    def handle(self, *args, **options):
        # Create groups
        manager_group, created = Group.objects.get_or_create(name='Manager')
        delivery_crew_group, created = Group.objects.get_or_create(name='Delivery_crew')

        # Create superusers and add to Manager group
        superuser1 = User.objects.create_superuser(username='VIDHU', password='VIDHU$12')
        superuser1.groups.add(manager_group)
        superuser1.save()

        superuser2 = User.objects.create_superuser(username='ADMIN', password='ADMIN$12')
        superuser2.groups.add(manager_group)
        superuser2.save()

        print('Groups and superusers created successfully')

        # Create delivery crew users and add to Delivery_crew group
        delivery_crew_usernames = ['SAM', 'PRANEETH', 'DHAR', 'CHAMMU', 'RAM']
        for username in delivery_crew_usernames:
            user = User.objects.create_user(username=username, password=f'{username}$12')
            user.groups.add(delivery_crew_group)
            user.save()

        print('Delivery Crew created successfully')
