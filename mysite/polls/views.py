from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from .models import Question, Choice, Vote
from django.urls import reverse
from django.views import View, generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import logout
from .permissions import user_gains_perms 
from django.contrib.auth.decorators import permission_required
import random

# Create your views here.


#class IndexView(generic.ListView):
    #template_name = "polls/index.html"
    #context_object_name = "latest_question_list"

    #def get_queryset(self):
        #"""
        #Return the last five published questions (not including those set to be
       # published in the future).
      #  """
       # return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        #    :5
      #  ]


class IndexView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    redirect_field_name = "my_redirect_field"   #elimina este si quieres que al iniciar sesion con esta url te manda a esta url
    template_name = "polls/Bootstrap.html"
    context_object_name = "latest_question_list"

    def get(self, request, *args, **kwargs):
      if not self.request.user.has_perm('auth.view_user'):    #  'nombre_de_la_app.    view o change o add el que queramos_ nombre_del_modelo'
            return HttpResponseForbidden()
      else: 
        # Obtenemos el queryset de preguntas
        queryset = self.get_queryset()

        # Creamos el contexto para el template
        context = {
            self.context_object_name: queryset,
        }

        # Renderizamos el template con el contexto y lo devolvemos como respuesta
        return render(request, self.template_name, context)

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())



def results(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    labels = []
    data = []

    for choice in question.choice_set.all():
        labels.append(choice.choice_text)
        data.append(choice.vote_set.count())

    cantidadcolor = len(labels)
    colores = []

    for _ in range(cantidadcolor):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colores.append(f'rgb({r}, {g}, {b})')

    return render(
        request,
        'polls/results.html',
        {'question': question, 'labels': labels, 'data': data, 'colores': colores}
    )



    
@login_required
def Index(request):
    return render(request, 'polls/superindex.html')



@login_required(redirect_field_name="my_redirect_field") #la diferencia es que cuando inicias sesion aqui, no te redirecciona al url de este def
def my_view1(request):
    # Código de la vista
    return render(request, 'polls/my_view1.html')


@login_required(login_url="/accounts/login/")
def my_view2(request):
    # Código de la vista
    return render(request, 'polls/my_view2.html')


def salir(request):
    logout(request)
    return redirect('/accounts/login/')




@login_required(login_url="/accounts/login/")
def some_view(request):
    user_id = request.user.id  # Obtén el ID del usuario actual
    usuario_anteriormente_tenia_permisos = user_gains_perms(request, user_id)  # Llama al método user_gains_perms

    if usuario_anteriormente_tenia_permisos:
        contexto = "tienes estos permisos"
        return render(request, 'polls/some_template.html', {'contexto': contexto})
    else:
        contexto = "No tienes estos permisos"
        return render(request, 'polls/some_template.html', {'contexto': contexto})
    







def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        
        user = request.user  # Assuming you have user authentication enabled
    
        # Create a new Vote object
        vote = Vote(choice=selected_choice, nombreusuario=user)
        vote.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    


   