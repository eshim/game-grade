# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserID'
        db.create_table(u'submissions_userid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'submissions', ['UserID'])

        # Adding model 'Task'
        db.create_table(u'submissions_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=' ', max_length=200)),
            ('fileName', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('descrip', self.gf('django.db.models.fields.TextField')()),
            ('xpVal', self.gf('django.db.models.fields.IntegerField')()),
            ('openTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('closeTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'submissions', ['Task'])

        # Adding model 'Exercise'
        db.create_table(u'submissions_exercise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Task'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('descrip', self.gf('django.db.models.fields.TextField')()),
            ('xpVal', self.gf('django.db.models.fields.IntegerField')()),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'submissions', ['Exercise'])

        # Adding model 'Upload'
        db.create_table(u'submissions_upload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fileUpload', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('userID', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submissions.Task'])),
            ('uploadTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('mostRecent', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('uploadURL', self.gf('django.db.models.fields.URLField')(default=' ', max_length=200)),
        ))
        db.send_create_signal(u'submissions', ['Upload'])

        # Adding model 'UnitTest'
        db.create_table(u'submissions_unittest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'submissions', ['UnitTest'])

        # Adding M2M table for field tasks on 'UnitTest'
        db.create_table(u'submissions_unittest_tasks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unittest', models.ForeignKey(orm[u'submissions.unittest'], null=False)),
            ('task', models.ForeignKey(orm[u'submissions.task'], null=False))
        ))
        db.create_unique(u'submissions_unittest_tasks', ['unittest_id', 'task_id'])


    def backwards(self, orm):
        # Deleting model 'UserID'
        db.delete_table(u'submissions_userid')

        # Deleting model 'Task'
        db.delete_table(u'submissions_task')

        # Deleting model 'Exercise'
        db.delete_table(u'submissions_exercise')

        # Deleting model 'Upload'
        db.delete_table(u'submissions_upload')

        # Deleting model 'UnitTest'
        db.delete_table(u'submissions_unittest')

        # Removing M2M table for field tasks on 'UnitTest'
        db.delete_table('submissions_unittest_tasks')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'submissions.exercise': {
            'Meta': {'object_name': 'Exercise'},
            'descrip': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['submissions.Task']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'xpVal': ('django.db.models.fields.IntegerField', [], {})
        },
        u'submissions.task': {
            'Meta': {'object_name': 'Task'},
            'closeTime': ('django.db.models.fields.DateTimeField', [], {}),
            'descrip': ('django.db.models.fields.TextField', [], {}),
            'fileName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'openTime': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '200'}),
            'xpVal': ('django.db.models.fields.IntegerField', [], {})
        },
        u'submissions.unittest': {
            'Meta': {'object_name': 'UnitTest'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['submissions.Task']", 'symmetrical': 'False'})
        },
        u'submissions.upload': {
            'Meta': {'object_name': 'Upload'},
            'fileUpload': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mostRecent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['submissions.Task']"}),
            'uploadTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'uploadURL': ('django.db.models.fields.URLField', [], {'default': "' '", 'max_length': '200'}),
            'userID': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'submissions.userid': {
            'Meta': {'object_name': 'UserID'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['submissions']