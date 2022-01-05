from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View

from time import mktime, strptime
from .models import Choice, Question, User
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'bi/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'bi/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'bi/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'bi/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('bi:results', args=(question.id,)))




class UserPredictAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        stocks = User.objects.all().order_by('sign_date')

        price_list = []
        camera_list = []
        for stock in stocks:
            time_tuple = strptime(str(stock.sign_date), '%Y-%m-%d')
            utc_now = mktime(time_tuple) * 1000
            price_list.append([utc_now, stock.price])
            camera_list.append([utc_now, stock.camera_num])

        data = {
            'price': price_list,
            'camera_num': camera_list
        }

        return Response(data)

class UserPercentAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        stocks = User.objects.all().order_by('sign_date')

        price_list = []
        camera_list = []
        for stock in stocks:
            time_tuple = strptime(str(stock.sign_date), '%Y-%m-%d')
            utc_now = mktime(time_tuple) * 1000
            price_list.append([utc_now, stock.price])
            camera_list.append([utc_now, stock.camera_num])

        data = {
            'price': price_list,
            'camera_num': camera_list
        }

        return Response(data)

class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'bi/chart.html')