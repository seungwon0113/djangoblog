from users.services import UserService
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from categories.models import Category
from posts.services import get_category_post_count

# user_profile View
class UserProfileView(View):
    def get(self, request):
        try:
            if not request.user.is_authenticated:
                return render(request, 'users/login.html', {
                    'error': '로그인 후 이용해주세요.',
                    'next': request.path  # 로그인 후 돌아올 페이지 저장
                })
                
            user = UserService.get_user_by_username(request.user.username)
            categories = Category.objects.all()
            # 카테고리별 게시글 수 계산
            category_post_count = get_category_post_count(user)
            return render(request, 'users/profile.html', {
                'user': user,
                'categories': categories,
                'category_post_count': category_post_count
            })
        except Exception as e:
            return render(request, 'users/login.html', {'error': str(e)})

# user_signup View
class UserSignupView(View):
    def get(self, request):
        return render(request, 'users/signup.html')

    def post(self, request):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            # 비밀번호 확인
            if password1 != password2:
                raise ValueError("비밀번호가 일치하지 않습니다.")
                
            # 사용자 생성
            user = UserService.create_user(
                username=username,
                password=password1,  # password1을 password로 전달
                email=email
            )
            
            # 로그인 처리
            login(request, user)
            return redirect('index')
            
        except Exception as e:
            return render(request, 'users/signup.html', {'error': str(e)})

# user_update View
class UserUpdateView(View):
    def post(self, request):
        try:
            user = UserService.update_user(
                request.user,
                username=request.POST.get('username'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone')
            )
            return redirect('users:user_profile')
        except Exception as e:
            # 에러가 발생하면 프로필 페이지로 돌아가서 에러 메시지 표시
            return render(request, 'users/profile.html', {
                'user': request.user,
                'error': str(e)
            })

# user_login View
class UserLoginView(View):
    def get(self, request):
        return render(request, 'users/login.html', {
            'next': request.GET.get('next', '')
        })

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', '')
            return redirect(next_url if next_url else 'index')
        else:
            return render(request, 'users/login.html', {
                'error': '아이디 또는 비밀번호가 틀렸습니다.',
                'next': request.POST.get('next', '')
            })

    
class UserLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('index')