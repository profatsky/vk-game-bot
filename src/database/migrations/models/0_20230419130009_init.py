from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "clothes" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "price" INT NOT NULL  DEFAULT 0,
    "image_path" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "faces" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "price" INT NOT NULL  DEFAULT 0,
    "image_path" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "gpu" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "price" INT NOT NULL  DEFAULT 0,
    "image_path" VARCHAR(256) NOT NULL,
    "income" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "haircuts" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "price" INT NOT NULL  DEFAULT 0,
    "image_path" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "skins" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "price" INT NOT NULL  DEFAULT 0,
    "image_path" VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "vk_id" INT NOT NULL UNIQUE,
    "balance" INT NOT NULL  DEFAULT 1500,
    "nickname" VARCHAR(16) NOT NULL,
    "status" VARCHAR(24) NOT NULL  DEFAULT 'Пользователь',
    "clothes_id" INT REFERENCES "clothes" ("id") ON DELETE CASCADE,
    "face_id" INT NOT NULL REFERENCES "faces" ("id") ON DELETE CASCADE,
    "gpu_1_id" INT REFERENCES "gpu" ("id") ON DELETE CASCADE,
    "gpu_2_id" INT REFERENCES "gpu" ("id") ON DELETE CASCADE,
    "gpu_3_id" INT REFERENCES "gpu" ("id") ON DELETE CASCADE,
    "haircut_id" INT NOT NULL REFERENCES "haircuts" ("id") ON DELETE CASCADE,
    "skin_id" INT NOT NULL REFERENCES "skins" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "mining" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "gpu_1" TIMESTAMP,
    "gpu_2" TIMESTAMP,
    "gpu_3" TIMESTAMP,
    "user_id" INT NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
INSERT INTO `skins` (`price`, `image_path`) VALUES 
(500, 'skins/skin1.png'), (500, 'skins/skin2.png'), (500, 'skins/skin3.png');
INSERT INTO `clothes` (`price`, `image_path`) VALUES 
(1500, 'clothes/clothes1.png'), (1500, 'clothes/clothes2.png'), (1500, 'clothes/clothes3.png');
INSERT INTO `haircuts` (`price`, `image_path`) VALUES 
(500, 'haircuts/haircut1.png'), (500, 'haircuts/haircut2.png'), (500, 'haircuts/haircut3.png'),
(1500, 'haircuts/haircut4.png'), (3000, 'haircuts/haircut5.png'), (5000, 'haircuts/haircut6.png'),
(10000, 'haircuts/haircut7.png'), (15000, 'haircuts/haircut8.png'), (30000, 'haircuts/haircut9.png');
INSERT INTO `faces` (`price`, `image_path`) VALUES 
(500, 'faces/face1.png'), (500, 'faces/face2.png'), (500, 'faces/face3.png'),
(1500, 'faces/face4.png'), (3000, 'faces/face5.png'), (5000, 'faces/face6.png');
INSERT INTO `gpu` (`price`, `image_path`, `income`) VALUES 
(1500, 'gpu/low_card.png', 25), (7500, 'gpu/medium_card.png', 80), (25000, 'gpu/high_card.png', 250);
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
