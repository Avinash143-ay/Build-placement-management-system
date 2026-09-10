create database placement_system_1;
use placement_system_1;
CREATE TABLE admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL  
);

-- Students Table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    department VARCHAR(50),
    cgpa DECIMAL(3,2),
    placement_status ENUM('Placed', 'Not Placed') DEFAULT 'Not Placed',
    image longblob,
    company_placed VARCHAR(100),
    company_id INT,  
    password VARCHAR(255) NOT NULL
    
);

-- Companies Table
CREATE TABLE companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    industry VARCHAR(50),
    contact_email VARCHAR(100),
    contact_phone VARCHAR(15)
);

-- Job Openings Table
CREATE TABLE job_openings (
    job_id INT PRIMARY KEY ,
    company_id INT,
    job_title VARCHAR(100) NOT NULL,
    job_description TEXT,
    package DECIMAL(10,2),
    eligibility_criteria TEXT,
    last_date_to_apply DATE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
) ;

-- Job Applications Table
CREATE TABLE job_applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    job_id INT,
    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Automatically set to current timestamp
    status ENUM('Applied', 'Shortlisted', 'Rejected', 'Hired') DEFAULT 'Applied',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_openings(job_id) ON DELETE CASCADE
)  AUTO_INCREMENT = 301;

-- Placements Table
CREATE TABLE placements (
    placement_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    company_id INT,
    job_id INT,
    package DECIMAL(10,2),
    placement_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_openings(job_id) ON DELETE CASCADE
);

