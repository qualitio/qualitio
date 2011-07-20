# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("store", "0005_auto__add_field_attachment_project__add_field_testcasestep_project__ad"),
        )


    def forwards(self, orm):

        # Adding field 'TestRunStatus.project'
        db.add_column('execute_testrunstatus', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Changing field 'TestRunStatus.name'
        db.alter_column('execute_testrunstatus', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        # Adding field 'TestCaseRun.project'
        db.add_column('execute_testcaserun', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Adding field 'TestCaseRunStatus.project'
        db.add_column('execute_testcaserunstatus', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Changing field 'TestCaseRunStatus.name'
        db.alter_column('execute_testcaserunstatus', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        # Adding field 'Bug.project'
        db.add_column('execute_bug', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Adding field 'TestCaseStepRun.project'
        db.add_column('execute_testcasesteprun', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Adding field 'TestRunDirectory.project'
        db.add_column('execute_testrundirectory', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Adding field 'TestRun.project'
        db.add_column('execute_testrun', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)


    def backwards(self, orm):

        # Deleting field 'TestRunStatus.project'
        db.delete_column('execute_testrunstatus', 'project_id')

        # Changing field 'TestRunStatus.name'
        db.alter_column('execute_testrunstatus', 'name', self.gf('django.db.models.fields.CharField')(max_length=256, unique=True))

        # Deleting field 'TestCaseRun.project'
        db.delete_column('execute_testcaserun', 'project_id')

        # Deleting field 'TestCaseRunStatus.project'
        db.delete_column('execute_testcaserunstatus', 'project_id')

        # Changing field 'TestCaseRunStatus.name'
        db.alter_column('execute_testcaserunstatus', 'name', self.gf('django.db.models.fields.CharField')(max_length=256, unique=True))

        # Deleting field 'Bug.project'
        db.delete_column('execute_bug', 'project_id')

        # Deleting field 'TestCaseStepRun.project'
        db.delete_column('execute_testcasesteprun', 'project_id')

        # Deleting field 'TestRunDirectory.project'
        db.delete_column('execute_testrundirectory', 'project_id')

        # Deleting field 'TestRun.project'
        db.delete_column('execute_testrun', 'project_id')


    models = {
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'execute.bug': {
            'Meta': {'unique_together': "(('testcaserun', 'alias'),)", 'object_name': 'Bug'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'testcaserun': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bugs'", 'to': "orm['execute.TestCaseRun']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'execute.testcaserun': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('parent', 'origin'),)", 'object_name': 'TestCaseRun'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'origin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.TestCase']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'testcases'", 'to': "orm['execute.TestRun']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'precondition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['require.Requirement']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['execute.TestCaseRunStatus']"})
        },
        'execute.testcaserunstatus': {
            'Meta': {'object_name': 'TestCaseRunStatus'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'total': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'execute.testcasesteprun': {
            'Meta': {'ordering': "['sequence']", 'object_name': 'TestCaseStepRun'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expected': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'testcaserun': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['execute.TestCaseRun']"})
        },
        'execute.testrun': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestRun'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subchildren'", 'to': "orm['execute.TestRunDirectory']"}),
            'passrate': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['execute.TestRunStatus']"}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['glossary.Language']"})
        },
        'execute.testrundirectory': {
            'Meta': {'object_name': 'TestRunDirectory'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['execute.TestRunDirectory']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'execute.testrunstatus': {
            'Meta': {'object_name': 'TestRunStatus'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"})
        },
        'glossary.language': {
            'Meta': {'object_name': 'Language'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"})
        },
        'require.requirement': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Requirement'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'blocks'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['require.Requirement']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['require.Requirement']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'release_target': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'store.testcase': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestCase'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subchildren'", 'to': "orm['store.TestCaseDirectory']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'precondition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['require.Requirement']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.TestCaseStatus']"})
        },
        'store.testcasedirectory': {
            'Meta': {'object_name': 'TestCaseDirectory'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['store.TestCaseDirectory']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'store.testcasestatus': {
            'Meta': {'object_name': 'TestCaseStatus'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"})
        }
    }

    complete_apps = ['execute']
