from tortoise import Model, fields


class MiningModel(Model):
    user = fields.OneToOneField('models.UserModel')
    gpu_1 = fields.DatetimeField(null=True)
    gpu_2 = fields.DatetimeField(null=True)
    gpu_3 = fields.DatetimeField(null=True)

    class Meta:
        table = 'mining'
