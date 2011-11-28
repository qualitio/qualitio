# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PaymentStrategy'
        db.create_table('payments_paymentstrategy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('verbose_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('users', self.gf('django.db.models.fields.IntegerField')()),
            ('price', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('payments', ['PaymentStrategy'])


    def backwards(self, orm):
        
        # Deleting model 'PaymentStrategy'
        db.delete_table('payments_paymentstrategy')


    models = {
        'payments.paymentstrategy': {
            'Meta': {'object_name': 'PaymentStrategy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'users': ('django.db.models.fields.IntegerField', [], {}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['payments']
