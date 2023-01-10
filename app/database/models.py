from tortoise.models import Model
from tortoise import fields

from database.models_representations import AppearanceItem, User


class UserModel(Model):
    vk_id = fields.IntField()
    balance = fields.IntField(default=0)
    nickname = fields.CharField(max_length=16)
    skin = fields.ForeignKeyField('models.SkinModel')
    face = fields.ForeignKeyField('models.FaceModel')
    haircut = fields.ForeignKeyField('models.HaircutModel')
    clothes = fields.ForeignKeyField('models.ClothesModel', null=True)
    gpu_1 = fields.ForeignKeyField('models.GraphicsCardModel', related_name=False, null=True)
    gpu_2 = fields.ForeignKeyField('models.GraphicsCardModel', related_name=False, null=True)
    gpu_3 = fields.ForeignKeyField('models.GraphicsCardModel', related_name=False, null=True)
    is_admin = fields.BooleanField(default=False)

    class Meta:
        table = 'users'

    async def convert_to_dataclass(self):
        clothes = await self.clothes
        if clothes:
            clothes = clothes.convert_to_dataclass()
        return User(
            pk=self.pk,
            balance=self.balance,
            nickname=self.nickname,
            skin=(await self.skin).convert_to_dataclass(),
            face=(await self.face).convert_to_dataclass(),
            haircut=(await self.haircut).convert_to_dataclass(),
            clothes=clothes,
            is_admin=self.is_admin
        )


class AbstractItemModel(Model):
    price = fields.IntField(default=0)
    image_path = fields.CharField(max_length=256)

    class Meta:
        abstract = True

    def convert_to_dataclass(self):
        return AppearanceItem(
            pk=self.pk,
            price=self.price,
            image_path=self.image_path
        )


class SkinModel(AbstractItemModel):
    class Meta:
        table = 'skins'


class FaceModel(AbstractItemModel):
    class Meta:
        table = 'faces'


class HaircutModel(AbstractItemModel):
    class Meta:
        table = 'haircuts'


class ClothesModel(AbstractItemModel):
    class Meta:
        table = 'clothes'


class GraphicsCardModel(AbstractItemModel):
    income = fields.IntField()

    class Meta:
        table = 'gpu'
