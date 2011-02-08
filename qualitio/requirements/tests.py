from nose.tools import *

from django.test import TestCase
from django.core.exceptions import ValidationError

from qualitio.requirements.models import Requirement
from qualitio.requirements.forms import RequirementForm



class DependencyTestCase(TestCase):
    """
    Dependency Test Case separate base class which gives us
    simple, well defined dependencies graph for test cases
    that checks requirement with dependencies behaviour.

    Graph:

    BigProject -> []
    MeeGo      -> [BigProject]
    IVI        -> [MeeGo, TV]
    TV         -> [MeeGo, Notebook]
    TV2        -> [MeeGo, Notebook]
    Notebook   -> [MeeGo]
    Toster     -> [IVI]
    Flashlight -> [Toster]
    """
    def setUp(self):
        mgr = Requirement.objects

        self.big_project = mgr.get(name="BigProject")  # assumes we've got it in fixtures !
        self.mee_go = mgr.create(name="MeeGo")
        self.mee_go_IVI = mgr.create(name="IVI")
        self.mee_go_TV = mgr.create(name="TV")
        self.mee_go_TV2 = mgr.create(name="TV2")
        self.mee_go_Notebook = mgr.create(name="Notebook")
        self.toster = mgr.create(name="Toster")
        self.flashlight = mgr.create(name="Flashlight")

        self.mee_go.dependencies.add(self.big_project)
        self.mee_go.save()

        self.mee_go_IVI.dependencies.add(self.mee_go)
        self.mee_go_IVI.dependencies.add(self.mee_go_TV)
        self.mee_go_IVI.save()

        self.mee_go_TV.dependencies.add(self.mee_go)
        self.mee_go_TV.dependencies.add(self.mee_go_Notebook)
        self.mee_go_TV.save()

        self.mee_go_TV2.dependencies.add(self.mee_go)
        self.mee_go_TV2.dependencies.add(self.mee_go_Notebook)
        self.mee_go_TV2.save()

        self.mee_go_Notebook.dependencies.add(self.mee_go)
        self.mee_go_Notebook.save()

        self.toster.dependencies.add(self.mee_go_IVI)
        self.toster.save()

        self.flashlight.dependencies.add(self.toster)
        self.flashlight.save()



class RequirementDependenciesOnModelTest(DependencyTestCase):
    def add_cycle_dependency(self):
        self.mee_go_Notebook.dependencies.add(self.mee_go_IVI)


    @raises(ValidationError)
    def test_requirements_dependency_cycle_check_on_save(self):
        self.add_cycle_dependency()
        self.mee_go_Notebook.save()


    def test_ability_to_avoid_dependency_graph_validation(self):
        self.add_cycle_dependency()
        try:
            self.mee_go_Notebook.save(clean_dependencies=False)
        except ValidationError, e:
            self.fail("The exception shouldn't be raised!")


    @raises(ValidationError)
    def test_full_clean_validates_dependencies(self):
        self.add_cycle_dependency()
        self.mee_go_Notebook.full_clean()


    def test_ability_to_avoid_full_clean_dependencies(self):
        self.add_cycle_dependency()
        try:
            self.mee_go_Notebook.full_clean(clean_dependencies=False)
        except ValidationError, e:
            self.fail("The exception shouldn't be raised!")


    def test_can_check_dependencies_before_save(self):
        try:
            self.mee_go_Notebook.clean_dependencies([self.mee_go_IVI])
        except ValidationError, e:
            pass
        else:
            self.fail("clean_dependencies method should raise error")

        dependencies = [d.id for d in self.mee_go_Notebook.dependencies.all()]
        assert_true(self.mee_go_IVI.id not in dependencies)


    @raises(ValidationError)
    def test_trying_to_add_new_dependencies_that_would_make_two_cycles(self):
        self.mee_go_Notebook.dependencies.add(self.mee_go_IVI)
        self.mee_go_Notebook.dependencies.add(self.flashlight)
        self.mee_go_Notebook.save()



class RequirementFormTest(DependencyTestCase):
    def configure_form_with_direct_cycle_dependency(self):
        data = {'dependencies': [self.mee_go.id, self.mee_go_TV.id]}
        return RequirementForm(data, instance=self.mee_go_Notebook)

    def configure_form_with_dependency_cycle(self):
        data = {'dependencies': [self.mee_go.id, self.flashlight.id]}
        return RequirementForm(data, instance=self.mee_go_Notebook)


    def test_dependencies_that_make_DIRECT_cycle_are_not_avaiable_for_users_form_select(self):
        form = self.configure_form_with_direct_cycle_dependency()

        avaiable_dependencies = [r.id for r in form.fields['dependencies'].queryset.all()]
        assert_true(self.mee_go_TV.id not in avaiable_dependencies)


    def test_trying_to_add_direct_cycle_via_form_causes_an_dependencies_validation_error(self):
        form = self.configure_form_with_direct_cycle_dependency()

        assert_false(form.is_valid())
        assert_true('dependencies' in form.errors)

        dependencies_errors_list = form.errors['dependencies']
        assert_equals(len(dependencies_errors_list), 1)

        first_error_msg = dependencies_errors_list[0]
        assert_true(first_error_msg.startswith('Select a valid choice.'))


    def test_cycles_are_discover_and_causes_validation_error(self):
        form = self.configure_form_with_dependency_cycle()

        assert_false(form.is_valid())
        assert_true('dependencies' in form.errors)

        dependencies_errors_list = form.errors['dependencies']
        assert_equals(len(dependencies_errors_list), 1)

        first_error_msg = dependencies_errors_list[0]
        assert_true(first_error_msg.startswith('You cannot set '))


    def new_requirement_form_data(self):
        return {
            'parent': self.mee_go_Notebook.id,
            'dependencies': [self.mee_go.id, self.flashlight.id],
            'name': 'TestRequirement',
            }


    def configure_form_for_new_requirement_object(self):
        data = self.new_requirement_form_data()
        return RequirementForm(data)


    def test_new_requirement_form(self):
        form = self.configure_form_for_new_requirement_object()
        assert_true(form.is_valid())

        requirement = form.save()
        assert_equals(len(requirement.dependencies.all()), 2)



class OnlyOneRequirementInDBTest(TestCase):
    def setUp(self):
        self.big_project = Requirement.objects.get(name="BigProject")  # assumes we've got it in fixtures !


    def test_no_error_on_save(self):
        assert_equals(Requirement.objects.count(), 1)

        self.big_project.name = "BIG PROJECT"
        try:
            self.big_project.save()
        except ValidationError, e:
            self.fail("The exception shouldn't be raised!")


    def configure_form(self):
        data = {'name': 'BIG PROJECT'}
        return RequirementForm(data, instance=self.big_project)


    def test_no_error_on_form_save(self):
        form = self.configure_form()
        assert_true(form.is_valid())
        try:
            form.save()
        except ValidationError, e:
            self.fail("The exception shouldn't be raised!")
