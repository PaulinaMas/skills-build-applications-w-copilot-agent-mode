from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from octofit_tracker.models import Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete existing data in correct order to avoid FK issues
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        for user in User.objects.all():
            if getattr(user, 'id', None):
                user.delete()
        for team in Team.objects.all():
            if getattr(team, 'id', None):
                team.delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users (Superheroes)
        users = [
            User.objects.create_user(username='ironman', email='ironman@marvel.com', team=marvel),
            User.objects.create_user(username='captainamerica', email='cap@marvel.com', team=marvel),
            User.objects.create_user(username='batman', email='batman@dc.com', team=dc),
            User.objects.create_user(username='superman', email='superman@dc.com', team=dc),
        ]

        # Create Activities
        for user in users:
            Activity.objects.create(user=user, type='run', duration=30, distance=5)
            Activity.objects.create(user=user, type='cycle', duration=60, distance=20)

        # Create Workouts
        Workout.objects.create(name='Morning Cardio', description='30 min run + 20 min cycle')
        Workout.objects.create(name='Strength Training', description='Pushups, Pullups, Squats')

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
