
CREATE TABLE userdetails (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
); 

-- /*Data for the table `userdetails` */

INSERT INTO userdetails (id, name, email, password)
VALUES (1,'hunnur','hunnur@gmail.com','123');

-- /*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

-- CREATE TABLE employees (
--   id INTEGER PRIMARY KEY,
--   name TEXT NOT NULL,
--   age INTEGER NOT NULL,
--   salary REAL NOT NULL
-- );

-- INSERT INTO employees (id, name, age, salary)
-- VALUES (1, 'John', 32, 45000.00);

-- INSERT INTO employees (id, name, age, salary)
-- VALUES (2, 'Jane', 27, 50000.00);

-- INSERT INTO employees (id, name, age, salary)
-- VALUES (3, 'Bob', 35, 55000.00);
