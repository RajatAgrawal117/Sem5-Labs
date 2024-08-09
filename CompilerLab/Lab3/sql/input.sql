-- This is a comment
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(100)
);

/* Another comment block
   with multiple lines */
INSERT INTO employees (id, name, position) VALUES (1, 'John Doe', 'Manager');
INSERT INTO employees (id, name, position) VALUES (2, 'Jane Smith', 'Developer');

SELECT * FROM employees;

UPDATE employees SET position = 'Senior Developer' WHERE id = 2;

DELETE FROM employees WHERE id = 1;

DROP TABLE employees;

-- Some random text
This text should not be extracted as SQL.

Another non-SQL line.
-- Inserting a new employee
INSERT INTO employees (id, name, position) VALUES (3, 'Mark Johnson', 'Tester');

-- Updating employee's position
UPDATE employees SET position = 'Project Manager' WHERE id = 1;

-- Selecting employees with a specific position
SELECT * FROM employees WHERE position = 'Developer';

-- Deleting all employees
DELETE FROM employees;