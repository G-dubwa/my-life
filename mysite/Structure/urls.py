from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("life",views.my_life,name="life"),
    path("options",views.options, name='options'),
    path("life/add_priority", views.add_priority, name="add_priority"),
    path("life/add_element/<int:priority_id>", views.add_element, name="add_element"),
    path("life/add_aspect/<int:priority_id>/<int:element_id>", views.add_aspect, name="add_aspect"),
    path("life/edit_priority/<int:priority_id>", views.edit_priority, name="edit_priority"),
    path("life/edit_element/<int:priority_id>/<int:element_id>", views.edit_element, name="edit_element"),
    path("life/edit_aspect/<int:priority_id>/<int:element_id>/<int:aspect_id>", views.edit_aspect, name="edit_aspect"),
    path("life/priority/<int:priority_id>", views.priority, name='priority'),
    path("life/element/<int:priority_id>/<int:element_id>", views.element, name='element'),
    path("life/aspect/<int:priority_id>/<int:element_id>/<int:aspect_id>", views.aspect, name='aspect'),
    path("life/delete/<int:priority_id>/<int:delete>", views.delete_priority, name='delete_priority'),
    path("life/delete/<int:priority_id>/<int:element_id>/<int:delete>", views.delete_element, name='delete_element'),
    path("life/delete/<int:priority_id>/<int:element_id>/<int:aspect_id>/<int:delete>", views.delete_aspect, name='delete_aspect'),
    path('activate-user/<uidb64>/<token>',views.activate_user,name='activate'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='Structure/change-password.html',
            success_url = '/'
        ),
    
        name='change_password'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='Structure/password-reset/password_reset_form.html',
             subject_template_name='Structure/password-reset/password_reset_subject.txt',
             email_template_name='Structure/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='Structure/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='Structure/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='Structure/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path("change-email/", views.change_email, name="change_email"),
    path('change-email/<uidb64>/<token>/<email>',views.email_reset, name='email_reset'),

    path('financial/<int:entity_id>',views.entity, name='entity'),
    path("financial/<int:entity_id>/<int:finaspect_id>", views.finaspect, name='finaspect'),
    path("financial/<int:entity_id>/<int:finaspect_id>/<int:update_id>", views.update, name='update'),
    path("financial/add-entity", views.add_entity, name="add_entity"),
    path("financial/add-finaspect/<int:entity_id>", views.add_finaspect, name="add_finaspect"),
    path("financial/add-update/<int:entity_id>/<int:finaspect_id>", views.add_update, name="add_update"),
    path("financial/edit-entity/<int:entity_id>", views.edit_entity, name="edit_entity"),
    path("financial/edit-finaspect/<int:entity_id>/<int:finaspect_id>",views.edit_finaspect, name="edit_finaspect"),
    path("financial/edit-update/<int:entity_id>/<int:finaspect_id>/<int:update_id>", views.edit_update, name="edit_update"),
    path("financial/delete/<int:entity_id>/<int:delete>", views.delete_entity, name='delete_entity'),
    path("financial/delete/<int:entity_id>/<int:finaspect_id>/<int:delete>", views.delete_finaspect, name='delete_finaspect'),
    path("financial/delete/<int:entity_id>/<int:finaspect_id>/<int:update_id>/<int:delete>", views.delete_update, name='delete_update'),
    path('event/<int:event_id>',views.event, name='event'),
    path("event/delete/<int:event_id>/<int:delete>", views.delete_event, name='delete_event'),
    path("event/edit-event/<int:event_id>", views.edit_event, name="edit_event"),
    path("event/add-event", views.add_event, name="add_event"),
]
