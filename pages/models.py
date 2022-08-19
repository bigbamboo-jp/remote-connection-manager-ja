from accounts.models import CustomUser
from django.db import models

# Create your models here.


class ActionLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ログ作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='ログ更新日時')
    created_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name='ユーザー')
    type = models.IntegerField()
    execution_time = models.DateTimeField(blank=True, null=True, verbose_name='実行日時', help_text='アクションがスケジュールされていてまだ完了していない場合、この値は実行予定日時を表します。')
    executed = models.BooleanField(blank=True, null=True, verbose_name='実行した', help_text='？は実行予定、×は実行中止、✓は完了を意味します。')

    def __str__(self) -> str:
        if self.type == 0:
            return self.execution_time.strftime('%Y/%m/%d %H:%M:%S') + ' (' + str(self.created_by) + '): SSH接続を今すぐ有効にする'
        if self.type == 1:
            return self.execution_time.strftime('%Y/%m/%d %H:%M:%S') + ' (' + str(self.created_by) + '): SSH接続を今すぐ無効にする'
        if self.type == 3:
            return self.execution_time.strftime('%Y/%m/%d %H:%M:%S') + ' (' + str(self.created_by) + '): SSH接続を一定時間後に無効にする'

    class Meta:
        verbose_name = 'アクションログ'
        verbose_name_plural = 'アクションログ'


class AutomaticProcessingSchedule(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name='作成者')
    process = models.IntegerField()
    run_at = models.DateTimeField(verbose_name='実行予定日時', help_text='何らかの理由で予定日時に処理を行えなかった場合は、次回のアプリケーション起動時に実行されます。')

    def __str__(self) -> str:
        if self.process == 1:
            return self.run_at.strftime('%Y/%m/%d %H:%M:%S') + ' (' + str(self.created_by) + '): SSH接続を一定時間後に無効にする'
        else:
            return self.run_at.strftime('%Y/%m/%d %H:%M:%S') + ' (' + str(self.created_by) + '): プロセス' + str(self.process)

    class Meta:
        verbose_name = '自動処理のスケジュール'
        verbose_name_plural = '自動処理のスケジュール'
