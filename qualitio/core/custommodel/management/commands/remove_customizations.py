#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import inspect
from operator import itemgetter, attrgetter
from subprocess import call
from optparse import make_option

from django.db import connection, transaction
from qualitio import customizations
from qualitio.core.custommodel.models import ModelCustomization
from qualitio.core.custommodel.management.commands.refresh_customizations import BaseCustomizationCommand
from south.models import MigrationHistory


CONFIRMATION = """
  Are you really sure you want to delete all information about customizations?
  Here is a list of changes:
    * all customization migrations will be removed (customizations/migrations/ directory),
    * migration history of customizations module from database will be removed,
    * tables of all customizations models will be droped.
  Are you sure you want to run? (y/n): """


class Command(BaseCustomizationCommand):
    option_list = list(BaseCustomizationCommand.option_list) + [  # verbose option is already there
        make_option('--no-interactive',
                    action="store_false",
                    dest="interactive",
                    default=True,
                    help="No interactive mode. Use it only if you know what you are doing."),
        ]
    help = "Remove all customizations."

    def remove_customizations_migrations_directory(self, verbose=True):
        if verbose:
            self.print_verbose_msg("Deleting qualitio/customizations/migration directory.")

        try:
            return call(['rm', '-rf', self.customizations_migrations_dir_path()]) == 0
        except OSError as e:
            return False

    def remove_history_of_customizations_migrations_from_database(self, verbose=True):
        if verbose:
            self.print_verbose_msg("Deleting history of customizations migrations from database.")

        MigrationHistory.objects.filter(app_name='customizations').delete()

    def _filter_customization_models(self):

        def predicate(tuple_info):  # inspect.getmembers returns list of (name, classinfo) tuples
            name, cls = tuple_info
            return inspect.isclass(cls) and issubclass(cls, ModelCustomization) and cls is not ModelCustomization

        # here we want only classinfo objects
        return map(itemgetter(1), filter(predicate, inspect.getmembers(customizations.models)))

    def _get_customization_models_table_names(self):
        return map(attrgetter('_meta.db_table'), self._filter_customization_models())

    def drop_customizations_tables(self, verbose=True):
        if verbose:
            self.print_verbose_msg("Droping tables")

        cursor = connection.cursor()
        for table in  self._get_customization_models_table_names():
            cursor.execute('DROP TABLE %s;' % table)
        transaction.commit_unless_managed()

    def handle_noargs(self, **options):
        verbose = options.get('verbose')

        if options.get('interactive'):
            answer = raw_input(CONFIRMATION)

            while answer not in ['y', 'n']:
                answer = raw_input("  choose 'y'(yes) or 'n'(no): ")

            if answer is not 'y':
                return

        self.remove_customizations_migrations_directory(verbose=verbose)
        self.remove_history_of_customizations_migrations_from_database(verbose=verbose)
        self.drop_customizations_tables(verbose=verbose)
