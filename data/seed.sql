-- Customers (20 rows)
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    created_at TEXT,
    tier TEXT DEFAULT 'standard'
);

INSERT INTO customers VALUES ('C001', 'Nguyen Van An', 'an.nguyen@email.com', '0901234567', '2023-03-15', 'platinum');
INSERT INTO customers VALUES ('C002', 'Tran Thi Binh', 'binh.tran@email.com', '0912345678', '2024-01-20', 'gold');
INSERT INTO customers VALUES ('C003', 'Le Hoang Cuong', 'cuong.le@email.com', '0923456789', '2024-06-10', 'standard');
INSERT INTO customers VALUES ('C004', 'Pham Minh Duc', 'duc.pham@email.com', '0934567890', '2023-08-05', 'gold');
INSERT INTO customers VALUES ('C005', 'Vo Thi Em', 'em.vo@email.com', '0945678901', '2025-01-12', 'standard');
INSERT INTO customers VALUES ('C006', 'Hoang Van Phuc', 'phuc.hoang@email.com', '0956789012', '2023-11-22', 'platinum');
INSERT INTO customers VALUES ('C007', 'Dang Thi Giang', 'giang.dang@email.com', '0967890123', '2024-04-18', 'standard');
INSERT INTO customers VALUES ('C008', 'Bui Quoc Huy', 'huy.bui@email.com', '0978901234', '2024-09-30', 'gold');
INSERT INTO customers VALUES ('C009', 'Ngo Thi Yen', 'yen.ngo@email.com', '0989012345', '2023-05-08', 'platinum');
INSERT INTO customers VALUES ('C010', 'Do Van Khanh', 'khanh.do@email.com', '0990123456', '2025-03-01', 'standard');
INSERT INTO customers VALUES ('C011', 'Ly Thi Lan', 'lan.ly@email.com', '0901112233', '2024-07-14', 'gold');
INSERT INTO customers VALUES ('C012', 'Truong Van Minh', 'minh.truong@email.com', '0912223344', '2023-12-01', 'standard');
INSERT INTO customers VALUES ('C013', 'Mai Thi Ngoc', 'ngoc.mai@email.com', '0923334455', '2024-02-28', 'gold');
INSERT INTO customers VALUES ('C014', 'Cao Van Phong', 'phong.cao@email.com', '0934445566', '2025-05-10', 'standard');
INSERT INTO customers VALUES ('C015', 'Dinh Thi Quyen', 'quyen.dinh@email.com', '0945556677', '2023-09-17', 'platinum');
INSERT INTO customers VALUES ('C016', 'Ha Van Son', 'son.ha@email.com', '0956667788', '2024-11-05', 'standard');
INSERT INTO customers VALUES ('C017', 'Luu Thi Thao', 'thao.luu@email.com', '0967778899', '2024-03-22', 'gold');
INSERT INTO customers VALUES ('C018', 'Vu Van Uy', 'uy.vu@email.com', '0978889900', '2025-02-14', 'standard');
INSERT INTO customers VALUES ('C019', 'Duong Thi Van', 'van.duong@email.com', '0989990011', '2023-07-30', 'gold');
INSERT INTO customers VALUES ('C020', 'Tang Van Xuan', 'xuan.tang@email.com', '0990001122', '2024-10-08', 'standard');

-- Orders (40 rows)
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT REFERENCES customers(customer_id),
    order_date TEXT,
    total_amount REAL,
    status TEXT,
    items_count INTEGER
);

