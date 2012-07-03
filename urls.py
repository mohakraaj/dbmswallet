from django.conf.urls.defaults import patterns, include, url
#from dbmswallet.wallet import views 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # this is to for media file
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media/'}),
#user authentication    
    url(r'^$', 'dbmswallet.wallet.views.showlogin'),
    url(r'^signup/$', 'dbmswallet.wallet.views.showsignup'),
    url(r'^loginfill/$', 'dbmswallet.wallet.views.loginp'),
    url(r'^signupfill/$', 'dbmswallet.wallet.views.signup'),
#laon management
    url(r'^loanfill/$', 'dbmswallet.wallet.views.loan_caller'),
    url(r'^loan/$', 'dbmswallet.wallet.views.loan'),
    url(r'^loan_display/$', 'dbmswallet.wallet.views.loan_display'),
        
    url(r'^showtransaction/$', 'dbmswallet.wallet.views.transaction_show'),
    url(r'^transaction/$', 'dbmswallet.wallet.views.transaction'),
    
    url(r'^displaytran/$', 'dbmswallet.wallet.views.transaction_display'),
 #budget management
   url(r'^showbudget/$', 'dbmswallet.wallet.views.show_budget'),
    url(r'^budgetset/$', 'dbmswallet.wallet.views.budgetset'),
    url(r'^budget_display/$', 'dbmswallet.wallet.views.budget_display'),
    url(r'^budgetcdata/$', 'dbmswallet.wallet.views.budget_cdata'),
    url(r'^budget_m_display/$', 'dbmswallet.wallet.views.budget_m_display'),
    url(r'^budgetmdata/$', 'dbmswallet.wallet.views.budget_mdata'),
    url(r'^budget_y_display/$', 'dbmswallet.wallet.views.budget_y_display'),
    url(r'^budgetydata/$', 'dbmswallet.wallet.views.budget_ydata'),
    
    url(r'^budgetcheck/$', 'dbmswallet.wallet.views.budget_check'),
    url(r'^check/$','dbmswallet.wallet.views.budget_left',),
#logout
    url(r'^logout/$', 'dbmswallet.wallet.views.logout_view'),
    # url(r'^dbmswallet/', include('dbmswallet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
