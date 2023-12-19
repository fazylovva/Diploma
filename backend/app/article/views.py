from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from account.models import User
from article.models import ArticleAdmin, Article, Discussion, ViewedArticle


def ArticlesPage(request):
    superusers = User.objects.filter(is_superuser=True)
    article_ids = [superuser.id for superuser in superusers]
    articles = Article.objects.filter(author__in=article_ids)

    context = {
        'articles': articles
    }

    return render(request, 'main/articles.html', context)


def ArticleDetail(request, pk):
    article = get_object_or_404(Article, id=pk)
    discussions = Discussion.objects.filter(article=article)

    user = request.user.id
    if user is not None:
        if not ViewedArticle.objects.filter(user=request.user, article=article).exists():
            ViewedArticle.objects.create(user=request.user, article=article)

    if request.method == 'POST':
        comment = request.POST['comment']
        is_anonymous = request.POST.getlist('anonymous')

        if comment:
            discussion = Discussion.objects.create(
                author=request.user,
                article=article,
                comment=comment,
                is_anonymous=False
            )

            if is_anonymous:
                discussion.is_anonymous = True

            discussion.save()
            return HttpResponseRedirect(reverse('article-detail', kwargs={'pk': article.pk}))

    count_of_views = ViewedArticle.objects.filter(article=article).count()

    context = {
        'article': article,
        'discussions': discussions,
        'count_of_views': count_of_views
    }

    for discussion in discussions:
        discussion.liked = discussion.like.filter(id=request.user.id).exists()

    for discussion in discussions:
        discussion.disliked = discussion.dislike.filter(id=request.user.id).exists()

    for discussion in discussions:
        discussion.complained = discussion.complain.filter(id=request.user.id).exists()

    return render(request, 'main/article-detail.html', context)


def BlogPage(request):
    superusers = User.objects.filter(is_superuser=True)
    article_ids = [superuser.id for superuser in superusers]
    articles = Article.objects.filter(is_approved=True)

    if not request.user.is_authenticated:
        return redirect('sign-in')
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        description = request.POST.get('description')

        if not (image and title and summary and description):
            messages.info(request, 'Empty fields are not allowed!')
            return redirect('blog')

        Article.objects.create(
            author=request.user,
            image=image,
            title=title,
            summary=summary,
            description=description
        ).save()
        messages.success(request, 'Article details sent to the moderator successfully!')

        html_template = 'article/add_article_notf.html'

        article = Article.objects.last()

        context = {
            'author': request.user,
            'image': article.image_url,
            'title': title,
            'summary': summary,
            'description': description
        }

        html_message = render_to_string(html_template, context)

        notification = EmailMessage(
            subject=f'{request.user.first_name} wants to add a article!',
            body=html_message,
            from_email='womenssdiary@gmail.com',
            to=['womenssdiarymoderator@gmail.com']
        )
        notification.content_subtype = 'html'
        notification.send()

        return redirect('/')

    context = {
        'articles': articles,
    }

    return render(request, 'main/blog.html', context)


def LikeComment(request, pk):
    user = request.user
    comment_like = get_object_or_404(Discussion, id=request.POST.get('comment_like'))
    liked_comment = False
    if user in comment_like.like.all():
        comment_like.like.remove(user)
        liked_comment = False
    else:
        comment_like.like.add(user)
        if user in comment_like.dislike.all():
            comment_like.dislike.remove(user)
        liked_comment = True
    return redirect('article-detail', pk=comment_like.article.id)


def DislikeComment(request, pk):
    user = request.user
    comment_dislike = get_object_or_404(Discussion, id=request.POST.get('comment_dislike'))
    disliked_comment = False
    if user in comment_dislike.dislike.all():
        comment_dislike.dislike.remove(user)
        disliked_comment = False
    else:
        comment_dislike.dislike.add(user)
        if user in comment_dislike.like.all():
            comment_dislike.like.remove(user)
        disliked_comment = True
    return redirect('article-detail', pk=comment_dislike.article.id)


def ComplainComment(request, pk):
    user = request.user
    complain_comment = get_object_or_404(Discussion, id=request.POST.get('comment_complain'))
    comment = get_object_or_404(Discussion, id=pk)

    complained = False
    if user in complain_comment.complain.all():
        complain_comment.complain.remove(user)
        complained = False
    else:
        complain_comment.complain.add(user)
        complained = True

        subject = 'Warning: Comment violation'
        message = f'Your comment on <{comment.article.title}> has been reported by other users and may violate our ' \
                  f'community guidelines. Please review our guidelines and ensure your comments are respectful ' \
                  f'and ' \
                  f'constructive. Thank you. '
        from_email = 'womenssdiary@gmail.com'
        to_email = [comment.author.email]
        EmailMessage(subject, message, from_email, to_email).send()

    return redirect('article-detail', pk=complain_comment.article.id)