INSERT INTO orders VALUES ('O001', 'C001', '2025-01-05', 2500000, 'delivered', 3);
INSERT INTO orders VALUES ('O002', 'C001', '2025-03-12', 1800000, 'delivered', 2);
INSERT INTO orders VALUES ('O003', 'C002', '2025-02-20', 4200000, 'delivered', 5);
INSERT INTO orders VALUES ('O004', 'C003', '2025-04-01', 750000, 'shipped', 1);
INSERT INTO orders VALUES ('O005', 'C004', '2025-03-15', 3100000, 'delivered', 4);
INSERT INTO orders VALUES ('O006', 'C005', '2025-05-08', 1200000, 'pending', 2);
INSERT INTO orders VALUES ('O007', 'C006', '2025-01-22', 5600000, 'delivered', 7);
INSERT INTO orders VALUES ('O008', 'C006', '2025-04-10', 890000, 'delivered', 1);
INSERT INTO orders VALUES ('O009', 'C007', '2025-02-14', 2100000, 'cancelled', 3);
INSERT INTO orders VALUES ('O010', 'C008', '2025-05-20', 1650000, 'shipped', 2);
INSERT INTO orders VALUES ('O011', 'C009', '2025-01-30', 3800000, 'delivered', 4);
INSERT INTO orders VALUES ('O012', 'C009', '2025-03-25', 920000, 'delivered', 1);
INSERT INTO orders VALUES ('O013', 'C010', '2025-06-01', 2750000, 'pending', 3);
INSERT INTO orders VALUES ('O014', 'C001', '2025-05-18', 4100000, 'shipped', 5);
INSERT INTO orders VALUES ('O015', 'C011', '2025-04-22', 1350000, 'delivered', 2);
INSERT INTO orders VALUES ('O016', 'C012', '2025-02-08', 680000, 'delivered', 1);
INSERT INTO orders VALUES ('O017', 'C013', '2025-05-30', 2900000, 'pending', 3);
INSERT INTO orders VALUES ('O018', 'C004', '2025-06-05', 1100000, 'pending', 1);
INSERT INTO orders VALUES ('O019', 'C014', '2025-05-12', 3400000, 'shipped', 4);
INSERT INTO orders VALUES ('O020', 'C015', '2025-01-10', 7200000, 'delivered', 8);
INSERT INTO orders VALUES ('O021', 'C015', '2025-03-05', 1900000, 'delivered', 2);
INSERT INTO orders VALUES ('O022', 'C016', '2025-04-28', 550000, 'delivered', 1);
INSERT INTO orders VALUES ('O023', 'C017', '2025-02-18', 2300000, 'delivered', 3);
INSERT INTO orders VALUES ('O024', 'C018', '2025-06-10', 1750000, 'pending', 2);
INSERT INTO orders VALUES ('O025', 'C019', '2025-01-15', 4500000, 'delivered', 5);
INSERT INTO orders VALUES ('O026', 'C019', '2025-04-02', 1600000, 'delivered', 2);
INSERT INTO orders VALUES ('O027', 'C020', '2025-05-25', 890000, 'shipped', 1);
INSERT INTO orders VALUES ('O028', 'C002', '2025-05-15', 3200000, 'shipped', 4);
INSERT INTO orders VALUES ('O029', 'C003', '2025-06-08', 2100000, 'pending', 2);
INSERT INTO orders VALUES ('O030', 'C008', '2025-03-20', 1450000, 'delivered', 2);
INSERT INTO orders VALUES ('O031', 'C011', '2025-06-12', 2800000, 'pending', 3);
INSERT INTO orders VALUES ('O032', 'C013', '2025-01-28', 1050000, 'delivered', 1);
INSERT INTO orders VALUES ('O033', 'C006', '2025-06-15', 3600000, 'pending', 4);
INSERT INTO orders VALUES ('O034', 'C004', '2025-02-05', 2200000, 'delivered', 3);
INSERT INTO orders VALUES ('O035', 'C009', '2025-05-22', 1800000, 'shipped', 2);
INSERT INTO orders VALUES ('O036', 'C001', '2025-06-20', 950000, 'pending', 1);
INSERT INTO orders VALUES ('O037', 'C015', '2025-05-08', 2600000, 'delivered', 3);
INSERT INTO orders VALUES ('O038', 'C017', '2025-06-02', 4100000, 'shipped', 5);
INSERT INTO orders VALUES ('O039', 'C012', '2025-04-15', 1300000, 'delivered', 2);
INSERT INTO orders VALUES ('O040', 'C019', '2025-06-18', 2000000, 'pending', 2);

-- Payments (35 rows)
CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT REFERENCES orders(order_id),
    paid_at TEXT,
    amount REAL,
    method TEXT,
    status TEXT
);

