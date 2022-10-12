from django.contrib import admin
from django.urls import path
from workStation import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='inicio'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/add/', views.add_user, name='user-create'),
    path('users/<int:pk>/update/', views.update_user, name='user-update'),
    path('users/<int:pk>/delete/', views.delete_user, name='user-delete'),
    path('change-your-pass/<int:pk>/', views.change_your_password, name='change-your-pass'),
    path('change-my-pass/', views.change_my_password, name='change-my-pass'),
    path('active-deactivate-user/<int:pk>/', views.active_deactivate_user, name='active-deactivate-user'),
    path('sign-up/', views.register, name='sign_up'),
    path('sign-in/', views.SignInView.as_view(), name='sign_in'),
    path('sign-out/', views.SignOutView.as_view(), name='sign_out'),
    #path('password-change/', views.password_change, name='password_change'),
#     path('password_change/done/', views [name='password_change_done']
# ^accounts/password_reset/done/$ [name='password_reset_done']
# ^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
# ^accounts/reset/done/$ [name='password_reset_complete']
#     path('password_reset/', views.logear, name='password-reset'),
    path('helps/', views.HelpsView.as_view(), name='helps'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('evidences/<int:pk>/', views.EvidencesView.as_view(), name='evidences'),
    path('evidence/<int:pk>/<int:pq>/confirm/', views.EvidenceAskDelete.as_view(), name='evidence-delete-confirm'),
    path('evidence/<int:pk>/<int:pq>/delete/', views.evidence_delete, name='evidence-delete'),
    path('evidence/<int:pk>/create/', views.evidence_create, name='evidence-create'),
    path('evidence/<int:pk>/<int:pq>/update/', views.evidence_update, name='evidence-update'),
    path('studies/', views.StudyListView.as_view(), name='studies'),
    path('study/<int:pk>/', views.study_detail, name='study-details'),
    path('study/add/', views.study_create, name='study-add'),
    path('study/<int:pk>/update/', views.study_update, name='study-update'),
    path('study/<int:pk>/delete/', views.StudyDeleteView.as_view(), name='study-delete'),
    path('study-report/<int:pk>/', views.study_report_PDF, name='study-report'),
    path('study-export/<int:pk>/', views.study_export, name='study-export'),
    path('input-files/', views.input_files, name='input-files'),
    path('input-variables/', views.input_variables, name='input-variables'),
    path('studies/<int:pk>/', views.StudiesByInvestigator.as_view(), name='studies-investigator'),
    path('investigators/', views.InvestigatorListView.as_view(), name='investigators'),
    path('investigators/<int:pk>/', views.InvestigatorDetailView.as_view(), name='investigator-details'),
    path('investigators/add/', views.InvestigatorCreateView.as_view(), name='investigator-add'),
    path('investigators-admin/add/', views.InvestigatorAdminCreateView.as_view(), name='investigator-admin-add'),
    path('investigators/<int:pk>/update/', views.InvestigatorUpdateView.as_view(), name='investigator-update'),
    path('investigators/<int:pk>/delete/', views.InvestigatorDeleteView.as_view(), name='investigator-delete'),
    path('investigator-report/<int:pk>/', views.investigator_report_PDF, name='investigator-report')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
