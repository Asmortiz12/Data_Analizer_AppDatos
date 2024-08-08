from django.db import models



class COMPANY(models.Model):
    class Meta:
        db_table = 'company'
    COM_ID     = models.CharField(primary_key=True) 
    COM_RUC    = models.CharField(max_length=20)
    COM_NAME   = models.TextField(max_length=50, default="Default Name")
    COM_SYMBOL = models.TextField(max_length=6, default="SYM")
    COM_IMFORMATION = models.TextField(max_length=1000, default="Default Information")
    CON_IMAGE = models.ImageField(upload_to='Company_Logos/', blank=True, null=True)
     
    def __str__(self):
        return self.COM_NAME

class PLACE_ORIGIN(models.Model):
    class Meta:
        db_table = 'place_origin'
    OR_ID       = models.AutoField(primary_key=True)  
    OR_LOCATION = models.CharField(max_length=50, default="Default Location")

class TYPE_TRANSACTION(models.Model):
    class Meta:
        db_table = 'type_transaction'
    TYT_ID   = models.AutoField(primary_key=True)  
    TYT_Type = models.CharField(max_length=50, default="Default Type")

class STOCK_TRANSACTION(models.Model):
    class Meta:
        db_table = 'stock_transaction'
    STT_ID             = models.AutoField(primary_key=True)  
    COM_ID             = models.ForeignKey(COMPANY, on_delete=models.CASCADE, null=False, blank=False)
    OR_ID              = models.ForeignKey(PLACE_ORIGIN, on_delete=models.CASCADE, null=False, blank=False)
    TYT_ID             = models.ForeignKey(TYPE_TRANSACTION, on_delete=models.CASCADE, null=False, blank=False)
    STT_DATE           = models.DateField(blank=True, null=True)
    STT_DESCRIPTION    = models.CharField(max_length=200, default="Default Description")
    STT_NOMINAL_VALUE  = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    STT_PRICE          = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    STT_NUM_SHARES     = models.IntegerField(null=False, default=0)
    STT_CASH_VALUE     = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)

    
    
    
    