from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.urls import reverse
from django.views import View, generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
    redirect_field_name = "my_redirect_field"
    template_name = "polls/Bootstrap.html"
    context_object_name = "latest_question_list"

    def get(self, request, *args, **kwargs):
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
        data.append(choice.votes)

    return render(
        request,
        'polls/results.html',
        {'question': question, 'labels': labels, 'data': data}
    )



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
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
@login_required
def Index(request):
    return render(request, 'polls/superindex.html')



@login_required(redirect_field_name="my_redirect_field")
def my_view1(request):
    # Código de la vista
    return render(request, 'polls/my_view1.html')


@login_required(login_url="/accounts/login/")
def my_view2(request):
    # Código de la vista
    return render(request, 'polls/my_view2.html')


