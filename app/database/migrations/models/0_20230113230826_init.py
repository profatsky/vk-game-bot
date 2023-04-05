from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `clothes` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `price` INTEGER NOT NULL  DEFAULT 0,
    `image_path` VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS `faces` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `price` INTEGER NOT NULL  DEFAULT 0,
    `image_path` VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS `gpu` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `price` INTEGER NOT NULL  DEFAULT 0,
    `image_path` VARCHAR(256) NOT NULL,
    `income` INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS `haircuts` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `price` INTEGER NOT NULL  DEFAULT 0,
    `image_path` VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS `skins` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `price` INTEGER NOT NULL  DEFAULT 0,
    `image_path` VARCHAR(256) NOT NULL
);
CREATE TABLE IF NOT EXISTS `users` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `vk_id` INTEGER NOT NULL UNIQUE,
    `balance` INTEGER NOT NULL  DEFAULT 1500,
    `nickname` VARCHAR(16) NOT NULL,
    `is_admin` BOOL NOT NULL  DEFAULT 0,
    `clothes_id` INTEGER,
    `face_id` INTEGER NOT NULL,
    `gpu_1_id` INTEGER,
    `gpu_2_id` INTEGER,
    `gpu_3_id` INTEGER,
    `haircut_id` INT NOT NULL,
    `skin_id` INT NOT NULL,
    CONSTRAINT `fk_users_clothes_cefbd78a` FOREIGN KEY (`clothes_id`) REFERENCES `clothes` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_users_faces_f3529b3b` FOREIGN KEY (`face_id`) REFERENCES `faces` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_users_gpu_639fa1fc` FOREIGN KEY (`gpu_1_id`) REFERENCES `gpu` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_users_gpu_eb4e6a28` FOREIGN KEY (`gpu_2_id`) REFERENCES `gpu` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_users_gpu_affb2aba` FOREIGN KEY (`gpu_3_id`) REFERENCES `gpu` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_users_haircuts_e3ffd613` FOREIGN KEY (`haircut_id`) REFERENCES `haircuts` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_users_skins_7e83cc18` FOREIGN KEY (`skin_id`) REFERENCES `skins` (`id`) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS `mining` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `gpu_1` DATETIME(6),
    `gpu_2` DATETIME(6),
    `gpu_3` DATETIME(6),
    `user_id` INTEGER NOT NULL UNIQUE,
    CONSTRAINT `fk_mining_users_bec9b01d` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
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
