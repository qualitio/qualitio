from qualitio import core

class TestCaseRunManager(core.BasePathManager):
    select_related_fields = core.BasePathManager.select_related_fields + ['status',
                                                                      'requirement',
                                                                      'origin']

    def passrate(self):
        passed = self.filter(status__passed=True).count()
        total = self.filter(status__total=True).count()

        if not total:
            return 0

        return round(float(passed)/float(total) * 100,2)

