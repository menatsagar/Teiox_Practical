from django.db import models


class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class BaseUserTrackedModel(models.Model):
    created_by = models.EmailField(null=True, blank=True)
    updated_by = models.EmailField(null=True, blank=True)

    class Meta:
        abstract = True


class AuditModelMixin(BaseTimestampedModel, BaseUserTrackedModel):
    mark_as_deleted = models.BooleanField(default = False, blank=True, null=True)
    class Meta:
        abstract = True