-- Interview Schedules Table
CREATE TABLE interview_schedules (
    interview_id INT PRIMARY KEY AUTO_INCREMENT,
    job_id INT,
    student_id INT,
    interview_date DATETIME,
    mode ENUM('Online', 'Offline'),
    status ENUM('Scheduled', 'Completed', 'Cancelled'),
    FOREIGN KEY (job_id) REFERENCES job_openings(job_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
) AUTO_INCREMENT = 401;

-- Feedback Table
CREATE TABLE feedback (
    feedback_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    company_id INT,
    job_id INT,
    feedback_text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Company Comments Table
CREATE TABLE company_comments (
    comment_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    student_id INT,
    comment_text TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Notifications Table
CREATE TABLE placement_statistics (
    department VARCHAR(50) PRIMARY KEY,
    total_students INT NOT NULL,
    placed_students INT NOT NULL,
    highest_package DECIMAL(10,2) NOT NULL,
    average_package DECIMAL(10,2) NOT NULL,
    placement_rate DECIMAL(5,2) NOT NULL 
);

INSERT INTO students (student_id, name, email, phone, department, cgpa, placement_status, company_id,image, password) VALUES
(221100, 'Amit Sharma', 'amit221100@iitgn.ac.in', '9876543210', 'CSE', 8.2, 'Placed', 101,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Passport-size-photo-Vivek-puri.jpg"), 'amitpass'),
(221101, 'Neha Verma', 'neha221101@iitgn.ac.in', '9876543211', 'ECE', 7.9, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\download.jpeg"), 'nehapass'),
(221102, 'Rahul Singh', 'rahul221102@iitgn.ac.in', '9876543212', 'ME', 8.5, 'Placed', 102,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men10.jpg"), 'rahulpass'),
(221103, 'Priya Patel', 'priya221103@iitgn.ac.in', '9876543213', 'CE', 7.8, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\download (5).jpeg"), 'priyapass'),
(221104, 'Karan Joshi', 'karan221104@iitgn.ac.in', '9876543214', 'EE', 8.0, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men 2.jpeg"), 'karanpass'),
(221105, 'Isha Mehta', 'isha221105@iitgn.ac.in', '9876543215', 'CSE', 8.4, 'Placed', 103, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\8c6a785483ee3e92d8163f2fac2cc567.jpg"),'ishapass'),
(221106, 'Manish Kumar', 'manish221106@iitgn.ac.in', '9876543216', 'ECE', 7.6, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men 3.jpeg"), 'manishpass'),
(221107, 'Sonal Gupta', 'sonal221107@iitgn.ac.in', '9876543217', 'ME', 8.3, 'Placed', 104,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\download (2).jpeg"), 'sonalpass'),
(221108, 'Vikram Thakur', 'vikram221108@iitgn.ac.in', '9876543218', 'CE', 7.7, 'Not Placed', NULL, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men4.jpeg"),'vikrampass'),
(221109, 'Divya Bansal', 'divya221109@iitgn.ac.in', '9876543219', 'EE', 8.1, 'Placed', 105, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\download (4).jpeg"),'divyapass'),
(221110, 'Anjali Reddy', 'anjali221110@iitgn.ac.in', '9876543220', 'CSE', 8.6, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\images (1).jpeg"), 'anjalipass'),
(221111, 'Rohit Malhotra', 'rohit221111@iitgn.ac.in', '9876543221', 'ECE', 7.5, 'Not Placed', NULL, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men5.jpeg"),'rohitpass'),
(221112, 'Pooja Desai', 'pooja221112@iitgn.ac.in', '9876543222', 'ME', 8.7, 'Placed', 106, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\images.jpeg"),'poojapass'),
(221113, 'Arun Mishra', 'arun221113@iitgn.ac.in', '9876543223', 'CE', 7.4, 'Not Placed', NULL, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men6.jpeg"),'arunpass'),
(221114, 'Swati Kapoor', 'swati221114@iitgn.ac.in', '9876543224', 'EE', 8.8, 'Placed', 107,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\prepare_light_b364e3ec37.webp"), 'swatipass'),
(221115, 'Rajesh Iyer', 'rajesh221115@iitgn.ac.in', '9876543225', 'CSE', 7.3, 'Not Placed', NULL, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men7.jpeg"),'rajeshpass'),
(221116, 'Deepa Nair', 'deepa221116@iitgn.ac.in', '9876543226', 'ECE', 8.9, 'Placed', 108,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\wo1.jpeg"), 'deepapass'),
(221117, 'Suresh Menon', 'suresh221117@iitgn.ac.in', '9876543227', 'ME', 7.2, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men8.jpeg"), 'sureshpass'),
(221118, 'Kavita Rao', 'kavita221118@iitgn.ac.in', '9876543228', 'CE', 9.0, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\wo2.jpeg"), 'kavitapass'),
(221119, 'Vivek Bhat', 'vivek221119@iitgn.ac.in', '9876543229', 'EE', 7.1, 'Placed', 109,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\men9.jpeg"), 'vivekpass'),
(221120, 'Meera Pillai', 'meera221120@iitgn.ac.in', '9876543230', 'BioTech', 8.2, 'Placed', 211,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\0.jpeg"), 'meerapass'),
(221121, 'Anand Dubey', 'anand221121@iitgn.ac.in', '9876543231', 'Chemical', 7.9, 'Placed', 212,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\1.jpeg"), 'anandpass'),
(221122, 'Sneha Kulkarni', 'sneha221122@iitgn.ac.in', '9876543232', 'Aerospace', 8.5, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\9.jpeg"), 'snehapass'),
(221123, 'Harsh Vardhan', 'harsh221123@iitgn.ac.in', '9876543233', 'Physics', 7.8, 'Placed', 214, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\2.jpeg"),'harshpass'),
(221124, 'Nisha Agarwal', 'nisha221124@iitgn.ac.in', '9876543234', 'Mathematics', 8.0, 'Placed', 215, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\8.jpeg"),'nishapass'),
(221125, 'Varun Nair', 'varun221125@iitgn.ac.in', '9876543235', 'BioTech', 8.3, 'Placed', 216, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\3.jpeg"),'varunpass'),
(221126, 'Ritika Sharma', 'ritika221126@iitgn.ac.in', '9876543236', 'Chemical', 7.7, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\7.jpeg"), 'ritikapass'),
(221127, 'Arjun Reddy', 'arjun221127@iitgn.ac.in', '9876543237', 'Aerospace', 8.6, 'Placed', 218, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\4.jpeg"),'arjunpass'),
(221128, 'Meghna Iyer', 'meghna221128@iitgn.ac.in', '9876543238', 'Physics', 8.1, 'Not Placed', NULL,load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\6.jpeg"), 'meghnapass'),
(221129, 'Siddharth Das', 'siddharth221129@iitgn.ac.in', '9876543239', 'Mathematics', 8.4, 'Placed', 220, load_file("C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\5.jpeg"),'siddharthpass');





INSERT INTO companies (company_id, name, industry, contact_email, contact_phone) VALUES
(101, 'Google', 'Technology', 'hr@google.com', '650-253-0000'),
(102, 'Microsoft', 'Technology', 'hr@microsoft.com', '425-882-8080'),
(103, 'Amazon', 'E-commerce', 'hr@amazon.com', '206-266-1000'),
(104, 'TCS', 'IT Services', 'hr@tcs.com', '022-6778-9999'),
(105, 'Bosch', 'Mechanical & Electronics', 'hr@bosch.com', '49-711-400'),
(106, 'L&T', 'Chemical & Infrastructure', 'hr@larsentoubro.com', '022-6752-5656'),
(107, 'Biocon', 'Biotechnology', 'hr@biocon.com', '080-2808-2808'),
(108, 'Reliance Chemicals', 'Chemical & Energy', 'hr@reliancechem.com', '022-3555-7000'),
(109, 'HAL', 'Aerospace & Defense', 'hr@hal-india.com', '080-2232-1234'),
(110, 'ISRO', 'Space Research', 'hr@isro.gov.in', '080-2217-2543');


INSERT INTO job_openings (job_id,company_id, job_title, job_description, package, eligibility_criteria, last_date_to_apply) VALUES
(201,101, 'Software Engineer', 'Develop and maintain software applications.', 250000.00, 'CGPA >= 8.0, Strong programming skills.', '2025-03-15'),
(202,101, 'AI Research Engineer', 'Work on AI/ML research projects.', 270000.00, 'CGPA >= 8.5, Experience in machine learning.', '2025-03-20'),
(203,102, 'Cloud Engineer', 'Design and implement cloud solutions.', 240000.00, 'CGPA >= 8.0, Experience with AWS/Azure.', '2025-03-18'),
(204,102, 'Cybersecurity Analyst', 'Ensure data security and prevent cyber threats.', 230000.00, 'CGPA >= 7.8, Knowledge of security protocols.', '2025-03-22'),
(205,103, 'DevOps Engineer', 'Automate and optimize deployment pipelines.', 220000.00, 'CGPA >= 7.5, Knowledge of CI/CD tools.', '2025-03-17'),
(206,103, 'Robotics Engineer', 'Develop automation and robotics for warehouses.', 210000.00, 'CGPA >= 8.0, Experience with embedded systems.', '2025-03-25'),
(207,104, 'Full Stack Developer', 'Develop scalable web applications.', 180000.00, 'CGPA >= 7.0, Proficiency in JavaScript.', '2025-03-19'),
(208,104, 'Embedded Systems Engineer', 'Work on microcontroller and IoT systems.', 175000.00, 'CGPA >= 7.5, Knowledge of C/C++.', '2025-03-23'),
(209,105, 'Automobile Engineer', 'Design automotive components and systems.', 190000.00, 'CGPA >= 7.0, Strong mechanical knowledge.', '2025-03-21'),
(210,105, 'Electronics Design Engineer', 'Develop embedded electronic systems.', 200000.00, 'CGPA >= 7.5, Experience with PCB design.', '2025-03-26'),
(211,106, 'Process Engineer', 'Work on chemical plant design and optimization.', 185000.00, 'CGPA >= 7.2, Strong chemical engineering background.', '2025-03-24'),
(212,106, 'Structural Engineer', 'Design infrastructure and buildings.', 195000.00, 'CGPA >= 7.5, Knowledge of AutoCAD and structural analysis.', '2025-03-28'),
(213,107, 'Biotech Research Associate', 'Conduct research on biopharmaceuticals and drug development.', 200000.00, 'CGPA >= 7.8, Background in biotechnology or life sciences.', '2025-03-20'),
(214,107, 'Genomics Data Analyst', 'Analyze genetic data using bioinformatics tools.', 210000.00, 'CGPA >= 8.0, Experience with Python and R.', '2025-03-25'),
(215,108, 'Chemical Process Engineer', 'Optimize chemical manufacturing processes.', 195000.00, 'CGPA >= 7.5, Strong background in chemical engineering.', '2025-03-22'),
(216,108, 'Materials Scientist', 'Develop new materials for industrial applications.', 205000.00, 'CGPA >= 8.0, Experience in material synthesis.', '2025-03-27'),
(217,109, 'Aerospace Engineer', 'Design and test aircraft components.', 220000.00, 'CGPA >= 8.2, Strong background in aerodynamics.', '2025-03-24'),
(218,109, 'Flight Simulation Engineer', 'Develop and maintain flight simulation software.', 215000.00, 'CGPA >= 7.8, Experience in MATLAB and Simulink.', '2025-03-29'),
(219,110, 'Astrophysics Researcher', 'Work on satellite-based research projects.', 230000.00, 'CGPA >= 8.5, Strong background in physics and mathematics.', '2025-03-21'),
(220,110, 'Data Scientist', 'Analyze space mission data using AI/ML techniques.', 240000.00, 'CGPA >= 8.0, Experience with Python and machine learning.', '2025-03-26');

INSERT INTO job_applications (student_id, job_id, application_date, status) VALUES
(221100, 201, '2025-02-28 10:15:00', 'Shortlisted'),
(221100, 202, '2025-02-28 10:20:00', 'Rejected'),
(221101, 203, '2025-02-28 10:25:00', 'Shortlisted'),
(221101, 204, '2025-02-28 10:30:00', 'Rejected'),
(221102, 202, '2025-02-28 10:35:00', 'Hired'),
(221102, 203, '2025-02-28 10:40:00', 'Shortlisted'),
(221103, 206, '2025-02-28 10:45:00', 'Shortlisted'),
(221103, 207, '2025-02-28 10:50:00', 'Rejected'),
(221104, 203, '2025-02-28 10:55:00', 'Rejected'),
(221104, 205, '2025-02-28 11:00:00', 'Shortlisted'),
(221105, 201, '2025-02-28 11:05:00', 'Hired'),
(221105, 202, '2025-02-28 11:10:00', 'Rejected'),
(221106, 205, '2025-02-28 11:15:00', 'Shortlisted'),
(221106, 206, '2025-02-28 11:20:00', 'Rejected'),
(221107, 207, '2025-02-28 11:25:00', 'Rejected'),
(221107, 208, '2025-02-28 11:30:00', 'Shortlisted'),
(221108, 208, '2025-02-28 11:35:00', 'Shortlisted'),
(221108, 209, '2025-02-28 11:40:00', 'Rejected'),
(221109, 209, '2025-02-28 11:45:00', 'Hired'),
(221109, 210, '2025-02-28 11:50:00', 'Shortlisted'),
(221110, 202, '2025-02-28 11:55:00', 'Rejected'),
(221110, 204, '2025-02-28 12:00:00', 'Shortlisted'),
(221111, 204, '2025-02-28 12:05:00', 'Shortlisted'),
(221111, 205, '2025-02-28 12:10:00', 'Shortlisted'),
(221112, 210, '2025-02-28 12:15:00', 'Hired'),
(221112, 211, '2025-02-28 12:20:00', 'Shortlisted'),
(221113, 211, '2025-02-28 12:25:00', 'Rejected'),
(221113, 212, '2025-02-28 12:30:00', 'Shortlisted'),
(221114, 212, '2025-02-28 12:35:00', 'Shortlisted'),
(221114, 201, '2025-02-28 12:40:00', 'Rejected'),
(221115, 207, '2025-02-28 12:45:00', 'Shortlisted'),
(221115, 208, '2025-02-28 12:50:00', 'Shortlisted'),
(221116, 201, '2025-02-28 12:55:00', 'Shortlisted'),
(221116, 202, '2025-02-28 13:00:00', 'Rejected'),
(221117, 211, '2025-02-28 13:05:00', 'Rejected'),
(221117, 212, '2025-02-28 13:10:00', 'Shortlisted'),
(221118, 212, '2025-02-28 13:15:00', 'Hired'),
(221118, 209, '2025-02-28 13:20:00', 'Shortlisted'),
(221119, 209, '2025-02-28 13:25:00', 'Shortlisted'),
(221119, 210, '2025-02-28 13:30:00', 'Rejected'),
(221120, 211, '2025-02-28 10:40:00', 'Hired'), 
(221120, 211, '2025-02-28 10:45:00', 'Rejected'), 
(221121, 212, '2025-02-28 10:50:00', 'Rejected'), 
(221121, 212, '2025-02-28 10:55:00', 'Hired'), 
(221122, 213, '2025-02-28 11:00:00', 'Rejected'), -- Sneha Kulkarni applying for Aerospace Engineer at HAL
(221122, 213, '2025-02-28 11:05:00', 'Rejected'), -- Sneha Kulkarni applying for Flight Simulation Engineer at HAL
(221123, 214, '2025-02-28 11:10:00', 'Hired'), -- Harsh Vardhan applying for Astrophysics Researcher at ISRO
(221123, 214, '2025-02-28 11:15:00', 'Rejected'), -- Harsh Vardhan applying for Data Scientist at ISRO
(221124, 215, '2025-02-28 11:20:00', 'Rejected'), -- Nisha Agarwal applying for Astrophysics Researcher at ISRO
(221124, 215, '2025-02-28 11:25:00', 'Hired'), -- Nisha Agarwal applying for Data Scientist at ISRO
(221125, 216, '2025-02-28 11:30:00', 'Rejected'), -- Varun Nair applying for Biotech Research Associate at Biocon
(221125, 216, '2025-02-28 11:35:00', 'Hired'), -- Varun Nair applying for Genomics Data Analyst at Biocon
(221126, 217, '2025-02-28 11:40:00', 'Rejected'), -- Ritika Sharma applying for Chemical Process Engineer at Reliance Chemicals
(221126, 217, '2025-02-28 11:45:00', 'Rejected'), -- Ritika Sharma applying for Materials Scientist at Reliance Chemicals
(221127, 218, '2025-02-28 11:50:00', 'Hired'), -- Arjun Reddy applying for Aerospace Engineer at HAL
(221127, 218, '2025-02-28 11:55:00', 'Rejected'), -- Arjun Reddy applying for Flight Simulation Engineer at HAL
(221128, 219, '2025-02-28 12:00:00', 'Rejected'), -- Meghna Iyer applying for Astrophysics Researcher at ISRO
(221128, 219, '2025-02-28 12:05:00','Rejected'), -- Meghna Iyer applying for Data Scientist at ISRO
(221129, 220, '2025-02-28 12:10:00', 'Rejected'), -- Siddharth Das applying for Astrophysics Researcher at ISRO
(221129, 220, '2025-02-28 12:15:00', 'Hired'); -- Siddharth Das applying for Data Scientist at ISRO



INSERT INTO placements (student_id, company_id, job_id, package, placement_date) VALUES
(221102, 101, 202, 270000.00, '2025-03-01'), 
(221105, 101, 201, 250000.00, '2025-03-02'),  
(221109, 105, 209, 190000.00, '2025-03-03'),  
(221112, 105, 210, 200000.00, '2025-03-04'),  
(221118, 106, 212, 195000.00, '2025-02-28'),
(221120, 106, 211, 185000.00, '2025-02-28'),
(221121, 106, 212, 195000.00, '2025-02-28'),
(221123, 107, 214, 210000.00, '2025-02-28'),
(221124, 108, 215, 195000.00, '2025-02-28'),
(221125, 108, 216, 205000.00, '2025-02-28'),
(221127, 109, 218, 215000.00, '2025-02-28'),
(221129, 110, 220, 240000.00, '2025-02-28');

 

INSERT INTO interview_schedules (student_id, job_id, interview_date, status, mode) VALUES
(221100, 201, '2025-03-01 09:00:00', 'Scheduled', 'Online'),
(221101, 203, '2025-03-01 09:30:00', 'Scheduled', 'Offline'),
(221102, 203, '2025-03-01 10:00:00', 'Scheduled', 'Online'),
(221103, 206, '2025-03-01 10:30:00', 'Scheduled', 'Offline'),
(221104, 205, '2025-03-01 11:00:00', 'Scheduled', 'Online'),
(221106, 205, '2025-03-01 11:30:00', 'Scheduled', 'Offline'),
(221107, 208, '2025-03-01 12:00:00', 'Scheduled', 'Online'),
(221108, 208, '2025-03-01 12:30:00', 'Scheduled', 'Offline'),
(221109, 210, '2025-03-01 13:00:00', 'Scheduled', 'Online'),
(221110, 204, '2025-03-01 13:30:00', 'Scheduled', 'Offline'),
(221111, 204, '2025-03-01 14:00:00', 'Scheduled', 'Online'),
(221111, 205, '2025-03-01 14:30:00', 'Scheduled', 'Offline'),
(221112, 211, '2025-03-01 15:00:00', 'Scheduled', 'Online'),
(221113, 212, '2025-03-01 15:30:00', 'Scheduled', 'Offline'),
(221114, 212, '2025-03-01 16:00:00', 'Scheduled', 'Online'),
(221115, 207, '2025-03-01 16:30:00', 'Scheduled', 'Offline'),
(221115, 208, '2025-03-01 17:00:00', 'Scheduled', 'Online'),
(221116, 201, '2025-03-01 17:30:00', 'Scheduled', 'Offline'),
(221117, 212, '2025-03-01 18:00:00', 'Scheduled', 'Online'),
(221118, 209, '2025-03-01 18:30:00', 'Scheduled', 'Offline'),
(221119, 209, '2025-03-01 19:00:00', 'Scheduled', 'Online');

INSERT INTO feedback (feedback_id, student_id, company_id, job_id, feedback_text, rating, feedback_date) VALUES
(1, 221100, 101, 201, 'The interview process was smooth and well-structured.', 5, '2025-03-02'),
(2, 221101, 102, 203, 'The technical round was challenging but fair.', 4, '2025-03-02'),
(3, 221102, 103, 203, 'The hiring team was very supportive and answered all my queries.', 5, '2025-03-03'),
(4, 221103, 104, 206, 'I expected more clarity in the interview questions.', 3, '2025-03-03'),
(5, 221104, 105, 205, 'Good experience overall, but the HR round took too long.', 4, '2025-03-04'),
(6, 221105, 101, 201, 'Excited to join! The process was efficient.', 5, '2025-03-05'),
(7, 221106, 105, 205, 'Wish I had received more feedback on my performance.', 3, '2025-03-05'),
(8, 221107, 106, 208, 'The coding round was tough but enjoyable.', 4, '2025-03-06'),
(9, 221108, 106, 208, 'It took too long to receive my interview results.', 3, '2025-03-06'),
(10, 221109, 103, 210, 'Great company culture, looking forward to joining!', 5, '2025-03-07'),
(11, 221110, 104, 204, 'The interviewers were very professional.', 5, '2025-03-07'),
(12, 221111, 104, 204, 'The process was smooth, but the questions were quite generic.', 4, '2025-03-08'),
(13, 221112, 106, 211, 'Happy with the entire process! Quick responses from HR.', 5, '2025-03-08'),
(14, 221113, 106, 212, 'Would have liked more time to prepare for the interview.', 3, '2025-03-09'),
(15, 221114, 106, 212, 'Good experience, but could be more streamlined.', 4, '2025-03-09'),
(16, 221115, 106, 207, 'The HR team was responsive and helpful.', 5, '2025-03-10'),
(17, 221116, 101, 201, 'Fair interview questions, but the process was lengthy.', 4, '2025-03-10'),
(18, 221117, 106, 212, 'I felt the test questions were not relevant to the job role.', 3, '2025-03-11'),
(19, 221118, 106, 209, 'Excited to be selected! Great experience.', 5, '2025-03-11'),
(20, 221119, 103, 209, 'The company was very welcoming and supportive.', 5, '2025-03-12');

INSERT INTO company_comments (comment_id, company_id, student_id, comment_text) VALUES
(1, 101, 221100, 'Amit showcased excellent problem-solving skills and confidence.'),
(2, 102, 221101, 'Neha demonstrated solid technical knowledge but should enhance communication.'),
(3, 103, 221102, 'Rahul had a structured approach but needed more clarity on complex problems.'),
(4, 104, 221103, 'Priya was well-prepared but needs to improve response structuring.'),
(5, 105, 221104, 'Karan has strong analytical skills but needs to be more concise.'),
(6, 105, 221106, 'Manish was a good candidate but should work on articulating ideas better.'),
(7, 106, 221107, 'Sonal had impressive coding skills but lacked confidence in HR discussions.'),
(8, 106, 221108, 'Vikram was detail-oriented and had great problem-solving abilities.'),
(9, 103, 221109, 'Divya had excellent domain knowledge and communication skills.'),
(10, 104, 221110, 'Anjali was confident and answered all technical questions well.'),
(11, 104, 221111, 'Rohit performed decently but should improve on structured problem-solving.'),
(12, 106, 221112, 'Pooja was an outstanding candidate with strong analytical abilities.'),
(13, 106, 221113, 'Arun showed good problem-solving ability but lacked confidence.'),
(14, 106, 221114, 'Swati performed consistently and showed great enthusiasm.'),
(15, 106, 221115, 'Rajesh was technically sound and handled tricky questions well.'),
(16, 101, 221116, 'Deepa had good domain expertise but needs to work on time management.'),
(17, 106, 221117, 'Suresh was a solid candidate but should focus on leadership skills.'),
(18, 106, 221118, 'Kavita showed passion for the role and adapted quickly to new problems.'),
(19, 103, 221119, 'Vivek was a well-rounded candidate, good fit for our company culture.'),
(20, 106, 221105, 'Isha had excellent problem-solving skills and communicated ideas well.');

INSERT INTO placement_statistics (department, total_students, placed_students, placement_rate, highest_package, average_package) VALUES
('CSE', 4, 2, (1.0 / 4) * 100, 250000.00, (250000.00 + 0) / 2),
('ECE', 4, 1, (1.0 / 4) * 100, 270000.00, (270000.00 + 0) / 1),
('ME', 4, 1, (1.0 / 4) * 100, 200000.00, (200000.00 + 0) / 1),
('CE', 4, 0, (0.0 / 4) * 100, 0, 0),
('EE', 4, 1, (1.0 / 4) * 100, 195000.00, (195000.00 + 0) / 1),
('BioTech', 2, 2, (2.0 / 2) * 100, 205000.00, (185000.00 + 205000.00) / 2),
('Chemical', 2, 1, (1.0 / 2) * 100, 195000.00, (195000.00 + 0) / 1),
('Aerospace', 2, 1, (1.0 / 2) * 100, 215000.00, (215000.00 + 0) / 1),
('Physics', 2, 1, (1.0 / 2) * 100, 210000.00, (210000.00 + 0) / 1),
('Mathematics', 2, 1, (2.0 / 2) * 100, 240000.00, (195000.00 + 240000.00) / 2);




select *from students;