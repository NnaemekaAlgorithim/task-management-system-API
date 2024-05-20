-- Create the database
CREATE DATABASE IF NOT EXISTS `task-manager-db`;
USE `task-manager-db`;

-- Create the User table
CREATE TABLE `user` (
    `user_id` VARCHAR(60) NOT NULL PRIMARY KEY,
    `first_name` VARCHAR(128),
    `last_name` VARCHAR(128),
    `email` VARCHAR(128) NOT NULL,
    `password` VARCHAR(128) NOT NULL,
    `confirmed` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (`email`)
);

-- Create the TaskGroup table
CREATE TABLE `task_group` (
    `task_group_id` VARCHAR(60) NOT NULL PRIMARY KEY,
    `task_group_title` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (`task_group_title`)
);

-- Create the Task table
CREATE TABLE `task` (
    `task_id` VARCHAR(60) NOT NULL PRIMARY KEY,
    `task_title` VARCHAR(255) NOT NULL,
    `task_description` VARCHAR(1024),
    `created_by` VARCHAR(128),
    `updated_by` VARCHAR(128),
    `moved_by` VARCHAR(128),
    `task_group` VARCHAR(255) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`task_group`) REFERENCES `task_group`(`task_group_title`)
);

INSERT INTO user (user_id, first_name, last_name, email, password, confirmed)
VALUES ('admin_user_id', 'Admin', 'Management', 'Admin@gmail.com', 'Admin$123', TRUE);
