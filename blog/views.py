from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,\
PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/list.html'











def list(request,tag_slug=None):
    list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        list=list.filter(tags__in=[tag])
    paginator = Paginator(list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/list.html',{'posts': posts,'tag':tag})



def detail(request, year, month, day, post):
    post=get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=post,publish__year=year,publish__month=month,publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form=CommentForm()
    post_tags_ids=post.tags.values_list('id',flat=True)
    similar_posts=Post.published.filter(tags__in=post_tags_ids)\
                                .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags','-publish')[:4]
    return render(request,'blog/detail.html',{'post': post,'comments':comments,'form':form,'similar_posts': similar_posts})



def share(request,id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'ahmed.201900039@gmail.com',
                      [cd['to']])
            sent = True




    # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post,'form': form,'sent':sent})




@require_POST

def comment(request,id):
    post = get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
    coment=None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        coment=form.save(commit=False)
        coment.post=post
        coment.save()
    return render(request,'blog/comment.html',{'post':post,'form':form,'coment':coment})


