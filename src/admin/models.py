from tortoise import Model, fields


class QuestionModel(Model):
    text = fields.CharField(max_length=512)
    from_user = fields.ForeignKeyField('models.UserModel', on_delete='SET NULL', related_name='questions', null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    answer = fields.CharField(max_length=512, null=True)
    answered_by = fields.ForeignKeyField('models.UserModel', on_delete='SET NULL', related_name='answers', null=True)
    answered_at = fields.DatetimeField(null=True)

    class Meta:
        table = 'questions'
