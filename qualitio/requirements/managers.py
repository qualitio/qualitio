# -*- coding: utf-8 -*-
from django.db.models import Manager
from django.db.models import query
from django.db import connection


class QuerySet(query.QuerySet):
    def exclude_potential_cycles(self, requirement):
        qs = self.exclude(pk=requirement.pk)
        qs = qs.exclude(dependencies__in=[requirement])
        # TODO: maybe it's the good idea to exclude more "dependencies of dependencies"
        #       eg:
        #       qs = qs.exclude(dependencies__dependencies__in=[requirement])
        #       qs = qs.exclude(dependencies__dependencies__dependencies__in=[requirement]) etc...
        return qs


class RequirementManager(Manager):
    def get_query_set(self):
        return QuerySet(model=self.model, using=self._db)

    def exclude_potential_cycles(self, requirement):
        return self.get_query_set().exclude_potential_cycles(requirement)

    def get_dependency_graph_edges(self):
        """
        Returns all dependency connections as a list of pairs (tuples).
        """
        query = "SELECT from_requirement_id, to_requirement_id FROM requirements_requirement_dependencies;"
        cursor = connection.cursor()
        cursor.execute(query)
        result = list(row for row in cursor.fetchall())
        cursor.close()
        return result
