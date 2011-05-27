# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Requirement'
        db.create_table('require_requirement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['require.Requirement'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('release_target', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('require', ['Requirement'])

        # Adding M2M table for field dependencies on 'Requirement'
        db.create_table('require_requirement_dependencies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_requirement', models.ForeignKey(orm['require.requirement'], null=False)),
            ('to_requirement', models.ForeignKey(orm['require.requirement'], null=False))
        ))
        db.create_unique('require_requirement_dependencies', ['from_requirement_id', 'to_requirement_id'])


    def backwards(self, orm):
        
        # Deleting model 'Requirement'
        db.delete_table('require_requirement')

        # Removing M2M table for field dependencies on 'Requirement'
        db.delete_table('require_requirement_dependencies')


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
        }
    }

    complete_apps = ['require']
