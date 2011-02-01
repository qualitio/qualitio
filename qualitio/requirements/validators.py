# -*- coding: utf-8 -*-
# external library "networkX" to operate on graphs
import networkx as nx
import warnings

from django.core.exceptions import ValidationError


# TODO: no test for this class
class RequirementDependencyValidator(object):
    """
    IMPORTANT! This is NOT standard django validator.

    This class provides ability to analize dependency (directed) graph
    for EXISTING requirement and list of it's dependencies.

    Responsibility:
      1) check's if there is cycle in the graph

        validator = RequirementDependencyValidator(requirement_object, [<some dependent requirement objects>])
        if validator.is_valid():
            print "No cycles"
        else:
            print "Adding dependencies will make dependency cycles"


      2) blaming dependencies which causes the cycle

        validator = RequirementDependencyValidator(requirement_object, [<some dependent requirement objects>])
        if not validator.is_valid():
            dependency_objects_that_causes_cycles = validator.blame_dependencies()


      3) getting cycles which were caused by requirement_object and its dependent requirements

        validator = RequirementDependencyValidator(requirement_object, [<some dependent requirement objects>])
        if not validator.is_valid():
            cycles = validator.get_cycles() # cycle is a list that contains lists with cycles


    RequirementDependencyValidator was created to check if the_dependencies_list would cause
    cycle when the gived requirement object will be saved.

    IT IGNORES SITUATION when there's already some cycles in dependency graph (just the warning is raised).
    """

    def __init__(self, requirement, dependencies=None, edges=None):
        self.requirement = requirement
        self.dependencies = dict((d.id, d) for d in dependencies or [])

        self.edges = edges
        if not self.edges:
            # to avoid circular imports
            from requirements.models import Requirement
            self.edges = Requirement.objects.get_dependency_graph_edges()

    def _complete_dependency_connections(self, potentialy_new_dependencies_ids):
        # We don't know if user totaly changed dependency or just add one
        # so we try to add dependency connections from those which
        # user of Requirement want to save
        dependency_connections = list(self.edges)
        for d_id in potentialy_new_dependencies_ids:
            candidate = (self.requirement.id, d_id)
            if candidate not in dependency_connections:
                dependency_connections.append(candidate)
        return dependency_connections

    def _build_dependency_graph(self):
        # Creates dependency graph.
        # Returns None if there's no dependencies.
        dependency_connections = self._complete_dependency_connections(self.dependencies.keys())
        graph = None

        if dependency_connections:
            graph = nx.DiGraph()
            for a1, a2 in dependency_connections:
                graph.add_edge(a1, a2)

        return graph

    def _is_ready(self):
        return hasattr(self, '_cycles')

    def _check_if_is_ready(self):
        if not self._is_ready():
            methods = ['get_cycles', 'blame_dependencies', 'format_error_msg']
            msg = u"To use one of %s methods you need to invoke 'is_valid' method first."
            raise AttributeError(msg % unicode(methods))
        return self

    def is_valid(self):
        """
        Check if dependency graph has cycles
        """
        if not self._is_ready():
            graph = self._build_dependency_graph()
            self._is_valid = True
            self._cycles = []
            if graph:
                self._cycles = nx.simple_cycles(graph)
                self._is_valid = bool(self._cycles)
        return self._is_valid

    def blame_dependencies(self):
        # TODO: explain this method!
        self._check_if_is_ready()

        nodes = {}
        dependencies_ids = set(self.dependencies.keys())

        for cycle in self._cycles:
            dependencies_ids_that_makes_cycles = list(set(cycle) & dependencies_ids)

            if not dependencies_ids_that_makes_cycles:
                # TODO: discuss what we should do here
                warnings.warn("Graph have already had cycle! Founded while analizing %s" % self.requirement)
                continue

            requirement_id = dependencies_ids_that_makes_cycles[0]
            if requirement_id not in nodes:
                nodes[requirement_id] = self.dependencies[requirement_id]
        return nodes.values()

    def get_cycles(self):
        self._check_if_is_ready()
        return self._cycles

    def format_error_msg(self):
        names = u', '.join("%s(id=%s)" % (r.name, r.id) for r in self.blame_dependencies())
        return u"You cannot set %s as dependency because it produces cycle." % names
