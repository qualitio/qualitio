# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from qualitio.glossary.models import Language

class Migration(DataMigration):

    def forwards(self, orm):
        status = orm.TestRunStatus.objects.get_or_create(name="default")[0]
        language = Language.objects.get_or_create(name="default")[0]
        for test_run in orm.TestRun.objects.all():
            test_run.status = status
            test_run.translation = language
            test_run.save()

    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'execute.bug': {
            'Meta': {'unique_together': "(('testcaserun', 'alias'),)", 'object_name': 'Bug'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
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
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['require.Requirement']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['execute.TestCaseRunStatus']"})
        },
        'execute.testcaserunstatus': {
            'Meta': {'object_name': 'TestCaseRunStatus'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'execute.testcasesteprun': {
            'Meta': {'ordering': "['sequence']", 'object_name': 'TestCaseStepRun'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expected': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
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
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['execute.TestRunStatus']"}),
            'translation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['glossary.Language']"})
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
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'execute.testrunstatus': {
            'Meta': {'object_name': 'TestRunStatus'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        'glossary.language': {
            'Meta': {'object_name': 'Language'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        'require.requirement': {
            'Meta': {'unique_together': "(('parent', 'name'),)", 'object_name': 'Requirement'},
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
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'store.testcasestatus': {
            'Meta': {'object_name': 'TestCaseStatus'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['execute']
