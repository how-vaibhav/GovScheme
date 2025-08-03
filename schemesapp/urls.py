from django.urls import path
from . import views

urlpatterns = [
      path('home/', views.home, name = "home"),
      path('feedback/', views.feedback, name = "feedback"),
      path('feedbacks/', views.view_feedback, name = "view_feedbacks"),
      path('login/', views.login_view, name = "login"),
      path('register/', views.register, name = "register"),
      path('logout/', views.logout_view, name = "logout"),
      path('addemployee/', views.add_employee, name= "add_employee"),
      path('feedbacks/respond/<int:feedback_id>/', views.reply_feedback, name="reply_feedback"),
      path("translate/", views.translate_page, name="translate_text"),
      path('schemes/', views.scheme_list, name='scheme_list'),
      path('scheme/<int:pk>/', views.scheme_detail, name='scheme_detail'),
      path('schemeadd/', views.scheme_input, name='add_scheme'),
      path('userdetails/', views.user_detail_input, name='user_detail'),
      path('eligibility/<int:pk>/', views.scheme_eligibility, name='user_eligibility'),
      path('check-eligibility/', views.check_all_eligibility, name='check_all_eligibility'),
      path('userdetails/view/', views.view_user_details, name='view_user_details'),
      path('userdetails/edit/', views.edit_user_details, name='edit_user_details'),
      path('scrape/', views.scrape_page, name='scrape_page'),
      path('scrape/run/', views.scrape_schemes_view, name='scrape_schemes'),  # scrape action
      path('apply/', views.apply_scheme, name='apply_scheme'),
      path('apply/success/', views.apply_success, name='apply_success'),
      path('applications/', views.applications_view, name='all_applications'),
      path('applications/<int:app_id>/accept/', views.accept_application, name='accept_application'),
      path('applications/<int:app_id>/reject/', views.reject_application, name='reject_application'),
      path('notifications/mark-read/', views.mark_read, name='mark_read'),
]

