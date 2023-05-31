from django.urls import path


from test_fixers import views


app_name = "test_fixers"
urlpatterns = [
    path("example1", views.test_controller1.Controller.as_view(), name="example1"),
    path("example2", views.test_controller2.Controller.as_view(), name="example2"),
	path('test', views.test.Controller.as_view(), name='test'),
	path('test-redirect', views.test_redirect.Controller.as_view(), name='test_redirect'),
	path('add-domain-1', views.add_domain_1.Controller.as_view(), name='add_domain_1'),
	path('add-domain-2', views.add_domain_2.Controller.as_view(), name='add_domain_2'),
	path('add-domain-3', views.add_domain_3.Controller.as_view(), name='add_domain_3'),
	path('add-domain-4', views.add_domain_4.Controller.as_view(), name='add_domain_4'),
	path('add-domain-5', views.add_domain_5.Controller.as_view(), name='add_domain_5'),
	path('<path:path>', views.index.Controller.as_view(), name='index'),
]
