from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import dish
from .forms import choice_form
from django.views import View
from .forms import choice_form

# Create your views here.



class choice(View):
    form_class = choice_form
    initial = {'key':'value'}
    def get(self, request):

        #Display the form
        form = self.form_class(initial=self.initial)
        return render(request, "choice/choice.html", {'liste':dish.objects.all(),
           "choice":form, "current":request.user.choosen})

    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():

            #if user has not ordered yet
            if request.user.command==False:
                if int(request.POST["choose"]) <= dish.objects.count():
                    #The menu that the user has choosen will be saved
                    request.user.choosen = int(request.POST["choose"])
                    request.user.save()
                    return render(request, "choice/choice.html", {'liste':dish.objects.all(),
                                                        "choice":choice_form(), "current":request.user.choosen })

                #if the reference number is higher than the number of menu that we can choose from, an error would have apparently occured
                else:
                    return render(request, "choice/choice.html", {'liste':dish.objects.all(),
                            "choice":choice_form, "current":request.user.choosen, "message":"Please choose again,\
                               an error occured." })
                
            #if the user has already ordered, the form is not displayed, so that the user cannot choose
            else:
                return render(request, "choice/choice.html", {'liste':dish.objects.all(),
                             "current":request.user.choosen, })

        #if form is not valid
        return render(request, "choice/choice.html", {'liste':dish.objects.all(),
                             "current":request.user.choosen, })
                
    
        




        



