CREATE DATABASE Sales_Management;
GO

CREATE TABLE branches (
    branch_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    branch_admin_name VARCHAR(100) NOT NULL
);
CREATE TABLE customer_sales (
    sale_id INT IDENTITY(1,1) PRIMARY KEY,
    branch_id INT NOT NULL, 
    [date] DATE NOT NULL,
    name VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(15),
    product_name VARCHAR(30) NOT NULL,
    gross_sales DECIMAL(12,2) NOT NULL,
    received_amount DECIMAL(12,2) DEFAULT 0,
    pending_amount AS (gross_sales - received_amount),
    
    status VARCHAR(10) NOT NULL
    CHECK (status IN ('Open', 'Close')),

    CONSTRAINT FK_BRANCH_ID
        FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
);
CREATE TABLE users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    branch_id INT NULL,
    role VARCHAR(20) NOT NULL
        CHECK (role IN ('Super Admin', 'Admin')),
    email VARCHAR(255) NOT NULL UNIQUE,
    CONSTRAINT FK_users_branch
        FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
);

CREATE TABLE payment_splits (
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    sale_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount_paid DECIMAL(12,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    CONSTRAINT FK_payment_splits_sales
        FOREIGN KEY (sale_id)
        REFERENCES customer_sales(sale_id)
);

CREATE TRIGGER trg_update_customer_sales
ON payment_splits
AFTER INSERT
AS
BEGIN

        UPDATE cs
    SET 
        received_amount = ISNULL(
            (
                SELECT SUM(ps.amount_paid)
                FROM payment_splits ps
                WHERE ps.sale_id = cs.sale_id
            ),
            0
        ),

        status = CASE
                    WHEN (
                        cs.gross_sales -
                        ISNULL(
                            (
                                SELECT SUM(ps.amount_paid)
                                FROM payment_splits ps
                                WHERE ps.sale_id = cs.sale_id
                            ),
                            0
                        )
                    ) = 0
                    THEN 'Close'

                    ELSE 'Open'
                 END

    FROM customer_sales cs
    INNER JOIN inserted i
        ON cs.sale_id = i.sale_id;
END;

select * from payment_splits
select * from branches
select * from users
select * from customer_sales
