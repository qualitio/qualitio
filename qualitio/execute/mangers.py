from qualitio import core

class TestCaseRunManager(core.BaseManager):
    select_related_fields = core.BaseManager.select_related_fields + ['status',
                                                                      'requirement',
                                                                      'origin']

    def passrate(self):
        passed = self.filter(status__passed=True).count()
        total = self.filter(status__total=True).count()
        return round(float(passed)/float(total) * 100,2)

