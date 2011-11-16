# -*- coding: utf-8 -*-
from django.db.models import query
from django.db import connection
from qualitio import core


class RequirementManager(core.BasePathManager):
    def get_query_set(self):
        return super(RequirementManager, self).get_query_set().select_related(*self.select_related_fields)

    def exclude_potential_cycles(self, requirement):
        qs = self.exclude(pk=requirement.pk)
        qs = qs.exclude(dependencies__in=[requirement])
        # TODO: maybe it's the good idea to exclude more "dependencies of dependencies"
        #       eg:
        #       qs = qs.exclude(dependencies__dependencies__in=[requirement])
        #       qs = qs.exclude(dependencies__dependencies__dependencies__in=[requirement]) etc...
        return qs

    def get_dependency_graph_edges(self):
        """
        Returns all dependency connections as a list of pairs (tuples).
        """
        query = "SELECT from_requirement_id, to_requirement_id FROM require_requirement_dependencies;"
        cursor = connection.cursor()
        cursor.execute(query)
        result = list(row for row in cursor.fetchall())
        cursor.close()
        return result
