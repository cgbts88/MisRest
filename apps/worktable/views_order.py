from datetime import datetime
from dateutil.relativedelta import relativedelta
from json import dumps as json_dumps

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WorkOrderLogSerializer, WorkOrderSerializer

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404
from django.views.generic.base import View
from .models import WorkOrder, WorkOrderLog
from .forms import OrderForm, InsteadForm
from users.models import Department

from utils.custom import MisCreateView, MisDeleteView, MisOrderListView, MisUpdateView
from utils.mixin import LoginRequiredMixin
from utils.toolkit import build_order_num, order_record, action_menu
from utils.mailer import send_work_order_message
from utils.util import form_invalid_msg

User = get_user_model()


"""
Here is WorkOrder Views


class WorkOrderListView(MisOrderListView):
    model = WorkOrderLog
    context_object_name = 'data_all'
    template_name = 'worktable/order/list.html'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        work_order_log = WorkOrderLog.objects.filter(record_type='create').values('record_time').first()
        date_start = datetime.now()
        date_end = work_order_log['record_time']
        date_list = []
        while date_start > date_end:
            date_list.append(str(date_start.year) + '-' + str(date_start.month).zfill(2))
            date_start -= relativedelta(months=1)
        kwargs['date_list'] = date_list
        kwargs['departments'] = Department.objects.all()
        return super().get_context_data(**kwargs)
"""


class WorkOrderListView(APIView):

    def get(self, request, format=None):
        work_order_log = WorkOrderLog.objects.filter(record_type='create')
        serializer = WorkOrderLogSerializer(work_order_log[0: 10], many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WorkOrderLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkOrderCreateView(MisCreateView):
    model = WorkOrder
    form_class = OrderForm
    template_name = 'worktable/order/create.html'

    def get_context_data(self, **kwargs):
        kwargs['types'] = WorkOrder.TYPES
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.num = build_order_num('A')
            new_form.proposer = request.user
            new_form.state = 'wait'
            new_form.save()
            order_record(recorder=new_form.proposer, num=new_form.num, record_type="create")
            send_work_order_message(new_form.num)
            res['result'] = True
        else:
            res = form_invalid_msg(form)
        return HttpResponse(json_dumps(res), content_type='application/json')


class WorkOrderInsteadView(MisCreateView):
    model = WorkOrder
    form_class = InsteadForm
    template_name = 'worktable/order/instead.html'

    def get_context_data(self, **kwargs):
        kwargs['types'] = WorkOrder.TYPES
        kwargs['users'] = User.objects.all().exclude(Q(username='admin') | Q(email=''))
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        form = self.get_form()
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.num = build_order_num('A')
            new_form.proposer = User.objects.get(id=request.POST['proposer'])
            new_form.state = 'wait'
            new_form.save()
            order_record(recorder=new_form.proposer, num=new_form.num, record_type="create")
            send_work_order_message(new_form.num)
            res['result'] = True
        else:
            res = form_invalid_msg(form)
        return HttpResponse(json_dumps(res), content_type='application/json')


class WorkOrderDeleteView(MisDeleteView):
    model = WorkOrder
    success_url = 'worktable/order'


class WorkOrderDetailView(MisUpdateView):
    model = WorkOrder
    form_class = OrderForm
    template_name = 'worktable/order/detail.html'

    def get_context_data(self, **kwargs):
        parameter = {
            'form_type': "A",
            'current_user': self.request.user.id,
            'order_status': self.object.state,
            'proposer': self.object.proposer.id,
            'leader': ''
        }
        actions_list = action_menu(**parameter)
        kwargs['types'] = WorkOrder.TYPES
        kwargs['records'] = WorkOrderLog.objects.filter(record_obj__num=self.request.GET['num'])
        kwargs['actions_list'] = actions_list
        kwargs['parameter'] = parameter
        kwargs['result'] = 'ban' if not actions_list else ''
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        res = dict(result=False)
        work_order = self.object()
        form = self.form_class(data=request.POST, instance=work_order)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.proposer = request.user
            new_form.state = 'wait'
            new_form.save()
            order_record(recorder=request.user, num=work_order.num, record_type="update")
            res['result'] = True
        else:
            res = form_invalid_msg(form)
        return HttpResponse(json_dumps(res), content_type='application/json')


class WorkOrderProcessView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            work_order = get_object_or_404(WorkOrder, pk=request.POST['id'])
            work_order.state = 'process'
            work_order.save()
            order_record(recorder=request.user, num=request.POST['num'], record_type="process")
            send_work_order_message(work_order.num)
            res['result'] = True
            return HttpResponse(json_dumps(res), content_type='application/json')


class WorkOrderFinishView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            work_order = get_object_or_404(WorkOrder, pk=request.POST['id'])
            work_order.state = 'finish'
            work_order.save()
            order_record(recorder=request.user, num=request.POST['num'], record_type="finish")
            send_work_order_message(work_order.num)
            res['result'] = True
            return HttpResponse(json_dumps(res), content_type='application/json')


class WorkOrderConfirmView(LoginRequiredMixin, View):

    @staticmethod
    def post(request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            work_order = get_object_or_404(WorkOrder, pk=request.POST['id'])
            work_order.state = 'confirm'
            work_order.save()
            order_record(recorder=request.user, num=request.POST['num'], record_type="confirm")
            send_work_order_message(work_order.num)
            res['result'] = True
            return HttpResponse(json_dumps(res), content_type='application/json')
