from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)

from ..media import models as media_modals
from ..channel import models as channel_modals


def search(query, limit=50):
    vector = SearchVector('name', weight='A') + SearchVector(
        'description', weight='B'
    )
    query_ = SearchQuery(query)
    channels = (
        channel_modals.Channel.objects.annotate(
            rank=SearchRank(vector, query_)
        )
        .filter(rank__gte=0.2)
        .order_by('-rank')
    )[:limit]
    vector = SearchVector('title', weight='A') + SearchVector(
        'description', weight='B'
    )
    query_ = SearchQuery(query)
    # TODO: exclude deleted
    videos = (
        media_modals.Video.objects.annotate(rank=SearchRank(vector, query_))
        .filter(rank__gte=0.2, visibility='public')
        .order_by('-rank')
    )[:limit]
    return {
        'channels': channels,
        'videos': videos,
    }
