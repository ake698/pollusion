from django.db import models

# Create your models here.


class Airquality(models.Model):
    id = models.AutoField(primary_key=True,verbose_name="ID")
    date = models.DateField(verbose_name="日期")
    qualityLevel = models.CharField(max_length=4,verbose_name="质量等级")
    AQI = models.IntegerField(max_length=4,verbose_name="AQI")
    # range = models.CharField(max_length=10,verbose_name="范围")
    PM25 = models.IntegerField(max_length=4,verbose_name="PM2.5")
    PM10 = models.IntegerField(max_length=4,verbose_name="PM10")
    SO2 = models.IntegerField(max_length=4,verbose_name="SO2")
    NO2 = models.IntegerField(max_length=4,verbose_name="NO2")
    CO = models.CharField(max_length=6,verbose_name="CO")
    O3 = models.IntegerField(max_length=4,verbose_name="O3")

    def __str__(self):
        return self.qualityLevel

    class Meta:
        verbose_name = "空气质量管理"
        verbose_name_plural = "空气质量管理"

