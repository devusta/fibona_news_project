from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import View

from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomProfileChangeForm
from .models import CustomUser, Profile
from news.models import Comment, News


# class'ga asoslangan custom signup view
class CustomUserCreationView(View):
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('login')
# /class'ga asoslangan custom signup view


@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'pages/dashboard.html', context)


# class'ga asoslangan CustomUserChangeView
class CustomUserChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = CustomProfileChangeForm(instance=request.user.profile)
        return render(request, 'registration/user_change.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = CustomUserChangeForm(instance=request.user, data=request.POST)
        profile_form = CustomProfileChangeForm(instance=request.user.profile,
                                               data=request.POST,
                                               files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            print(request.user.profile.address)
            print(request.user.profile.photo)
            return redirect('dashboard')
# /class'ga asoslangan CustomUserChangeView


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser:
            return HttpResponse("<h2>You have no such right!</h2>")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@admin_required
def admin_page_view(request):
    all_news = News.published.all().order_by('-publish_time')
    users = CustomUser.objects.all()
    admins = CustomUser.objects.filter(is_superuser=True)
    comments = Comment.objects.all()
    context = {
        'all_news': all_news,
        'users': users,
        'admins': admins,
        'comments': comments
    }
    return render(request, 'pages/admin_page.html', context)


@admin_required
def comment_delete_view(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('admin_page')


@admin_required
def toggle_comment_status_view(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.is_active = not comment.is_active
    comment.save()
    return JsonResponse({'success': True, 'is_active': comment.is_active})


@admin_required
def toggle_user_status_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return JsonResponse({'success': True, 'is_active': user.is_active})


@admin_required
def user_info_view(request, user_id):
    user = request.user
    view_user = get_object_or_404(CustomUser, pk=user_id)
    context = {
        'user': user,
        'view_user': view_user
    }
    return render(request, 'pages/user_info.html', context)


# # funksiyaga asoslangan user_change_view
# @login_required
# def user_change_view(request):
#     if request.method == 'POST':
#         user_form = CustomUserChangeForm(instance=request.user, data=request.POST)
#         profile_form = CustomProfileChangeForm(instance=request.user.profile,
#                                                data=request.POST,
#                                                files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('dashboard')
#
#     else:
#         user_form = CustomUserChangeForm(instance=request.user)
#         profile_form = CustomProfileChangeForm(instance=request.user.profile)
#
#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#     }
#     return render(request, 'registration/user_change.html', context)
# # /funksiyaga asoslangan user_change_view


# # Tayyor viewdan meros oluvchi custom signup view
# class CustomUserCreationView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'
# # /Tayyor viewdan meros oluvchi custom signup view


# # funksiyaga asoslangan custom signup view
# def custom_signup_view(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             Profile.objects.create(user=user)
#             context = {
#                 'user': user,
#             }
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'registration/signup.html', context)
# # /funksiyaga asoslangan custom signup view


# # funksiyaga asoslangan custom login view
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(request,
#                                 username=data['username'],
#                                 password=data['password'])
#             print(data)
#             print(user)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Logged in successfully!')
#                 else:
#                     return HttpResponse('Your registration is inactive!')
#
#             else:
#                 return HttpResponse('Invalid login or password!')
#
#     else:
#         form = LoginForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'registration/login.html', context)
# # /funksiyaga asoslangan custom login view


