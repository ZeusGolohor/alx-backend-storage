-- Write a SQL script that creates a trigger that decreases the quantity
CREATE TRIGGER decrease_quantity AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name=NEW.item_name;
