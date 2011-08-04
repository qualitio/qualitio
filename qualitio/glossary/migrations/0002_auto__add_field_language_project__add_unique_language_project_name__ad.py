# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    depends_on = (
        ("projects", "0001_initial"),
    )

    def forwards(self, orm):

        # Adding field 'Language.project'
        db.add_column('glossary_language', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.Project']), keep_default=False)

        # Adding unique constraint on 'Language', fields ['project', 'name']
        db.create_unique('glossary_language', ['project_id', 'name'])

        # Adding field 'Representation.project'
        db.add_column('glossary_representation', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.Project']), keep_default=False)

        # Adding field 'Word.project'
        db.add_column('glossary_word', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['projects.Project']), keep_default=False)


    def backwards(self, orm):

        # Removing unique constraint on 'Language', fields ['project', 'name']
        db.delete_unique('glossary_language', ['project_id', 'name'])

        # Deleting field 'Language.project'
        db.delete_column('glossary_language', 'project_id')

        # Deleting field 'Representation.project'
        db.delete_column('glossary_representation', 'project_id')

        # Deleting field 'Word.project'
        db.delete_column('glossary_word', 'project_id')


    models = {
        'glossary.language': {
            'Meta': {'unique_together': "(('project', 'name'),)", 'object_name': 'Language'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"})
        },
        'glossary.representation': {
            'Meta': {'unique_together': "(('word', 'language'),)", 'object_name': 'Representation'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['glossary.Language']"}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"}),
            'representation': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['glossary.Word']"})
        },
        'glossary.word': {
            'Meta': {'object_name': 'Word'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['projects.Project']"})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project'},
            'created_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['glossary']
