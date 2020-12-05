from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Blog, Photo, Comment
from .forms import CommentForm

# Create your views here.

def home(request):
    blogs = Blog.objects
    #블로그 모든 글들을 대상으로
    blog_list=Blog.objects.all()
    #블로그 객체 세 개를 한 페이지로 자르기
    paginator = Paginator(blog_list,3)
    #request된 페이지가 뭔지 알고 request페이지를 변수에 담음
    page = request.GET.get('page')#html에서 온 값
    #request된 페이지를 얻어온 뒤 return 해 준다.
    posts = paginator.get_page(page)

    return render(request, 'home.html', {'blogs':blogs, 'posts':posts})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)#Blog 모델명
    mycom_form = CommentForm()
    context = {'comment_form':mycom_form,'blog_detail':blog_detail}
    return render(request, 'detail.html', context)

def write(request):
    return render(request, 'write.html')

def send(request):
    if(request.method == 'POST'):
        blog = Blog()
        blog.title = request.POST['title']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.description = request.POST['description']
        blog.save()
        for img in request.FILES.getlist('image'):
            photo = Photo()
            photo.post = blog
            photo.image = img
            photo.save()
        return redirect('/blog/' + str(blog.id))
    else:
        return render(request, 'new.html')

def delete(request, blog_id):
    blog_delete = get_object_or_404(Blog, pk=blog_id)
    blog_delete.delete()
    return redirect('home')

def update(request, blog_id):
    blog_update = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'update.html', {'blog_update':blog_update})

def updateSend(request, blog_id):
    updateSendBlog = get_object_or_404(Blog, pk=blog_id)
    updateSendBlog.title = request.GET['updateTitle']
    updateSendBlog.body = request.GET['updatebody']
    updateSendBlog.pub_date = timezone.datetime.now()
    updateSendBlog.save()
    return redirect('home')

def create_comment(request, blog_id):
    filled_form = CommentForm(request.POST) #post 요청으로 넘어온 form data들을 CommentForm양식에 담아서 filled_form으로 저장

    if filled_form.is_valid():    
    #정상적인 값들이 입력이 되었으면 if문 안으로 들어가서 save()작업을 할꺼고 
    #만약 유효성 검사에 실패해도 다시 입력을 받아야하므로 return redirect를 if문 밖으로 빼서 모든 경우에 detail로 돌아가게했다.
        temp_form = filled_form.save(commit=False)  
        
        #그런데 modelform이 입력받는 값은 body에 대한 값 밖에 없으므로 어떤글에 해당하는 댓글인지 아직 모른다. 
        #그래서 어떤 글인지를 지정해서 저장해야하므로 commit= False옵션을 주고 잠시 저장을 미룬다.
        # 그리고 그 저장을 미룬 상태의 값을 temp_form에 저장했다.
        temp_form.post = Blog.objects.get(id = blog_id) #어디에 적힌 글인지 지정해줘야하는데 단순히 글 번호만 알려주는게 아닌
        #진짜 어떤글인지를 알려줘야한다( 단순히 숫자만을 알려주는게 아니라 진짜 어떤글인지 객체를 지정해줘야한다는 말)
        #그리고 그 객체는 우리가 넘겨받은 jss_id를 통해서 댓글을 적은 글을 찝어서 가져올수있다.
        temp_form.save() #저장!
    
    return redirect('detail', blog_id) #redirect('애칭', parameter) 해주면 google.com/1 이런식으로 뒤에 붙는 값을 지정해줄수있다.

def delete_comment(request, i_id, blog_id):
    mycom = Comment.objects.get(id = i_id)#이걸 해놨기에 뭐든 상관없는거!
    mycom.delete()
    return redirect('detail', blog_id)