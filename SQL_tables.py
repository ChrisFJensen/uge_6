brands_table = """CREATE TABLE brands (
  brand_id int NOT NULL AUTO_INCREMENT,
  brand_name varchar(255) NOT NULL,
  PRIMARY KEY (brand_id)
)"""

categories_table = """CREATE TABLE categories (
  category_id int NOT NULL AUTO_INCREMENT,
  category_name varchar(255) NOT NULL,
  PRIMARY KEY (category_id)
);"""

products_table = """CREATE TABLE products (
  product_id int NOT NULL AUTO_INCREMENT,
  product_name varchar(255) NOT NULL,
  brand_id int DEFAULT NULL,
  category_id int DEFAULT NULL,
  model_year int DEFAULT NULL,
  list_price float DEFAULT NULL,
  PRIMARY KEY (product_id),
  KEY brand_id (brand_id),
  KEY category_id (category_id),
  CONSTRAINT products_ibfk_1 FOREIGN KEY (brand_id) REFERENCES brands (brand_id),
  CONSTRAINT products_ibfk_2 FOREIGN KEY (category_id) REFERENCES categories (category_id)
)"""

stores_table = """CREATE TABLE stores (
    name varchar(50) DEFAULT NULL,
    phone varchar(15) DEFAULT NULL,
    email varchar(50) DEFAULT NULL,
    street varchar(255) DEFAULT NULL,
    city varchar(255) DEFAULT NULL,
    state char(2) DEFAULT NULL,
    zip_code int DEFAULT NULL,
    store_id int NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (store_id)
)"""

stocks_table = """CREATE TABLE stocks (
  store_id int DEFAULT NULL,
  product_id int DEFAULT NULL,
  quantity int DEFAULT NULL,
  KEY product_id (product_id),
  CONSTRAINT stocks_ibfk_1 FOREIGN KEY (product_id) REFERENCES products (product_id),
  CONSTRAINT stocks_ibfk_2 FOREIGN KEY (store_id) REFERENCES stores (store_id)
)"""

staff_table = """CREATE TABLE staffs(
    name varchar(20) DEFAULT NULL,
    last_name varchar(50) DEFAULT NULL,
    email varchar(255) DEFAULT NULL,
    phone varchar(15) DEFAULT NULL,
    active bit DEFAULT NULL,
    manager_id int DEFAULT NULL,
    staff_id int NOT NULL AUTO_INCREMENT,
    store_id int DEFAULT NULL,
    PRIMARY KEY (staff_id),
    CONSTRAINT staffs_ibfk_1 FOREIGN KEY (store_id) REFERENCES stores (store_id)
)"""

customers_table = """CREATE TABLE customers (
    city varchar(255) DEFAULT NULL,
    customer_id int NOT NULL AUTO_INCREMENT,
    email varchar(255) DEFAULT NULL,
    first_name varchar(20) DEFAULT NULL,
    last_name varchar(50) DEFAULT NULL,
    phone varchar(15) DEFAULT NULL,
    state char(2) DEFAULT NULL,
    street varchar(255) DEFAULT NULL,
    zip_code int DEFAULT NULL,
    PRIMARY KEY (customer_id)
)"""

orders_table = """CREATE TABLE orders (
    customer_id int DEFAULT NULL,
    order_date date DEFAULT NULL,
    order_id int NOT NULL AUTO_INCREMENT,
    order_status tinyint DEFAULT 1,
    required_date date DEFAULT NULL,
    shipped_date date DEFAULT NULL,
    staff_id int DEFAULT NULL,
    store_id int DEFAULT NULL,
    PRIMARY KEY (order_id),
    CONSTRAINT orders_ibfk_1 FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    CONSTRAINT orders_ibfk_2 FOREIGN KEY (staff_id) REFERENCES staffs (staff_id),
    CONSTRAINT orders_ibfk_3 FOREIGN KEY (store_id) REFERENCES stores (store_id)
)"""

order_items_table = """CREATE TABLE order_items (
    discount decimal(4,3) DEFAULT 0.0,
    item_id tinyint NOT NULL,
    order_id int NOT NULL,
    product_id int NOT NULL,
    quantity tinyint DEFAULT 1,
    CONSTRAINT order_items_ibfk_1 FOREIGN KEY (order_id) REFERENCES orders (order_id),
    CONSTRAINT order_items_ibfk_2 FOREIGN KEY (product_id) REFERENCES products (product_id)
)"""

table_list = [brands_table, categories_table, products_table, stores_table, stocks_table, customers_table, staff_table, orders_table, order_items_table]