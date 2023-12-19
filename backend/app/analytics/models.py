from django.db import models


class DiscussionLikesDislikes(models.Model):
    id = models.IntegerField(primary_key=True)
    comment = models.CharField(max_length=255)
    likes = models.IntegerField()
    dislikes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'discussion_likes_dislikes'
