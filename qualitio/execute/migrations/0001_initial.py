# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TestRunDirectory'
        db.create_table('execute_testrundirectory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['execute.TestRunDirectory'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('execute', ['TestRunDirectory'])

        # Adding model 'TestRun'
        db.create_table('execute_testrun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subchildren', to=orm['execute.TestRunDirectory'])),
        ))
        db.send_create_signal('execute', ['TestRun'])

        # Adding model 'TestCaseRun'
        db.create_table('execute_testcaserun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('requirement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['require.Requirement'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('precondition', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('origin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.TestCase'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['execute.TestCaseRunStatus'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='testcases', to=orm['execute.TestRun'])),
        ))
        db.send_create_signal('execute', ['TestCaseRun'])

        # Adding unique constraint on 'TestCaseRun', fields ['parent', 'origin']
        db.create_unique('execute_testcaserun', ['parent_id', 'origin_id'])

        # Adding model 'TestCaseStepRun'
        db.create_table('execute_testcasesteprun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('expected', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('testcaserun', self.gf('django.db.models.fields.related.ForeignKey')(related_name='steps', to=orm['execute.TestCaseRun'])),
        ))
        db.send_create_signal('execute', ['TestCaseStepRun'])

        # Adding model 'TestCaseRunStatus'
        db.create_table('execute_testcaserunstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=7, blank=True)),
        ))
        db.send_create_signal('execute', ['TestCaseRunStatus'])

        # Adding model 'Bug'
        db.create_table('execute_bug', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('testcaserun', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bugs', to=orm['execute.TestCaseRun'])),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('resolution', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
        ))
        db.send_create_signal('execute', ['Bug'])

        # Adding unique constraint on 'Bug', fields ['testcaserun', 'alias']
        db.create_unique('execute_bug', ['testcaserun_id', 'alias'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Bug', fields ['testcaserun', 'alias']
        db.delete_unique('execute_bug', ['testcaserun_id', 'alias'])

        # Removing unique constraint on 'TestCaseRun', fields ['parent', 'origin']
        db.delete_unique('execute_testcaserun', ['parent_id', 'origin_id'])

        # Deleting model 'TestRunDirectory'
        db.delete_table('execute_testrundirectory')

        # Deleting model 'TestRun'
        db.delete_table('execute_testrun')

        # Deleting model 'TestCaseRun'
        db.delete_table('execute_testcaserun')

        # Deleting model 'TestCaseStepRun'
        db.delete_table('execute_testcasesteprun')

        # Deleting model 'TestCaseRunStatus'
        db.delete_table('execute_testcaserunstatus')

        # Deleting model 'Bug'
        db.delete_table('execute_bug')


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
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['execute.TestCaseRunStatus']"})
        },
        'execute.testcaserunstatus': {
            'Meta': {'object_name': 'TestCaseRunStatus'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'})
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
            'path': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'})
        },
        'execute.testrundirectory': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestRunDirectory'},
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
        'require.requirement': {
            'Meta': {'ordering': "['name']", 'object_name': 'Requirement'},
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
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['require.Requirement']", 'null': 'True', 'blank': 'True'})
        },
        'store.testcasedirectory': {
            'Meta': {'ordering': "['name']", 'object_name': 'TestCaseDirectory'},
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
        }
    }

    complete_apps = ['execute']
