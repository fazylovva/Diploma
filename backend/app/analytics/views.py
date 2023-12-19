from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from analytics.models import DiscussionLikesDislikes
from article.models import Discussion


def analytics_view(request):
    if request.user.is_superuser:
        discussions = DiscussionLikesDislikes.objects.all()
        
        context = {
            'discussions': discussions
        }

        return render(request, 'analytics/analytics.html', context)
    return HttpResponse('', status=404)


@require_GET
def discussion_likes_dislikes(request):
    discussions = Discussion.objects.annotate(
        num_likes=Count('likes'),
        num_dislikes=Count('dislikes')
    ).values('id', 'comment', 'num_likes', 'num_dislikes')
    return JsonResponse({'discussions': list(discussions)})
