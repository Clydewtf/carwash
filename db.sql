CREATE TABLE `roles`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);
CREATE TABLE `services`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL,
    `price` INT NOT NULL,
    `time` INT NOT NULL
);
CREATE TABLE `role_user`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `role_id` INT NOT NULL
);
CREATE TABLE `customer_cars`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `car_id` INT NOT NULL,
    `customer_id` INT NOT NULL,
    `year` INT NOT NULL COMMENT 'Год выпуска',
    `number` VARCHAR(255) NOT NULL COMMENT 'Номер машины'
);
CREATE TABLE `cars`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `brand_id` INT NOT NULL,
    `model` VARCHAR(255) NOT NULL
);
CREATE TABLE `order_service`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `service_id` INT NOT NULL,
    `order_id` INT NOT NULL
);
CREATE TABLE `orders`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `administrator_id` INT NOT NULL,
    `customer_car_id` INT NOT NULL,
    `employee_id` INT NOT NULL,
    `status` INT NOT NULL,
    `start_date` DATETIME NOT NULL,
    `end_date` DATETIME NOT NULL
);
CREATE TABLE `brand`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL
);
CREATE TABLE `users`(
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(255) NOT NULL,
    `last_name` VARCHAR(255) NOT NULL,
    `patronymic` VARCHAR(255) NULL,
    `email` VARCHAR(255) NOT NULL,
    `is_send_notify` BOOLEAN NOT NULL
);
ALTER TABLE
    `orders` ADD CONSTRAINT `orders_customer_car_id_foreign` FOREIGN KEY(`customer_car_id`) REFERENCES `customer_cars`(`id`);
ALTER TABLE
    `cars` ADD CONSTRAINT `cars_brand_id_foreign` FOREIGN KEY(`brand_id`) REFERENCES `brand`(`id`);
ALTER TABLE
    `order_service` ADD CONSTRAINT `order_service_service_id_foreign` FOREIGN KEY(`service_id`) REFERENCES `services`(`id`);
ALTER TABLE
    `customer_cars` ADD CONSTRAINT `customer_cars_customer_id_foreign` FOREIGN KEY(`customer_id`) REFERENCES `users`(`id`);
ALTER TABLE
    `role_user` ADD CONSTRAINT `role_user_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `users`(`id`);
ALTER TABLE
    `orders` ADD CONSTRAINT `orders_administrator_id_foreign` FOREIGN KEY(`administrator_id`) REFERENCES `users`(`id`);
ALTER TABLE
    `role_user` ADD CONSTRAINT `role_user_user_id_foreign` FOREIGN KEY(`user_id`) REFERENCES `roles`(`id`);
ALTER TABLE
    `customer_cars` ADD CONSTRAINT `customer_cars_id_foreign` FOREIGN KEY(`id`) REFERENCES `cars`(`id`);
ALTER TABLE
    `orders` ADD CONSTRAINT `orders_employee_id_foreign` FOREIGN KEY(`employee_id`) REFERENCES `users`(`id`);
ALTER TABLE
    `order_service` ADD CONSTRAINT `order_service_order_id_foreign` FOREIGN KEY(`order_id`) REFERENCES `orders`(`id`);