from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque

TicketNumber = 0
Est_time = {'oil': 0, 'tires': 0, 'diagnostic': 0}
OilQueue = deque()
TiresQueue = deque()
DiagnosticQueue = deque()
NextNumber = 0

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu_tmplt.html')


class Oil(View):
    def get(self, request, *args, **kwargs):
        global TicketNumber
        global Est_time
        global OilQueue
        TicketNumber += 1
        WaitingTime = Est_time['oil']
        Est_time['oil'] += 2
        OilQueue.append(TicketNumber)
        return render(request, 'tickets/Est_time.html', {'number': TicketNumber,
                                                         'time': WaitingTime})


class Tires(View):
    def get(self, request, *args, **kwargs):
        global TicketNumber
        global Est_time
        global TiresQueue
        TicketNumber += 1
        WaitingTime = Est_time['oil'] + Est_time['tires']
        Est_time['tires'] += 5
        TiresQueue.append(TicketNumber)
        return render(request, 'tickets/Est_time.html', {'number': TicketNumber,
                                                         'time': WaitingTime})


class Diagnostic(View):
    def get(self, request, *args, **kwargs):
        global TicketNumber
        global Est_time
        global DiagnosticQueue
        TicketNumber += 1
        WaitingTime = Est_time['oil'] + Est_time['tires'] + Est_time['diagnostic']
        Est_time['diagnostic'] += 30
        DiagnosticQueue.append(TicketNumber)
        return render(request, 'tickets/Est_time.html', {'number': TicketNumber,
                                                         'time': WaitingTime})


class Processing(View):
    def get(self, request, *args, **kwargs):
        global OilQueue
        global TiresQueue
        global DiagnosticQueue
        return render(request, 'tickets/Processing.html', {'OilQueueLength': len(OilQueue),
                                                            'TiresQueueLength': len(TiresQueue),
                                                            'DiagnosticQueueLength': len(DiagnosticQueue)})

    def post(self, request, *args, **kwargs):
        global NextNumber

        #    if len(OilQueue) + len(TiresQueue) + len(DiagnosticQueue) > 2:
        if len(OilQueue) != 0:
            NextNumber = OilQueue.popleft()
            Est_time['oil'] -= 2
        elif len(TiresQueue) != 0:
            NextNumber = TiresQueue.popleft()
            Est_time['tires'] -= 5
        elif len(DiagnosticQueue) != 0:
            NextNumber = DiagnosticQueue.popleft()
            Est_time['diagnostic'] -= 30
        return redirect('/next', )


class Next(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/Next.html', {'TicketNumber': NextNumber})
