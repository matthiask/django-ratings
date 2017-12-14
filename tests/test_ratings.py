import random

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from djangoratings.exceptions import IPLimitReached
from djangoratings.models import Vote

from tests.models import RatingTestModel

settings.RATINGS_VOTES_PER_IP = 1


class RatingTestCase(TestCase):
    def testRatings(self):
        instance = RatingTestModel.objects.create()

        # Test adding votes
        instance.rating.add(score=1, user=None, ip_address='127.0.0.1')
        self.assertEquals(instance.rating.score, 1)
        self.assertEquals(instance.rating.votes, 1)

        # Test adding votes
        instance.rating.add(score=2, user=None, ip_address='127.0.0.2')
        self.assertEquals(instance.rating.score, 3)
        self.assertEquals(instance.rating.votes, 2)

        # Test changing of votes
        instance.rating.add(score=2, user=None, ip_address='127.0.0.1')
        self.assertEquals(instance.rating.score, 4)
        self.assertEquals(instance.rating.votes, 2)

        # Test users
        user = User.objects.create(username=str(random.randint(0, 100000000)))
        user2 = User.objects.create(username=str(random.randint(0, 100000000)))

        instance.rating.add(score=2, user=user, ip_address='127.0.0.3')
        self.assertEquals(instance.rating.score, 6)
        self.assertEquals(instance.rating.votes, 3)

        instance.rating2.add(score=2, user=user, ip_address='127.0.0.3')
        self.assertEquals(instance.rating2.score, 2)
        self.assertEquals(instance.rating2.votes, 1)

        self.assertRaises(IPLimitReached, instance.rating2.add, score=2, user=user2, ip_address='127.0.0.3')

        # Test deletion hooks
        Vote.objects.filter(ip_address='127.0.0.3').delete()

        instance = RatingTestModel.objects.get(pk=instance.pk)
        instance._update()

        self.assertEquals(instance.rating.score, 4)
        self.assertEquals(instance.rating.votes, 2)
        self.assertEquals(instance.rating2.score, 0)
        self.assertEquals(instance.rating2.votes, 0)
