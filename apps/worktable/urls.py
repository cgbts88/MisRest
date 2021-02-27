from django.urls import path, re_path
# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from apps.worktable import views, views_order

router = DefaultRouter()
router.register(r'order', views_order.WorkOrderView, basename='order')
urlpatterns = router.urls
"""
urlpatterns = [

    path('', views.WorktableIndexView.as_view(), name='index'),
    path('phonebook/', views.PhoneBookView.as_view(), name='phonebook'),
    path('notice/', views. NoticeCenterView.as_view(), name='notice'),
    path('person/', views. PersonCenterView.as_view(), name='person'),
    path('person/passwdchange/', views. PersonPasswordChangeView.as_view(), name='passwdchange'),

    # Form_A Router
    path('order/', work_order_list, name='order-list'),
    path('order/create/', views_order.WorkOrderCreateView.as_view(), name='order-create'),
    path('order/instead/', views_order.WorkOrderInsteadView.as_view(), name='order-instead'),
    path('order/delete/', views_order.WorkOrderDeleteView.as_view(), name='order-delete'),
    re_path(r'^order/detail/(?P<pk>\d+)$', views_order.WorkOrderDetailView.as_view(), name='order-detail'),
    # path('order/detail/', views_order.WorkOrderDetailView.as_view(), name='order-detail'),
    path('order/process/', views_order.WorkOrderProcessView.as_view(), name='order-process'),
    path('order/finish/', views_order.WorkOrderFinishView.as_view(), name='order-finish'),
    path('order/confirm/', views_order.WorkOrderConfirmView.as_view(), name='order-confirm'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
"""