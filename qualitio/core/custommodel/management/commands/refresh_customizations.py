#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from subprocess import call
from optparse import make_option

from django.core.management.base import NoArgsCommand
from qualitio import customizations


class BaseCustomizationCommand(NoArgsCommand):
    option_list = list(NoArgsCommand.option_list) + [
        make_option('--no-verbose',
                    action="store_false",
                    dest="verbose",
                    default=True,
                    help="Flag to not print verbose messages. Default's to false."),
        ]

    def customizations_module_path(self):
        return os.path.dirname(os.path.abspath(customizations.__file__))

    def customizations_migrations_dir_path(self):
        return os.path.join(self.customizations_module_path(), 'migrations')

    def migrations_dir_exists(self):
        return os.path.exists(self.customizations_migrations_dir_path())

    def initial_migration_exists(self):
        return os.path.exists(os.path.join(self.customizations_migrations_dir_path(), '0001_initial.py'))

    def print_verbose_msg(self, msg):
        print ""
        print "  %s" % msg
        print ""


class Command(BaseCustomizationCommand):
    help = "The command do the migrations for customizations model"

    def run_schemamigration(self, verbose=True):
        if verbose:
            self.print_verbose_msg("Running schema migration: python manage.py schemamigration customizations --auto")

        try:
            return call(['python', 'manage.py', 'schemamigration', 'customizations', '--auto']) == 0
        except OSError as e:
            return False

    def run_initial_migration(self, verbose=True):
        if verbose:
            self.print_verbose_msg("Running initial schema migration: python manage.py schemamigration customizations --initial")

        try:
            return call(['python', 'manage.py', 'schemamigration', 'customizations', '--initial']) == 0
        except OSError as e:
            return False

    def run_migrate(self, verbose=True):
        if verbose:
            self.print_verbose_msg("Running command: python manage.py migrate")

        return call(['python', 'manage.py', 'migrate'])

    def handle_noargs(self, **options):
        verbose = options.get('verbose')

        if self.migrations_dir_exists() and self.initial_migration_exists():
            execution_was_ok = self.run_schemamigration(verbose=verbose)
        else:
            execution_was_ok = self.run_initial_migration(verbose=verbose)

        if execution_was_ok:
            self.run_migrate(verbose=verbose)
