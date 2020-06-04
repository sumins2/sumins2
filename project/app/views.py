from django.shortcuts import render, redirect
from .models import post, comment
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .utils import upload_img
# Create your views here.
def home(request):
    posts= post.objects.all().order_by('date')
    return render(request, 'home.html', {'posts' : posts})



def detail(request, name_of_pk):
    detail_of_post = post.objects.get(pk=name_of_pk)
    comment_of_post = comment.objects.filter(post_that_i_wrote_a_comment=detail_of_post)
    if request.method =="POST":
        comment.objects.create(
            post_that_i_wrote_a_comment = detail_of_post,
            content = request.POST['suminbest'],
            author = request.user
        )
        return redirect('detail', name_of_pk)


    return render (request, 'detail.html', {'detail_of_post': detail_of_post, 'comment_of_post' : comment_of_post})

def delete(request, name_of_pk):
    detail_of_post = post.objects.get(pk=name_of_pk)
    detail_of_post.delete()
    return redirect('home')

def comment_delete(request, pk_of_comment, post_pk):
    comment_of_post = comment.objects.get(pk=pk_of_comment)
    comment_of_post.delete()
    return redirect('detail', post_pk)

def edit(request, name_of_pk):
    detail_of_post = post.objects.get(pk=name_of_pk)
    
    if request.method == 'POST':
        post.objects.filter(pk=name_of_pk).update(
            title = request.POST['title'],
            content = request.POST['content'],
            date= request.POST['date']

        )
        return redirect('detail', name_of_pk)
    return render(request, 'edit.html', {'detail_of_post':detail_of_post})

def edit_comment(request, post_pk, pk_of_comment):
    detail_of_post = post.objects.get(pk = post_pk)

    comment_to_edit = comment.objects.get(pk = pk_of_comment)
    if request.method == "POST":
        comment.objects.filter(pk = pk_of_comment).update (
            post_that_i_wrote_a_comment = post_pk,
            content = request.POST['content'],
            author = request.user
        )
        return redirect('detail', post_pk)
    return render(request, 'edit_comment.html', {'detail_of_post' : detail_of_post, 'comment_to_edit': comment_to_edit})

def signup(request):

    if request.method == "POST":
        found_user = User.objects.filter(username = request.POST['username'])
        if len(found_user) > 0 :
            error = '이미 존재하는 username입니다'
            return render(request, 'registration/signup.html', {'error' : error})

        new_user = User.objects.create_user(
            username = request.POST['username'],
            password = request.POST['password']
        )
        auth.login(
            request,
            new_user,
            backend = 'django.contrib.auth.backends.ModelBackend')
        return redirect('home')

    return render(request, 'registration/signup.html')



def login(request):
    if request.method =="POST":
        found_user = auth.authenticate(
            username = request.POST['username'],
            password = request.POST['password']
        )
        if found_user is None:
            error = "아이디 또는 비밀번호가 틀렸습니다."
            return render(request, 'registeration/login.html', {'error' : error})

        auth.login(
            request,
            found_user,
            backend = 'django.contrib.auth.backends.ModelBackend'
            )
        return redirect(request.GET.get('next', '/'))

    return render(request,'registration/login.html')
    
@login_required(login_url = 'registration/login')
def new(request):
    if request.method == "POST":
        img_to_upload = request.FILES.get('img')
        new_post = post.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            date = request.POST['date'],
            author = request.user,
            img = upload_img(request, img_to_upload)
        )
        return redirect('detail', new_post.pk)
    return render(request, 'new.html')


def logout(request):
    auth.logout(request)
    return redirect('home')

# @login_required(login_url = 'registration/login')
# def home_private(request):
   
#     todolist = post.objects.filter(author = request.user).order_by('date')
#     username = request.user.username
    
#     for todo in todolist:
#         timeleft = todo.deadline - dt.datetime.now(pytz.utc) - dt.timedelta(hours=9)
#         timeleft_f = {"days" : timeleft.days, "hours" : timeleft.seconds//3600, "minutes" : timeleft.seconds%3600//60}
#         timeleft_str = f"{timeleft_f['days']} 일 {timeleft_f['hours']} 시간 {timeleft_f['minutes']} 분"
#         todo.timeleft = timeleft_str

#     return render(request, 'home_private.html', {'todolist' : todolist, 'username' : username })

# 댓글 삭제 / 수정이 안됨 ㅠㅠ!