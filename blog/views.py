from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from .form import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'
def post_list(request, tag_slug=None):         # выводим только запосченные объявления
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)                       # по 3 поста на каждой странице
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list =object_list.filter(tags__in=[tag])
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)                               # Если страница не является целым числом, отправляем первую страницу
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)             # Если страница вне диапазона отправляем последнюю страницу результатов
    return render(request, 'blog/post/list.html',{'page': page, 'posts': posts, 'tag':tag})
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этой записи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method =='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)           # Создать объект комментариев, но еще не сохранять его в базе
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments,
                                                     'new_comment': new_comment,'comment_form': comment_form})
def post_share(request, post_id):                                   # Получаем сообщение по его id
    post = get_object_or_404(Post, id=post_id,  status='published')
    sent = False
    if request.method == 'POST':                                    # Форма была отправлена
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data                                  # ... отправляем email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading " {}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post' : post, 'form': form, 'sent': sent})


