from djongo import models

# Create your models here.
class Logs(models.Model):
    _id = models.ObjectIdField()
    endPoint= models.CharField(max_length=200,null=True)
    modulo = models.CharField(max_length=100,null=True)
    tipo = models.CharField(max_length=100,null=True)
    accion = models.CharField(max_length=100,null=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    dataEnviada = models.TextField(default='{}')
    fechaFin= models.DateTimeField(null=True)
    dataRecibida = models.TextField(default='{}')
    state = models.SmallIntegerField(default=1)
    def __str__(self):
        return '{}'.format(self.endPoint)


