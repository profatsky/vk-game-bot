from tortoise.models import Model
from tortoise import fields


class User(Model):
    vk_id = fields.IntField()
    balance = fields.IntField(default=0)
    nickname = fields.CharField(max_length=16)
    skin = fields.ForeignKeyField('models.Skin')
    face = fields.ForeignKeyField('models.Face')
    haircut = fields.ForeignKeyField('models.Haircut')
    clothes = fields.ForeignKeyField('models.Clothes')
    gpu_1 = fields.ForeignKeyField('models.GraphicsCard', related_name=False)
    gpu_2 = fields.ForeignKeyField('models.GraphicsCard', related_name=False)
    gpu_3 = fields.ForeignKeyField('models.GraphicsCard', related_name=False)
    is_admin = fields.BooleanField(default=False)

    class Meta:
        table = 'users'


class AbstractItemModel(Model):
    price = fields.IntField(default=0)
    image_path = fields.CharField(max_length=256)

    class Meta:
        abstract = True


class Skin(AbstractItemModel):
    class Meta:
        table = 'skins'


class Face(AbstractItemModel):
    class Meta:
        table = 'faces'


class Haircut(AbstractItemModel):
    class Meta:
        table = 'haircuts'


class Clothes(AbstractItemModel):
    class Meta:
        table = 'clothes'


class GraphicsCard(AbstractItemModel):
    income = fields.IntField()

    class Meta:
        table = 'gpu'
