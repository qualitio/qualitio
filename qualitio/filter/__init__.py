"""
Application that allows filtering tables on fly.
Just add filter.views.filter view to your urlpatters:


from filter import views
urlpatters = patterns(''
                      (r'filter/', views.filter, {'model': MyModel}),
                      )


This will generate django_filter.FilterSet instance for the given model
and will pass it into 'filter/filter.html' template.
"""
