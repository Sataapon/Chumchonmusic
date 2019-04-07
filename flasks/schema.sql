DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Teacher;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Instrument;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Teach;
DROP TABLE IF EXISTS Enroll;
DROP TABLE IF EXISTS DateTime;

CREATE TABLE Admin (
	AdminId INTEGER PRIMARY KEY AUTOINCREMENT,
	Name TEXT UNIQUE NOT NULL,
	Username TEXT UNIQUE NOT NULL,
	Password TEXT NOT NULL
);

CREATE TABLE Teacher (
	TeacherID INTEGER PRIMARY KEY AUTOINCREMENT,
	Username TEXT UNIQUE NOT NULL,
	Password TEXT NOT NULL,
	Firstname TEXT NOT NULL,
	Lastname TEXT NOT NULL,
	Nickname TEXT NOT NULL,
	Birthday TEXT NOT NULL,
	Email TEXT UNIQUE NOT NULL,
	TelNum TEXT UNIQUE NOT NULL,
	LineId TEXT UNIQUE,
	Image BLOB
);

CREATE TABLE Student (
	StudentID INTEGER PRIMARY KEY AUTOINCREMENT,
	Username TEXT UNIQUE NOT NULL,
	Password TEXT NOT NULL,
	Firstname TEXT NOT NULL,
	Lastname TEXT NOT NULL,
	Nickname TEXT NOT NULL,
	Birthday TEXT NOT NULL,
	Email TEXT UNIQUE NOT NULL,
	TelNum TEXT UNIQUE NOT NULL,
	LineId TEXT UNIQUE,
	Image BLOB
);

CREATE TABLE Instrument (
	InstrumentId INTEGER PRIMARY KEY AUTOINCREMENT,
	Name TEXT UNIQUE NOT NULL	
);

CREATE TABLE Course (
	CourseId INTEGER PRIMARY KEY AUTOINCREMENT,
	Name TEXT UNIQUE NOT NULL,
	Price INTEGER NOT NULL,
	HousPerTime INTEGER NOT NULL,
	NumOfTime INTEGER NOT NULL,
	InstrumentId INTEGER NOT NULL,
	FOREIGN KEY (InstrumentId) REFERENCES Instrument (InstrumentId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Teach (
	CourseId INTEGER,
	TeacherId INTEGER,
	PRIMARY KEY (CourseId, TeacherId),
	FOREIGN KEY (CourseId) REFERENCES Course (CourseId) ON DELETE CASCADE ON UPDATE CASCADE
	FOREIGN KEY (TeacherId) REFERENCES Teacher (TeacherId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Enroll (
	CourseId INTEGER,
	StudentId INTEGER,
	PRIMARY KEY (CourseId, StudentId),
	FOREIGN KEY (CourseId) REFERENCES Course (CourseId) ON DELETE CASCADE ON UPDATE CASCADE
	FOREIGN KEY (StudentId) REFERENCES Student (StudentId) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE DateTime (
	CourseId INTEGER,
	StudentId INTEGER,
	DateTime TEXT,
	PRIMARY KEY (CourseId, StudentId, DateTime),
	FOREIGN KEY (CourseId, StudentId) REFERENCES Enroll (CourseId, StudentId) ON DELETE CASCADE ON UPDATE CASCADE
);

