from django import template
from qualitio.execute.models import TestCaseRunStatus
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('execute/_passrate.html')
def passrate(testrun):
    testcaseruns_count = testrun.testcases.count()
    passrate = TestCaseRunStatus.objects.filter(testcaserun__parent=testrun).annotate(count=Count('testcaserun'))
    for status in passrate:
        status.ratio = float(status.count) / float(testcaseruns_count) * 100

    return {"passrate": passrate,
            "testrun": testrun}
