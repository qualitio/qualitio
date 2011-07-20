# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Word'
        db.create_table('glossary_word', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'])),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('glossary', ['Word'])

        # Adding model 'Language'
        db.create_table('glossary_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'])),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('glossary', ['Language'])

        # Adding model 'Representation'
        db.create_table('glossary_representation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'])),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['glossary.Word'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['glossary.Language'])),
            ('representation', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
        ))
        db.send_create_signal('glossary', ['Representation'])

        # Adding unique constraint on 'Representation', fields ['word', 'language']
        db.create_unique('glossary_representation', ['word_id', 'language_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Representation', fields ['word', 'language']
        db.delete_unique('glossary_representation', ['word_id', 'language_id'])

        # Deleting model 'Word'
        db.delete_table('glossary_word')

        # Deleting model 'Language'
        db.delete_table('glossary_language')

        # Deleting model 'Representation'
        db.delete_table('glossary_representation')


    models = {
        'core.project': {
            'Meta': {'object_name': 'Project'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'glossary.language': {
            'Meta': {'object_name': 'Language'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"})
        },
        'glossary.representation': {
            'Meta': {'unique_together': "(('word', 'language'),)", 'object_name': 'Representation'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['glossary.Language']"}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"}),
            'representation': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['glossary.Word']"})
        },
        'glossary.word': {
            'Meta': {'object_name': 'Word'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Project']"})
        }
    }

    complete_apps = ['glossary']
