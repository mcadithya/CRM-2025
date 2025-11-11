from django.urls import path

from . import views

urlpatterns=[
            path("batch-list/",views.BatchListView.as_view(), name = 'batch-list'),
            path("add-batch/",views.AddBatchView.as_view(), name = 'add-batch'),
            path("edit-batch/<str:uuid>/",views.EditBatchView.as_view(), name = 'edit-batch'),
            path("delete-batch/<str:uuid>/",views.BatchDeleteView.as_view(), name = 'delete-batch'),
            path("batch-details/<str:uuid>/",views.BatchDetailsView.as_view(), name = 'batch-details')
             ]
