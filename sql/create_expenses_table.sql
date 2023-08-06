CREATE TABLE expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expenseDate DATE NOT NULL,
    amount FLOAT NOT NULL,
    category INT
);