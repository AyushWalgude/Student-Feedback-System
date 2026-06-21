-- STUDENT FEEDBACK SYSTEM — DATABASE SETUP
-- Run this entire file in MySQL to set up the complete database

-- ── Create Database ────────────────────────────────────────────────────────────
CREATE DATABASE IF NOT EXISTS student_feedback_db;
USE student_feedback_db;

-- TABLE: students

CREATE TABLE IF NOT EXISTS students (
    student_id    VARCHAR(20) PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    department    VARCHAR(100) NOT NULL,
    email         VARCHAR(100),
    password      VARCHAR(255),
    is_registered BOOLEAN DEFAULT FALSE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- TABLE: teachers

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id  VARCHAR(20) PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    department  VARCHAR(100) NOT NULL,
    subject     VARCHAR(100) NOT NULL
);

-- TABLE: feedback

CREATE TABLE IF NOT EXISTS feedback (
    student_id        VARCHAR(20) NOT NULL,
    teacher_id        VARCHAR(20) NOT NULL,
    teaching_quality  INT CHECK (teaching_quality BETWEEN 1 AND 5),
    communication     INT CHECK (communication BETWEEN 1 AND 5),
    punctuality       INT CHECK (punctuality BETWEEN 1 AND 5),
    knowledge         INT CHECK (knowledge BETWEEN 1 AND 5),
    overall_rating    INT CHECK (overall_rating BETWEEN 1 AND 5),
    comments          TEXT,
    submitted_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- TABLE: admins

CREATE TABLE IF NOT EXISTS admins (
    admin_id    VARCHAR(20) PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SAMPLE DATA — Default Admin

INSERT INTO admins (admin_id, name, email, password) VALUES
('ADM001', 'Super Admin', 'admin@college.edu', 'admin123');


-- VERIFY SETUP

SHOW TABLES;
SELECT * FROM admins;

