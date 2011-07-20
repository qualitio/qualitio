# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("core", "0002_data_after_0001"),
    )

    def forwards(self, orm):

        # Adding field 'Attachment.project'
        db.add_column('store_attachment', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Adding field 'TestCaseStep.project'
        db.add_column('store_testcasestep', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Adding field 'TestCaseDirectory.project'
        db.add_column('store_testcasedirectory', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Adding field 'TestCaseStatus.project'
        db.add_column('store_testcasestatus', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)

        # Changing field 'TestCaseStatus.name'
        db.alter_column('store_testcasestatus', 'name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        # Adding field 'TestCase.project'
        db.add_column('store_testcase', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Project']), keep_default=False)


    def backwards(self, orm):

        # Deleting field 'Attachment.project'
        db.delete_column('store_attachment', 'project_id')

        # Deleting field 'TestCaseStep.project'
        db.delete_column('store_testcasestep', 'project_id')

        # Deleting field 'TestCaseDirectory.project'
        db.delete_column('store_testcasedirectory', 'project_id')

        # Deleting field 'TestCaseStatus.project'
        db.delete_column('store_testcasestatus', 'project_id')

        # Changing field 'TestCaseStatus.name'
        db.alter_column('store_testcasestatus', 'name', self.gf('django.db.models.fields.TextField')(unique=True))

        # Deleting field 'TestCase.project'
        db.delete_column('store_testcase', 'project_id')


    models = {
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        'store.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'requirement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['require.Requirement']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['store.TestCaseStatus']"})
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
        },
        'store.testcasestep': {
            'Meta': {'ordering': "['sequence']", 'object_name': 'TestCaseStep'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'expected': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'sequence': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'testcase': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': "orm['store.TestCase']"})
        }
    }

    complete_apps = ['store']
