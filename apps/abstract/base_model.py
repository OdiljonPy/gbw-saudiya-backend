from django.db import models

class CreatedAtAbstractModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True

class UpdatedAtAbstractModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class CreatedUpdatedAbstractModel(CreatedAtAbstractModel, UpdatedAtAbstractModel):
    class Meta:
        abstract = True
        ordering = ['-created_at']