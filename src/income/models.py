from tortoise import Model, fields


class DailyBonus(Model):
    user = fields.OneToOneField('models.UserModel', on_delete='CASCADE')
    receiving_date = fields.DateField()
    amount = fields.IntField(default=0)

    class Meta:
        table = 'daily_bonus'
