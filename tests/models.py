from django.db import models

from djangoratings.fields import AnonymousRatingField, RatingField


class RatingTestModel(models.Model):
    rating = AnonymousRatingField(range=2, can_change_vote=True)
    rating2 = RatingField(range=2, can_change_vote=False)

    def __unicode__(self):
        return unicode(self.pk)