INSERT INTO payments VALUES ('P001', 'O001', '2025-01-05', 2500000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P002', 'O002', '2025-03-12', 1800000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P003', 'O003', '2025-02-20', 4200000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P004', 'O004', '2025-04-01', 750000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P005', 'O005', '2025-03-15', 3100000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P006', 'O006', '2025-05-08', 1200000, 'credit_card', 'pending');
INSERT INTO payments VALUES ('P007', 'O007', '2025-01-22', 5600000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P008', 'O008', '2025-04-10', 890000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P009', 'O009', '2025-02-14', 2100000, 'credit_card', 'refunded');
INSERT INTO payments VALUES ('P010', 'O010', '2025-05-20', 1650000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P011', 'O011', '2025-01-30', 3800000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P012', 'O012', '2025-03-25', 920000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P013', 'O013', '2025-06-01', 2750000, 'credit_card', 'pending');
INSERT INTO payments VALUES ('P014', 'O014', '2025-05-18', 4100000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P015', 'O015', '2025-04-22', 1350000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P016', 'O016', '2025-02-08', 680000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P017', 'O017', '2025-05-30', 2900000, 'bank_transfer', 'pending');
INSERT INTO payments VALUES ('P018', 'O018', '2025-06-05', 1100000, 'e-wallet', 'pending');
INSERT INTO payments VALUES ('P019', 'O019', '2025-05-12', 3400000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P020', 'O020', '2025-01-10', 7200000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P021', 'O021', '2025-03-05', 1900000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P022', 'O022', '2025-04-28', 550000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P023', 'O023', '2025-02-18', 2300000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P024', 'O024', '2025-06-10', 1750000, 'credit_card', 'pending');
INSERT INTO payments VALUES ('P025', 'O025', '2025-01-15', 4500000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P026', 'O026', '2025-04-02', 1600000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P027', 'O027', '2025-05-25', 890000, 'bank_transfer', 'pending');
INSERT INTO payments VALUES ('P028', 'O028', '2025-05-15', 3200000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P029', 'O029', '2025-06-08', 2100000, 'credit_card', 'pending');
INSERT INTO payments VALUES ('P030', 'O030', '2025-03-20', 1450000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P031', 'O032', '2025-01-28', 1050000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P032', 'O034', '2025-02-05', 2200000, 'credit_card', 'completed');
INSERT INTO payments VALUES ('P033', 'O037', '2025-05-08', 2600000, 'bank_transfer', 'completed');
INSERT INTO payments VALUES ('P034', 'O039', '2025-04-15', 1300000, 'e-wallet', 'completed');
INSERT INTO payments VALUES ('P035', 'O025', '2025-01-16', 0, 'credit_card', 'refunded');

-- Support Tickets (15 rows)
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id TEXT PRIMARY KEY,
    customer_id TEXT REFERENCES customers(customer_id),
    issue TEXT,
    status TEXT,
    priority TEXT,
    created_at TEXT,
    resolved_at TEXT
);

INSERT INTO support_tickets VALUES ('T001', 'C001', 'Order O002 arrived with damaged packaging', 'resolved', 'high', '2025-03-14', '2025-03-16');
INSERT INTO support_tickets VALUES ('T002', 'C003', 'Cannot track order O004 shipment', 'open', 'medium', '2025-04-05', NULL);
INSERT INTO support_tickets VALUES ('T003', 'C007', 'Request refund for cancelled order O009', 'resolved', 'high', '2025-02-15', '2025-02-20');
INSERT INTO support_tickets VALUES ('T004', 'C005', 'Payment pending for over 48 hours', 'in_progress', 'high', '2025-05-10', NULL);
INSERT INTO support_tickets VALUES ('T005', 'C009', 'Wrong item received in order O011', 'resolved', 'critical', '2025-02-02', '2025-02-05');
INSERT INTO support_tickets VALUES ('T006', 'C002', 'Request to upgrade membership tier', 'resolved', 'low', '2025-03-01', '2025-03-02');
INSERT INTO support_tickets VALUES ('T007', 'C012', 'Billing discrepancy on order O016', 'open', 'medium', '2025-02-10', NULL);
INSERT INTO support_tickets VALUES ('T008', 'C006', 'Late delivery for order O008', 'resolved', 'medium', '2025-04-15', '2025-04-17');
INSERT INTO support_tickets VALUES ('T009', 'C015', 'Request invoice for order O020', 'closed', 'low', '2025-01-12', '2025-01-12');
INSERT INTO support_tickets VALUES ('T010', 'C008', 'Product quality complaint', 'in_progress', 'high', '2025-05-22', NULL);
INSERT INTO support_tickets VALUES ('T011', 'C019', 'Account login issue', 'resolved', 'medium', '2025-04-05', '2025-04-06');
INSERT INTO support_tickets VALUES ('T012', 'C013', 'Requesting order cancellation for O017', 'open', 'high', '2025-06-01', NULL);
INSERT INTO support_tickets VALUES ('T013', 'C010', 'Promo code not applied', 'open', 'low', '2025-06-03', NULL);
INSERT INTO support_tickets VALUES ('T014', 'C004', 'Delivery address change request', 'in_progress', 'medium', '2025-06-06', NULL);
INSERT INTO support_tickets VALUES ('T015', 'C017', 'Warranty claim for defective product', 'open', 'high', '2025-06-08', NULL);
