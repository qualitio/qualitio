# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TestCaseDirectory'
        db.create_table('store_testcasedirectory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['store.TestCaseDirectory'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('store', ['TestCaseDirectory'])

        # Adding model 'TestCase'
        db.create_table('store_testcase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('requirement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['require.Requirement'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('precondition', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subchildren', to=orm['store.TestCaseDirectory'])),
        ))
        db.send_create_signal('store', ['TestCase'])

        # Adding model 'TestCaseStep'
        db.create_table('store_testcasestep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('expected', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sequence', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True)),
            ('testcase', self.gf('django.db.models.fields.related.ForeignKey')(related_name='steps', to=orm['store.TestCase'])),
        ))
        db.send_create_signal('store', ['TestCaseStep'])

        # Adding model 'Attachment'
        db.create_table('store_attachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('testcase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['store.TestCase'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('store', ['Attachment'])


    def backwards(self, orm):
        
        # Deleting model 'TestCaseDirectory'
        db.delete_table('store_testcasedirectory')

        # Deleting model 'TestCase'
        db.delete_table('store_testcase')

        # Deleting model 'TestCaseStep'
        db.delete_table('store_testcasestep')

        # Deleting model 'Attachment'
        db.delete_table('store_attachment')


    models = {
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
        'store.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['store.TestCase']"})
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
        },
        'store.testcasestep': {
            'Meta': {'ordering': "['sequence']", 'object_name': 'TestCaseStep'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expected': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['store.TestCase']"})
        }
    }

    complete_apps = ['store']
