from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from qualitio.core.utils import json_response, success, failed

from qualitio.report.models import ReportDirectory, Report
from qualitio.report.forms import ReportDirectoryForm, ReportForm, ContextElementFormset
from qualitio.report.validators import ReportValidator


def index(request):
    return direct_to_template(request, 'report/base.html', {})

def directory_details(request, directory_id):
    return direct_to_template(request, 'report/reportdirectory_details.html',
                              {'directory': ReportDirectory.objects.get(pk=directory_id)})

@permission_required('report.add_reportdirectory', login_url='/permission_required/')
def directory_new(request, directory_id):
    directory = ReportDirectory.objects.get(pk=directory_id)
    reportdirectory_form = ReportDirectoryForm(initial={'parent': directory})

    return direct_to_template(request, 'report/reportdirectory_edit.html',
                              {'reportdirectory_form': reportdirectory_form})

@permission_required('report.change_reportdirectory', login_url='/permission_required/')
def directory_edit(request, directory_id):
    directory = ReportDirectory.objects.get(pk=directory_id)
    reportdirectory_form = ReportDirectoryForm(instance=directory)
    return direct_to_template(request, 'report/reportdirectory_edit.html',
                              {'reportdirectory_form': reportdirectory_form})

@json_response
def directory_valid(request, directory_id=0):
    # TODO: should we think about permissions for valid views?
    if directory_id:
        reportdirectory = ReportDirectory.objects.get(pk=directory_id)
        reportdirectory_form = ReportDirectoryForm(request.POST,
                                                   instance=reportdirectory)
    else:
        reportdirectory_form = ReportDirectoryForm(request.POST)


    if reportdirectory_form.is_valid():
        reportdirectory = reportdirectory_form.save()

        # log = history.History(request.user, report_directory)
        # log.add_form(report_directory_form)
        # log.save()

        return success(message='report directory saved',
                       data={"parent_id": getattr(reportdirectory.parent, "id", 0),
                             "current_id": reportdirectory.id})
    else:
        return failed(message="Validation errors: %s" % reportdirectory_form.error_message(),
                      data=reportdirectory_form.errors_list())


def report_details(request, report_id):
    report = Report.objects.get(pk=report_id)
    if report.is_html():
        content = report.content
        styles = None
    else:
        from pygments.lexers import XmlLexer, JavascriptLexer, TextLexer
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from django.utils.safestring import mark_safe

        lexers = {"application/xml": XmlLexer(),
                  "application/json": JavascriptLexer(),
                  "text/plain" : TextLexer() }

        formatter = HtmlFormatter(linenos=True)
        content = mark_safe(highlight(report.content, lexers[report.mime], formatter))
        styles = formatter.get_style_defs('.highlight')

    return direct_to_template(request, 'report/report_details.html',
                              {'report': report,
                               'content' : content,
                               'styles' : styles})


@permission_required('report.add_report', login_url='/permission_required/')
def report_new(request, directory_id):
    directory = ReportDirectory.objects.get(pk=directory_id)
    report_form = ReportForm(initial={'parent': directory})
    report_contextelement_formset = ContextElementFormset()
    return direct_to_template(request, 'report/report_edit.html',
                              {"report_form": report_form,
                               "report_contextelement_formset": report_contextelement_formset})


@permission_required('report.change_report', login_url='/permission_required/')
def report_edit(request, report_id):
    report = Report.objects.get(pk=report_id)
    report_form = ReportForm(instance=report)
    report_contextelement_formset = ContextElementFormset(instance=report)
    return direct_to_template(request, 'report/report_edit.html',
                              {'report_form': report_form,
                               "report_contextelement_formset": report_contextelement_formset})

@json_response
def report_valid(request, report_id=0):
    if report_id:
        report = Report.objects.get(pk=str(report_id))
        report_form = ReportForm(request.POST, instance=report)
        report_contextelement_formset = ContextElementFormset(request.POST, instance=report)
    else:
        report_form = ReportForm(request.POST)
        report_contextelement_formset = ContextElementFormset(request.POST)

    errors = {}

    if report_form.is_valid() and report_contextelement_formset.is_valid():
        validator = ReportValidator(report_form.cleaned_data['template'],
                                    report_contextelement_formset.get_context())
        if validator.raport_is_valid():
            report = report_form.save()
            report_contextelement_formset.instance = report
            report_contextelement_formset.save(queries=validator.queries)
            # TODO: the history should be updated here I guess
            return success(message='report saved',
                           data={"parent_id": getattr(report.parent, "id", 0),
                                 "current_id": report.id,
                                 "link": report.link})
        else:
            errors.update(validator.errors)

    errors = report_form.errors_list(additional=errors.items())
    errors.extend(report_contextelement_formset._errors_list())
    return failed(message="Validation errors: %s" % report_form.error_message(),
                  data=errors)


def report_external(request, report_id):
    report = get_object_or_404(Report, pk=report_id)

    if not report.public and not request.user.is_authenticated():
        return HttpResponseRedirect("%s?next=/report/external/%s"
                                    % (reverse('django.contrib.auth.views.login'),
                                       report.link))

    if report.is_html():
        return direct_to_template(request, 'report/report_external.html',
                                  {'report': report})

    return HttpResponse(report.content,
                        content_type=report.mime)
