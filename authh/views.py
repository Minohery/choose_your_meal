from django.shortcuts import render

# Create your views here.

from django.views import View
from .forms import LoginForm, ConfirmForm, ChangeForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from choice.models import User
from django.core.mail import send_mail
from random import randint
from random import shuffle
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.views.decorators.cache import cache_page
from django.core import signing
from random import randint


#function that generates a random 6-digit code
def gen_code():
    r=""
    for i in range(6):
        r += str(randint(1,6))
    return int(r)

#function that generates a password with 8 characters
def set_new_password():
    l="azertyuiopqsdfghjklmwxcvbnAZERTYUIOPQSDFGHJKLMWXCVBN123456789"
    i=list(l)
    shuffle(i)
    return ''.join(i[0:8])

#login view
class LoginView(View):
    template_name = "authh/Login.html"
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('authh:home'))
        else:
            form=LoginForm()
            return render(request, self.template_name, {'form':form})
    def post(self, request):
        form=LoginForm(request.POST)
        username=request.POST['Username']
        password=request.POST['Password']
        #check if the user exists in the database
        o=authenticate(request, username=username, password=password)
        if o is not None:
            a=User.objects.get(username=username)
            #check whether the user has a confirmtion_code. If so, the program will set\
            #confirm to false, thus the user won't have any access to the confirmation
            #page wehn resetting the password.
            #else, the program will simply login the user, if the confirmation_code does
            #not exist
            try:
                h=a.confirmation_code_set.get(ref=1)
            except:
                login(request, o)
                return HttpResponseRedirect(reverse('authh:home'))
            else:
                h.confirm=False
                h.save()
                login(request, o)
                return HttpResponseRedirect(reverse('authh:home'))
        else:
            #if the user is not authenticated
            return render(request, 'authh/Login.html', {'error':"Your password or your\
                                                           username does not match. Please try again.", 'form':form,})
#Home view
class Home(View):
    template_name = "authh/home.html"
    def get(self, request):
        return render(request, self.template_name)

#logging out action
def logging_out(request):
    #check if the user has permission to access success page when changing password.
    #If so, the permission is deleted. Thus, next time he logs in, he will not have
    #an access to that success page.
    try:
        a=request.user.has_perm_success_set.get(ref=1)
    except:
        logout(request)
        return HttpResponseRedirect(reverse('authh:home'))
    else:
        request.user.has_perm_success_set.get(ref=1).delete()
        logout(request)
        return HttpResponseRedirect(reverse('authh:home'))

#reset a password when not logged in
class reset_password(View):
    template_name='authh/reset_password.html'
    def post(self, request):
        form=ChangeForm(request.POST)
        if form.is_valid:
            username=request.POST['Username']
            #if the username exists
            if User.objects.filter(username=username).exists():
                a=User.objects.get(username=username)
                #generate a 6-digit-code, that will be sent by mail to the username's
                #email
                code = gen_code()
                #Create a confirmation code that corresponds to the user if it does not exist
                c=a.confirmation_code_set.update_or_create(ref=1, defaults={'num':code, 'qualified':True},)
                c[0].save()
                #send mail to the user (the from_email is the DEFAULT_FROM_MAIL in the settings)
                send_mail("Confirmation code", "Here is your confirmation code : {}".format(code), None, [a.email])
                return HttpResponseRedirect(reverse('authh:conf_page', args=(username,)))
            else:
                return render(request, self.template_name, {'error_message':'Please enter an existing username', 'form':form})

    def get(self, request):
        if not request.user.is_authenticated:
            form=ChangeForm()
            return render(request, self.template_name, {'form':form})
        else:
            #If the user is athenticatedn he is not allowed to access the reset_password page
            return HttpResponseRedirect(reverse('authh:home'))

class confirm(View):
    template_name='authh/confirm.html'
    def get(self, request, pk):
        if not request.user.is_authenticated:
            uu=User.objects.get(username=pk)

            #If the user is allowed to access the confirm view
            if uu.confirmation_code_set.get(ref=1).qualified==True:
                form=ConfirmForm()
                return render(request, self.template_name, {'form':form})
            else:

                #Else redirect to reset_password page
                return HttpResponseRedirect(reverse('authh:reset_password'))
        else:
            return HttpResponseRedirect(reverse('authh:home'))

    def post(self, request, pk):
        form = ConfirmForm(request.POST)
        usr=User.objects.get(username=pk)
        codei=usr.confirmation_code_set.get(ref=1)
        if form.is_valid():
            code=request.POST["code"]
            if len(str(code)) != 6:

                #If there are more or less than 6-digits typed by the user
                return render(request, self.template_name, {'error_message':'Please enter 6 digits.', 'form':form,})
            else:

                #If the code is correct
                if int(code)==codei.num:
                    newPassword=set_new_password()
                    usr.set_password(newPassword)
                    usr.save()
                    send_mail(
                    "Password change",
                    'This is your new password : {}'.format(newPassword),
                    None,
                    [usr.email],
                    )
                    codei.qualified=False
                    codei.save()
                    codei.confirm=True
                    codei.save()
                    return HttpResponseRedirect(reverse("authh:reset_pass_success", args=(pk,)))

                #Else, display an error message.
                else:
                    return render(request, self.template_name, {'error':"Ce n est pas le bon code. Veuillez reessayer ou reinitialiser votre formulaire",
                    'form':form,})

class reset_pass_success(View):
    template_name='authh/success.html'
    def get(self, request, pk):
        a=User.objects.get(username=pk)
        try:
            #Check if the confirmation_code exists or not
            b=a.confirmation_code_set.get(ref=1)
        except:
            return HttpResponseRedirect(reverse("authh:home"))
        #If the confirmation_code exists:
        if b.confirm == True:
            return render(request, self.template_name)
        else:
            return HttpResponseRedirect(reverse('authh:home'))

class change_pass_success(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    template_name='authh/change_pass_success.html'
    def get(self, request):
        usr=get_object_or_404(User, pk=request.user.pk)
        try:

            #Check if the user has the permission to access the page
            a=usr.has_perm_success_set.get(ref=1)
        except:
            return HttpResponseRedirect(reverse('authh:home'))
        else:
            if a.permission==True:
                return render(request, self.template_name)
            else:
                return HttpResponseRedirect(reverse('authh:home'))


class change_password(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    template_name='authh/change_password.html'
    def get(self, request):
        form=PasswordChangeForm(user=request.user)
        return render(request, self.template_name, {'form': form, })
    def post(self, request):
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            usr=get_object_or_404(User, pk=request.user.pk)
            try:

                #Check if the user has the permission to access success page
                a=usr.has_perm_success_set.get(ref=1)
            except:

                #If not, create a permission and set the permission to True
                r=usr.has_perm_success_set.create(ref=1, permission=True)
                r.save()
                return HttpResponseRedirect(reverse('authh:change_pass_success'))
            #Set the permission to True if the user has one
            a.permission=True
            a.save()
            return HttpResponseRedirect(reverse('authh:change_pass_success'))
        else:
            return render(request, self.template_name, {'error':'Review your errors', 'form':PasswordChangeForm(user=request.user)})

