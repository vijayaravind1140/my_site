from django.http import HttpResponse
from django.template import loader
from .models import Question
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.views import generic
# Create your views here.


# def index(request):
#     return HttpResponse("Hello ,world.you're at poll index")


# def index(request):
#     latest_question_list=Question.objects.order_by("-pub_date")[:5]
#     output=", ".join([q.question_text for q in latest_question_list])
#     template=loader.get_template("polls/index.html")
#     context={"latest_question_list":latest_question_list,}
#     return HttpResponse(template.render(context,request))

#
# def index(request):
#     latest_question_list=Question.object.order_by("-pub-date")[:5]
#     context={"latest_question_list":latest_question_list}
#     return render(request,"polls/index.html",context)


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]



# def detail(request, question_id):
#     return HttpResponse("you're looking at question %s." % question_id)

# def detail(request,question_id):
#     try:
#         question=Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request,"polls/detail.html",{"question":question})

# def detail(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/detail.html",{"question":question})


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

# def results(request, question_id):
#     # response = "you're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    # return HttpResponse("you're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
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
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
