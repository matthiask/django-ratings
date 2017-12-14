import random

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from djangoratings.exceptions import IPLimitReached
from djangoratings.models import Vote, SimilarUser, IgnoredObject

from tests.models import RatingTestModel

settings.RATINGS_VOTES_PER_IP = 1


class RecommendationsTestCase(TestCase):
    def setUp(self):
        self.instance = RatingTestModel.objects.create()
        self.instance2 = RatingTestModel.objects.create()
        self.instance3 = RatingTestModel.objects.create()
        self.instance4 = RatingTestModel.objects.create()
        self.instance5 = RatingTestModel.objects.create()

        # Test users
        self.user = User.objects.create(username=str(random.randint(0, 100000000)))
        self.user2 = User.objects.create(username=str(random.randint(0, 100000000)))

    def testExclusions(self):
        Vote.objects.all().delete()

        self.instance.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance2.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance3.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance4.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance5.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance.rating.add(score=1, user=self.user2, ip_address='127.0.0.2')

        # we should only need to call this once
        SimilarUser.objects.update_recommendations()

        self.assertEquals(SimilarUser.objects.count(), 2)

        recs = list(SimilarUser.objects.get_recommendations(self.user2, RatingTestModel))
        self.assertEquals(len(recs), 4)

        ct = ContentType.objects.get_for_model(RatingTestModel)

        IgnoredObject.objects.create(user=self.user2, content_type=ct, object_id=self.instance2.pk)

        recs = list(SimilarUser.objects.get_recommendations(self.user2, RatingTestModel))
        self.assertEquals(len(recs), 3)

        IgnoredObject.objects.create(user=self.user2, content_type=ct, object_id=self.instance3.pk)
        IgnoredObject.objects.create(user=self.user2, content_type=ct, object_id=self.instance4.pk)

        recs = list(SimilarUser.objects.get_recommendations(self.user2, RatingTestModel))
        self.assertEquals(len(recs), 1)
        self.assertEquals(recs, [self.instance5])

        self.instance5.rating.add(score=1, user=self.user2, ip_address='127.0.0.2')
        recs = list(SimilarUser.objects.get_recommendations(self.user2, RatingTestModel))
        self.assertEquals(len(recs), 0)

    def testSimilarUsers(self):
        Vote.objects.all().delete()

        self.instance.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance2.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance3.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance4.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance5.rating.add(score=1, user=self.user, ip_address='127.0.0.1')
        self.instance.rating.add(score=1, user=self.user2, ip_address='127.0.0.2')
        self.instance2.rating.add(score=1, user=self.user2, ip_address='127.0.0.2')
        self.instance3.rating.add(score=1, user=self.user2, ip_address='127.0.0.2')

        SimilarUser.objects.update_recommendations()

        self.assertEquals(SimilarUser.objects.count(), 2)

        recs = list(SimilarUser.objects.get_recommendations(self.user2, RatingTestModel))
        self.assertEquals(len(recs), 2)

        self.instance4.rating.add(score=1, user=self.user2, ip_address='127.0.0.2')

        SimilarUser.objects.update_recommendations()

        self.assertEquals(SimilarUser.objects.count(), 2)

        recs = list(SimilarUser.objects.get_recommendations(self.user2, RatingTestModel))
        self.assertEquals(len(recs), 1)
        self.assertEquals(recs, [self.instance5])

        self.instance5.rating.add(score=1, user=self.user2, ip_address='127.0.0.2')

        SimilarUser.objects.update_recommendations()

        self.assertEquals(SimilarUser.objects.count(), 2)

        recs = list(SimilarUser.objects.get_recommendations(self.user2, RatingTestModel))
        self.assertEquals(len(recs), 0)
