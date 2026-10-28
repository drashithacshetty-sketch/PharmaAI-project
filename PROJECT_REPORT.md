# II SEMESTER PROJECT REPORT ON

# PHARMAAI: SMART PHARMACY INVENTORY AND DEMAND FORECASTING SYSTEM

**Submitted in partial fulfilment of the requirements for the award of the degree of**

### MASTER OF COMPUTER APPLICATIONS (MCA)
**During the Academic Year 2025 – 2026**

---

**Submitted By:**
* **Candidate 1**: Register No.: `25MCAC01`
* **Candidate 2**: Register No.: `25MCAC02`

**Under the guidance of:**
* **Internal Guide**: Dr. Assistant Professor
* Department of Computer Applications
* Kristu Jayanti Institute of Technology
* Kristu Jayanti (Deemed to be University), K. Narayanapura, Kothanur P.O., Bengaluru – 560077

---

## BONAFIDE CERTIFICATE

This is to certify that the project report entitled **"PHARMAAI: SMART PHARMACY INVENTORY AND DEMAND FORECASTING SYSTEM"** is a bonafide record of the software engineering project work carried out by **Candidate 1 (Register No.: 25MCAC01)** and **Candidate 2 (Register No.: 25MCAC02)**, students of the Master of Computer Applications (MCA) program at Kristu Jayanti Institute of Technology, Kristu Jayanti Deemed to be University, Bengaluru, in partial fulfillment of the academic requirements for the award of the degree of Master of Computer Applications during the academic year 2025–2026.

The project implementation, source code repository, and accompanying technical documentation represent original work conducted under my supervision and have not been submitted previously, in part or in full, for the award of any other degree, diploma, or fellowship at this or any other university.

<br><br>

-------------------------------------------- &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; --------------------------------------------
**Internal Guide / Project Supervisor** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Head of the Department**
Department of Computer Applications &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Department of Computer Applications
Kristu Jayanti (Deemed to be University) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Kristu Jayanti (Deemed to be University)

<br>

**Submitted for the University Viva-Voce Examination held on:** ____________________

**Internal Examiner:** ____________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **External Examiner:** ____________________

---

## ACKNOWLEDGMENT

We would like to express our gratitude to everyone who helped us plan, build, test, and complete the **PharmaAI** project. Working on this system gave us practical experience in addressing real-world pharmacy supply chain issues, combining web engineering with machine learning.

First, we thank the Almighty for giving us the health, focus, and strength to carry out this project through every stage of development.

We express our sincere thanks to the Management and the **Vice-Chancellor** of Kristu Jayanti (Deemed to be University), Bengaluru, for providing us with modern computer laboratories, reliable internet connectivity, and a supportive learning environment.

We are deeply grateful to our **Head of the Department**, Department of Computer Applications, for encouraging practical software development, setting clear academic milestones, and providing constructive feedback during periodic reviews.

Our special thanks go to our **Project Guide and Supervisor**, whose practical guidance kept us on track. From refining our database design to helping us tune the First-Expiry, First-Out (FEFO) dispensing logic and validate the machine learning model, their suggestions were invaluable.

Finally, we thank our professors, lab instructors, classmates, and families for their constant encouragement, patience, and helpful suggestions throughout this semester.

**Candidates (MCA 2025–2026)**

---

## ABSTRACT

Managing pharmacy inventory is very different from managing standard retail goods. Every strip of tablets, vial of syrup, and box of capsules comes with a fixed expiration date, a manufacturer batch code, and strict rules against selling expired medicines. In most local chemist shops and community hospital dispensaries, staff still rely on manual notebooks, simple retail cash registers, or basic spreadsheets. When new stock arrives, workers often stack the fresh cartons right in front of older ones on the shelf. As a result, older medicines sit neglected at the back until they expire, causing direct financial loss to the pharmacy. At the same time, sudden spikes in patient illnesses—such as seasonal fevers or respiratory infections—frequently catch pharmacies unprepared, leading to stockouts of essential medicines.

To tackle these everyday operational headaches, we built **PharmaAI**, a web-based pharmacy inventory and demand prediction system. The application is developed with a Python and Flask backend, uses an SQLAlchemy-managed relational database, and runs on a responsive Bootstrap 5 interface that works smoothly on standard desktop monitors and counter tablets. 

The core feature of PharmaAI is automated **First-Expiry, First-Out (FEFO)** batch management. When a staff member bills a customer at the counter, the system automatically draws stock from the active batch that expires earliest, rather than simply taking from the newest delivery. If any batch has already crossed its expiration date, the system immediately blocks it from being billed and tags it for safe disposal. 

To help store owners order stock proactively, the system includes a **Random Forest Regression** model trained on historical sales figures. The model analyzes past consumption trends, rolling 7-day and 14-day averages, and day-of-week patterns to forecast medicine requirements for the upcoming week and month. Using these forecasts alongside distributor delivery lead times, PharmaAI calculates realistic safety stock levels and automated Reorder Points (ROP) that match commercial pack sizes. Role-Based Access Control keeps administrative, clinical, and billing duties clearly separated, while an immutable audit log tracks every stock movement. Testing showed that the system reliably prevents the sale of expired drugs, reduces stockout risks, and simplifies daily pharmacy operations.

---

## TABLE OF CONTENTS

### Table 0.1: Master Table of Contents

| CHAPTER NO | TITLE | PAGE NO |
| :--- | :--- | :--- |
| | **TITLE PAGE** | i |
| | **BONAFIDE CERTIFICATE** | ii |
| | **ACKNOWLEDGMENT** | iii |
| | **ABSTRACT** | iv |
| | **TABLE OF CONTENTS** | v |
| | **LIST OF TABLES** | vii |
| | **LIST OF FIGURES** | viii |
| **CHAPTER 1** | **INTRODUCTION** | **1** |
| 1.1 | Problem Statement | 1 |
| 1.2 | Project Description | 4 |
| 1.2.1 | Module Description | 6 |
| **CHAPTER 2** | **SYSTEM STUDY** | **9** |
| 2.1 | Existing System and Practical Limitations | 9 |
| 2.2 | Proposed System and Operational Advantages | 11 |
| 2.3 | Use Case Diagram and Actor Analysis | 14 |
| 2.4 | Sequential Diagram and Dispensing Workflow | 17 |
| 2.5 | Activity Diagram and Decision Flows | 20 |
| **CHAPTER 3** | **SYSTEM CONFIGURATION** | **23** |
| 3.1 | Hardware Configuration | 23 |
| 3.2 | Software Configuration and Libraries | 25 |
| **CHAPTER 4** | **SOFTWARE DESCRIPTION** | **28** |
| 4.1 | Front End User Interface and Experience | 28 |
| 4.2 | Back End Architecture and Service Layers | 31 |
| 4.3 | Machine Learning Demand Forecasting Pipeline | 34 |
| **CHAPTER 5** | **SYSTEM DESIGN** | **37** |
| 5.1 | Architectural Design | 37 |
| 5.2 | Input Design and Validation Rules | 40 |
| 5.3 | Output Design and Billing Layouts | 43 |
| 5.4 | Database Design and Schema Specification | 46 |
| **CHAPTER 6** | **SOURCE CODE** | **55** |
| 6.1 | Core FEFO Batch Allocation and Dispensing Engine | 55 |
| **CHAPTER 7** | **SYSTEM TESTING** | **63** |
| 7.1 | Testing Approach and Objectives | 63 |
| 7.2 | Detailed Test Cases (TC-01 to TC-12) | 65 |
| 7.3 | Master Test Matrix and Results Summary | 74 |
| **CHAPTER 8** | **SYSTEM IMPLEMENTATION AND DEPLOYMENT** | **78** |
| 8.1 | Environment Setup and Configuration | 78 |
| 8.2 | Step-by-Step Installation and Run Guide | 81 |
| **CHAPTER 9** | **CONCLUSION AND FUTURE SCOPE** | **84** |
| 9.1 | Conclusion | 84 |
| 9.2 | Future Scope and Enhancements | 85 |
| **CHAPTER 10**| **APPENDICES** | **87** |
| 10.1 | Application Interface Screenshots and Walkthrough | 87 |
| **CHAPTER 11**| **REFERENCES AND BIBLIOGRAPHY** | **94** |

---

### Table 0.2: Master List of Tables

| TABLE NO | TABLE TITLE | PAGE NO |
| :--- | :--- | :--- |
| Table 2.1 | Comparison Between Traditional Pharmacy Methods and PharmaAI | 13 |
| Table 3.1 | Minimum and Recommended Hardware Specifications | 24 |
| Table 3.2 | Software Frameworks, Versions, and Their Roles in the Project | 26 |
| Table 4.1 | Application Route Namespaces, Assigned Controllers, and Access Permissions | 33 |
| Table 5.1 | Form Input Validation Constraints Across Application Modules | 42 |
| Table 5.2 | Users Table Schema (`users`) | 48 |
| Table 5.3 | Medicines Table Schema (`medicines`) | 49 |
| Table 5.4 | Batches Table Schema (`batches`) | 50 |
| Table 5.5 | Sales Table Schema (`sales`) | 51 |
| Table 5.6 | Sale Items Table Schema (`sale_items`) | 52 |
| Table 5.7 | Purchase Orders Table Schema (`purchase_orders`) | 53 |
| Table 5.8 | Stock Movements Audit Table Schema (`stock_movements`) | 54 |
| Table 7.1 | Summary of Test Cases and Verification Outcomes | 75 |
| Table 8.1 | Environment Variables and Configuration Parameters | 80 |

---

### Table 0.3: Master List of Figures

| FIGURE NO | FIGURE TITLE | PAGE NO |
| :--- | :--- | :--- |
| Figure 2.1 | Use Case Diagram of the PharmaAI System | 15 |
| Figure 2.2 | Sequence Diagram of the Automated FEFO Dispensing Process | 18 |
| Figure 2.3 | Activity Diagram Showing Inventory Handling, Sales, and Disposal | 21 |
| Figure 5.1 | Four-Tier System Architecture of PharmaAI | 38 |
| Figure 5.2 | Entity-Relationship (ER) Diagram of the Relational Database | 47 |
| Figure 10.1 | Secure Login Screen with Role-Based Redirection | 88 |
| Figure 10.2 | Real-Time Operations and Stock Status Dashboard | 89 |
| Figure 10.3 | Medicine Inventory and Batch Overview Screen | 90 |
| Figure 10.4 | Multi-Tier Expiration Alert and Safe Disposal Panel | 91 |
| Figure 10.5 | Machine Learning Demand Prediction and Trend Analysis Screen | 92 |
| Figure 10.6 | Reorder Suggestions and Supplier Purchase Order Generator | 93 |
| Figure 10.7 | Point-of-Sale (POS) Billing Counter with Live Batch Breakdown | 94 |

---

# CHAPTER 1: INTRODUCTION

Running a pharmacy or medical dispensary involves a delicate balance between public safety and business efficiency. Unlike general supermarkets where products have long shelf lives or can simply be marked down when old, pharmacies deal with regulated chemical drugs that lose potency or become hazardous after their expiration date. Every medicine strip, bottle, and vial has a specific batch number, an exact expiry date, and strict legal requirements about who can dispense it and how it must be recorded.

In everyday practice, a pharmacy staff member must receive deliveries from wholesale distributors, check the cartons against paper delivery challans, update stock records, place medicines on storage shelves, handle walk-in customers with prescriptions, calculate totals, check if any stock is running low, and discard medicines that have expired. When a pharmacy handles hundreds of different drugs, tracking all these moving parts by memory or on paper becomes almost impossible. Mistakes easily creep in: an older batch gets pushed into a corner and forgotten until it expires, or a high-demand fever syrup suddenly runs out on a weekend when distributors are closed.

**PharmaAI** was created to solve these exact problems. It is a web-based pharmacy management and predictive inventory platform designed for everyday use in retail chemist shops and hospital dispensaries. By combining a clean, responsive web interface with a Python/Flask backend and machine learning forecasting, the system automates First-Expiry, First-Out (FEFO) dispensing, alerts staff well before drugs expire, and helps owners reorder stock based on actual consumption patterns rather than guesswork.

---

## 1.1 Problem Statement

Even though many businesses have switched to modern digital tools, a surprising number of local pharmacies and dispensary counters still use outdated methods. Many rely on basic cash-register software that only records the total bill amount, standalone spreadsheets that quickly get out of sync, or handwritten stock registers. These legacy tools fail to track medicines at the individual batch level and have no ability to look ahead at patient demand.

The main challenge PharmaAI addresses is the lack of an integrated, batch-aware software system that can automatically manage drug shelf life and predict future medicine needs. Five practical issues stand out in traditional pharmacy setups:

1. **Medicines Expiring on Back Shelves (Lack of FEFO Enforcement):**
   When fresh shipments arrive, busy helpers often put the new boxes right at the front of the shelf because it is faster. As a result, older boxes get pushed further back. When dispensing to customers, counter staff naturally reach for the closest box. Over months, older batches quietly sit uninspected until they pass their expiry date. The pharmacy takes a direct financial loss, and there is always a dangerous risk that an expired strip might accidentally be handed to a customer during rush hours.

2. **Unexpected Stockouts of Critical Medicines:**
   Patient demand changes quickly. Seasonal flu outbreaks, sudden weather shifts, or doctors prescribing a popular new antibiotic can rapidly clear out a pharmacy's stock. Without predictive tools, pharmacists only realize a medicine is finished when they open a drawer and find it empty. Patients are left stranded, and the pharmacy loses business while waiting days for a distributor delivery.

3. **Haphazard Reordering and Pack-Size Mismatches:**
   Most reordering is done reactively. At the end of the day or week, the pharmacist glances through the shelves and writes a list of depleted items on a notepad. This method ignores lead times—the 2 to 5 days a distributor takes to deliver. Furthermore, distributors sell medicines in boxes of 10 or 20 strips, not individual units. Without automated calculations, pharmacists often guess how much to order, leading to over-purchasing slow drugs and under-purchasing fast ones.

4. **Incomplete Audit Trails and Accountability Gaps:**
   Drug inspectors and healthcare regulators require pharmacies to maintain clear records of where medicines came from and where they went. In manual systems or basic spreadsheets, entries can easily be deleted, edited, or skipped. If physical stock does not match the register, there is no reliable way to know whether the difference came from unbilled sales, breakage, theft, or untracked disposal.

5. **Counter Bottlenecks During Peak Billing Hours:**
   In the evening, when clinic patients arrive with prescriptions, counter staff face heavy queues. If staff have to manually search through drawers, read tiny batch numbers printed on foil strips, and look up prices, the billing process slows down significantly, leading to long customer wait times and clerical errors.

---

## 1.2 Project Description

**PharmaAI** is built as an end-to-end, multi-tier web application designed to make daily pharmacy work faster, safer, and more organized. Every medicine is tracked from the moment it is received from a distributor to the moment it is handed to a customer at the billing counter.

The application is structured into four main layers:

* **Presentation Layer (`templates/` and `static/`):** A responsive web interface built using Jinja2 template inheritance, HTML5, and Bootstrap 5. It uses clear visual cards, color-coded status badges, and lightweight JavaScript so that counter staff can search medicines and complete sales quickly without waiting for full page reloads.
* **Application and Service Layer (`routes/` and `services/`):** The backend is written in Python using Flask. We organized the code by separating URL routing (`routes/`) from the actual business logic (`services/`). Services like `InventoryService`, `SalesService`, and `ReorderService` handle all calculations, ensuring the code is modular and easy to maintain.
* **Machine Learning Intelligence Layer (`ml/`):** A forecasting pipeline built with Scikit-Learn. It takes historical daily sales figures, computes rolling moving averages, day-of-week trends, and recent demand lags, and uses a Random Forest Regressor to forecast upcoming 7-day and 30-day medicine demand.
* **Data Persistence Layer (`models/` and Database):** Built using SQLAlchemy Object-Relational Mapping (ORM). The relational schema enforces referential integrity, foreign key links, and atomic transactions. It runs on SQLite for development and testing, and can switch to PostgreSQL or MySQL in production with a simple configuration change.

---

### 1.2.1 Module Description

To keep the application clean and easy to maintain, the features are divided into seven core modules:

#### 1. Authentication and Role-Based Access Control (RBAC) Module
Protects the system and ensures that users only see the features they need:
* **Administrator:** Has full authority over user accounts, master catalog pricing, supplier setups, and high-level reports.
* **Pharmacist:** Manages clinical inventory, registers new medicines, logs incoming distributor batches, runs expired batch disposals, reviews AI demand forecasts, and creates purchase orders.
* **Staff:** Focuses on customer service, operating the Point-of-Sale (POS) billing counter, searching available stock, and printing receipts.

#### 2. Medicine Catalog and Inventory Module
Serves as the master directory for all pharmaceutical products. Each record includes the commercial brand name, generic chemical composition, clinical category (e.g., Antibiotic, Analgesic, Cardiovascular), dosage form (Tablet, Capsule, Syrup), unit strength (e.g., 500mg), and default reorder thresholds.

#### 3. FEFO Batch Management and Expiry Tracking Module
Allows multiple batches to exist under a single medicine. Each batch stores its unique batch code, manufacturing date, expiration date, cost price, selling price, and remaining quantity. The system automatically classifies batches into visual risk tiers:
* **Critical (Red):** Expires within 7 days.
* **Expiring Soon (Yellow):** Expires within 30 days.
* **Normal (Green):** More than 30 days of shelf life remaining.
* **Expired (Black/Gray):** Past its expiration date; locked from billing and flagged for disposal.

#### 4. Machine Learning Demand Forecasting Module
Takes the guesswork out of ordering. By analyzing past daily sales, the Random Forest model learns weekly rhythms and seasonal shifts. It outputs projected unit needs for the next 7 and 30 days along with Mean Absolute Error (MAE) benchmarks to help pharmacists plan ahead.

#### 5. Smart Reorder and Procurement Module
Connects the forecast to everyday purchasing. It calculates the Reorder Point (ROP) by combining expected sales during distributor lead time with a calculated safety stock buffer. When stock drops below this point, the system creates a purchase order recommendation that automatically rounds up to full supplier pack sizes.

#### 6. Point-of-Sale (POS) Billing Module
Designed for fast counter service. Staff select the medicine and enter the requested quantity. The backend FEFO algorithm automatically pulls units from the active batch expiring earliest, calculates line subtotals, prevents any expired items from being billed, generates a clean invoice number (`INV-YYYYMMDDHHMM-XXXX`), and prints a neat receipt.

#### 7. Analytics and Audit Reporting Module
Gives owners a clear overview through dashboard KPI cards (Usable Stock, Near-Expiry Units, Monthly Sales, Pending Orders). It also allows exporting inventory valuation lists, sales history, and disposal logs to CSV files for accounting and inspections.

---

# CHAPTER 2: SYSTEM STUDY

## 2.1 Existing System and Practical Limitations

Before designing PharmaAI, we observed how local pharmacies and small hospital dispensaries manage their day-to-day work. Most operate using traditional, manual routines:

1. **Delivery Receipts on Paper:** When delivery cartons arrive from distributors, the pharmacist or an assistant checks the physical delivery paper, manually enters the details into a register book or a basic spreadsheet, and files the paper bill in a binder.
2. **Unordered Storage on Shelves:** Cartons are placed on shelves wherever there is free space. In the rush of daily work, newly delivered boxes are frequently placed on top of or in front of older boxes.
3. **Flat Billing Without Batch Tracking:** When a customer purchases a strip of tablets, the counter person rings up the sale on a simple billing machine that only prints the drug name and total price. The specific batch code and expiration date are rarely recorded on the bill.
4. **Occasional Manual Expiry Checks:** Once every few months, staff spend hours physically taking boxes off shelves, squinting at the small printed expiry dates, and making handwritten lists of near-expiry items.

### Practical Limitations of the Traditional Approach

* **Heavy Financial Losses from Expired Stock:** Because there is no automatic system ensuring older stock gets sold first, medicines often expire unnoticed on back shelves, costing the pharmacy thousands of rupees annually.
* **Safety Risks for Patients:** With manual handling, there is always a chance that an inattentive or tired counter clerk might pick up an expired box during a busy shift and sell it to a patient.
* **Frequent Stockouts of Essential Drugs:** Because reordering depends on someone noticing an empty box on the shelf, fast-moving medicines frequently run out before a replacement order can arrive.
* **Clerical Errors During Counter Rush Hours:** Calculating discounts, looking up prices across different batches, and manually writing out receipts during peak evening hours leads to billing mistakes and long queues.
* **Vulnerable, Incomplete Records:** Paper notebooks get damaged, stained, or misplaced, and standalone Excel files can be accidentally overwritten or deleted with no way to trace who made changes.

---

## 2.2 Proposed System and Operational Advantages

**PharmaAI** was designed to replace these error-prone manual routines with an organized, automated digital platform. By combining a modern web interface with a relational database and machine learning, the system addresses both immediate counter billing and long-term procurement planning.

### Operational Advantages of PharmaAI

1. **Automatic FEFO Priority Allocation:** When a medicine is billed, the software automatically assigns units from the batch that expires earliest. Staff do not need to spend time checking dates manually—the software handles it behind the scenes.
2. **Predictive Ordering with Machine Learning:** Instead of waiting for stock to run out, the Random Forest model analyzes past sales and alerts the pharmacist ahead of time, ensuring sufficient stock is ordered before seasonal demand picks up.
3. **Dynamic Reorder Points and Safety Stock:** The system calculates realistic safety stock levels based on daily consumption and distributor delivery times, recommending replenishment in practical supplier pack sizes.
4. **Three-Tier Role-Based Security:** Separate logins for Admins, Pharmacists, and Billing Staff keep clinical and financial duties secure while preventing unauthorized changes.
5. **Permanent Audit Trail for Every Unit:** Every action—adding stock, billing a customer, or disposing of damaged goods—is permanently recorded with the staff member's name and an exact timestamp.
6. **Fast, Lightweight Web Interface:** Built on Bootstrap 5 and Flask, the application runs smoothly on ordinary counter computers and tablets without requiring expensive hardware.

---

### Table 2.1: Comparison Between Traditional Pharmacy Methods and PharmaAI

| Operational Area | Traditional Pharmacy Setup | PharmaAI Platform |
| :--- | :--- | :--- |
| **Data Record Keeping** | Handwritten paper notebooks and isolated Excel files | Centralized relational database managed with SQLAlchemy ORM |
| **Stock Dispensing Method** | Random selection; often Last-In, First-Out (LIFO) because new boxes sit in front | Automated First-Expiry, First-Out (FEFO) queue that always picks the earliest-expiring batch |
| **Expiration Monitoring** | Irregular visual shelf checks; high chance of missing expiring stock | Real-time color-coded alerts (Critical ≤7 days, Warning ≤30 days, Normal, Expired) |
| **Demand Planning** | Guesswork and intuition based on what looks empty | Machine learning (Random Forest) analyzing trends, seasonality, and moving averages |
| **Reorder Calculation** | Reactive ordering after an item is completely out of stock | Dynamic Reorder Point ($\text{ROP} = \text{Lead Time Sales} + \text{Safety Stock}$) with pack rounding |
| **Billing & Receipts** | Hand-written bills or flat POS receipts without batch codes | One-click POS billing with automated batch breakdown and clean printable invoices |
| **Audit & Accountability** | No user tracking; changes can be made or lost without accountability | Role-based permissions and an immutable log of every stock movement |
| **Hardware Demands** | Prone to paper wear and tear; no network backup | Lightweight web app deployable on counter PCs, tablets, or cloud servers |

---

## 2.3 Use Case Diagram and Actor Analysis

The Use Case Diagram illustrates how different users interact with the system based on their daily responsibilities. PharmaAI defines three distinct user roles:

1. **Administrator (`ADMIN`):** Manages user accounts, configures overall system settings, approves large purchase orders, and reviews executive financial summaries.
2. **Pharmacist (`PHARMACIST`):** Focuses on medicine inventory, adds new drug formulations, enters arriving distributor batches, runs safe disposal of expired stock, checks AI demand forecasts, and creates reorders.
3. **Staff (`STAFF`):** Handles front-counter billing, checks medicine availability, and prints customer receipts.

```
                    +---------------------------------------------------+
                    |                   PharmaAI                    |
                    +---------------------------------------------------+
                    |                                                   |
( Admin ) --------->| [UC-01] Authenticate & Manage Session             |
   |   |            | [UC-02] Manage User Accounts & Permissions        |<--- ( Pharmacist )
   |   +----------->| [UC-03] Manage Medicine Catalog & Formulations    |         |
   |                | [UC-04] Receive Batches & Inspect FEFO Stock      |---------+
   |                | [UC-05] Review Expiry Tiers & Perform Disposal    |---------+
   |                | [UC-06] Run ML Demand Forecast & View Projections |---------+
   +--------------->| [UC-07] Create, Review & Receive Purchase Orders  |---------+
   |                | [UC-08] Process POS Sale with Auto-FEFO Dispense  |---------+--- ( Staff )
   |                | [UC-09] Check Stock Balance & Batch Expiry Dates  |---------+-------+
   +--------------->| [UC-10] Export Audit Logs & CSV Analytics Reports |                 |
                    |                                                   |                 |
                    +---------------------------------------------------+
```

### Detailed Actor Interaction Analysis

* **Step 1 (Login):** Every user starts by logging in through **Authenticate & Manage Session (UC-01)**. Passwords are checked against salted hashes, and a session is created matching the user's role.
* **Administrative Scope:** The **Administrator** alone can add or deactivate user accounts via **Manage User Accounts (UC-02)** and holds final authority over **Purchase Order Approvals (UC-07)** and **Exporting Master Reports (UC-10)**.
* **Clinical & Inventory Scope:** The **Pharmacist** maintains drug information via **Manage Medicine Catalog (UC-03)**, logs new shipments via **Receive Batches (UC-04)**, disposes of expired units safely via **Review Expiry Tiers & Disposal (UC-05)**, and inspects future needs using **Run ML Demand Forecast (UC-06)**.
* **Counter Billing Scope:** The **Staff** member handles customers through **Process POS Sale (UC-08)** and looks up medicines using **Check Stock Balance (UC-09)**. Billing staff cannot alter wholesale prices or delete audit logs.

---

## 2.4 Sequential Diagram and Dispensing Workflow

The Sequence Diagram shows the step-by-step communication between the user interface, backend route handlers, service classes, and the database during a customer purchase:

```
Staff / User         POS UI (Client)         SalesRoute         SalesService         InventoryService         Database (ORM)
     |                      |                     |                   |                      |                      |
     |--- 1. Select Meds -->|                     |                   |                      |                      |
     |    & Quantities      |                     |                   |                      |                      |
     |--- 2. Click Checkout>|                     |                   |                      |                      |
     |                      |--- 3. POST /sales ->|                   |                      |                      |
     |                      |       (JSON Data)   |--- 4. process() ->|                      |                      |
     |                      |                     |                   |--- 5. allocate_fefo->|                      |
     |                      |                     |                   |       (med_id, qty)  |--- 6. Query Batches->|
     |                      |                     |                   |                      |    (ORDER BY expiry) |
     |                      |                     |                   |                      |<-- 7. Active Batches-|
     |                      |                     |                   |                      |                      |
     |                      |                     |                   |<-- 8. Allocations ---|                      |
     |                      |                     |                   |    [(Batch1, qty)]   |                      |
     |                      |                     |                   |                      |                      |
     |                      |                     |                   |--- 9. Check Not Expired -------------------->|
     |                      |                     |                   |--- 10. Deduct Stock & Create Line Items ---->|
     |                      |                     |                   |--- 11. Write Audit Log Entries ------------->|
     |                      |                     |                   |--- 12. Update Daily Sales Aggregates ------->|
     |                      |                     |                   |--- 13. Commit Transaction ------------------>|
     |                      |                     |                   |<-- 14. Transaction Success -----------------|
     |                      |                     |<-- 15. Sale Object|                      |                      |
     |                      |<-- 16. HTTP 200 ----|                   |                      |                      |
     |                           (Render Invoice) |                   |                      |                      |
     |<-- 17. Display Bill -|                     |                   |                      |                      |
```

### Step-by-Step Walkthrough

1. **Cart Selection (Steps 1–3):** Counter staff pick the requested medicines and quantities on the POS billing screen and click Checkout. The browser sends a `POST` request with the customer information and item list.
2. **Delegation to Business Logic (Steps 4–5):** The route controller verifies that the user is logged in and forwards the cart to `SalesService.process_sale()`.
3. **FEFO Allocation Query (Steps 6–8):** `SalesService` calls `InventoryService.allocate_fefo()`. The service queries all active batches for that medicine from the database, sorted strictly by `expiry_date ASC`. It allocates units from the batch that expires soonest. If that batch does not have enough units, the remaining quantity is drawn from the next earliest batch.
4. **Safety Check (Step 9):** If any selected batch has an expiry date on or before today, the transaction is immediately stopped with a clear error message.
5. **Database Commit (Steps 10–13):** Inside an atomic transaction block:
   * Stock numbers on each affected batch are reduced.
   * A master `Sale` record is created with a unique invoice number (`INV-YYYYMMDDHHMM-XXXX`).
   * Detailed `SaleItem` rows are inserted recording which batch each strip came from.
   * `StockMovement` audit logs are created with type `DISPENSE`.
   * `DailyMedicineSales` records are updated to feed the forecasting engine.
6. **Billing Confirmation (Steps 14–17):** Once the database transaction commits successfully, the system renders a clean, printable customer invoice.

---

## 2.5 Activity Diagram and Decision Flows

The Activity Diagram tracks the decision points and state changes across daily pharmacy operations:

```
                              [ Start Session ]
                                      |
                                      v
                        /-----------------------------\
                       <  User Enters Credentials?    >
                        \-----------------------------/
                                      |
                     +----------------+----------------+
                     | Valid                           | Invalid
                     v                                 v
         [ Initialize User Session ]         [ Show Login Error Alert ]
                     |                                 |
                     v                                 v
        /-----------------------------\          [ End Session ]
       <   Check User Role in RBAC    >
        \-----------------------------/
          |            |            |
  ( Admin )     ( Pharmacist )   ( Staff )
          |            |            |
          v            v            v
     [ Executive ] [ Clinical ]  [ POS Billing ]
     [ Dashboard ] [ Inventory]  [ Counter     ]
          |            |            |
          +------------+------------+
                       |
        /------------------------------\
       <     Choose Daily Operation     >
        \------------------------------/
          |            |             |
          |            |             v
          |            |      [ POS Checkout Workflow ]
          |            |             |
          |            |             v
          |            |      /-------------------------\
          |            |     < Available Stock >= Qty?  >
          |            |      \-------------------------/
          |            |             |
          |            |      +------+------+
          |            |      | Yes         | No
          |            |      v             v
          |            |  [ Auto-FEFO ]  [ Show Insufficient ]
          |            |  [ Allocation]  [ Stock Warning     ]
          |            |      |
          |            |      v
          |            |  /-------------------------\
          |            | < Is Any Selected Expired? >
          |            |  \-------------------------/
          |            |      |
          |            |   No |  Yes
          |            |      v   +-----------------> [ Abort & Flag for Disposal ]
          |            |  [ Decrement Batch Stock ]
          |            |  [ Write Audit Movement  ]
          |            |  [ Generate Invoice Bill ]
          |            |
          |            v
          |   [ Batch & Expiry Management ]
          |            |
          |            v
          |   /-------------------------\
          |  < Batch Past Expiry Date?   >
          |   \-------------------------/
          |      | Yes         | No
          |      v             v
          |   [ Block & Safe ] [ Keep in Active ]
          |   [ Disposal     ] [ FEFO Rotation  ]
          |
          v
     [ AI Demand Forecasting & Reordering ]
          |
          v
     [ Gather Historical Sales Records ]
     [ Train Random Forest Regressor ]
     [ Compute ROP = LeadTime Sales + Safety Stock ]
     [ Create Suggested Purchase Order ]
          |
          v
     [ End Session / Logout ]
```

---

# CHAPTER 3: SYSTEM CONFIGURATION

## 3.1 Hardware Configuration

PharmaAI is designed to run efficiently on modest hardware. Pharmacies should not need to invest in expensive high-end servers just to manage inventory and billing. 

The hardware requirements for both development and production deployment are listed in Table 3.1.

### Table 3.1: Minimum and Recommended Hardware Specifications

| Setup Tier | Hardware Item | Minimum Requirement | Recommended Specification |
| :--- | :--- | :--- | :--- |
| **Development Machine** | **Processor (CPU)** | Intel Core i3 (8th Gen) or AMD Ryzen 3 (Quad-Core, 2.0 GHz) | Intel Core i5 / i7 (11th Gen+) or AMD Ryzen 5 (6-Core, 3.2 GHz+) |
| **Development Machine** | **RAM** | 4 GB DDR4 | 8 GB to 16 GB DDR4 / DDR5 (smoother multi-tasking and ML training) |
| **Development Machine** | **Disk Space** | 128 GB SATA SSD | 256 GB+ NVMe SSD |
| **Development Machine** | **Network** | 10 Mbps broadband / Wi-Fi | 50+ Mbps stable connection |
| **Production Server** | **Virtual CPU (vCPU)** | 1 vCPU (cloud instance) | 2 to 4 vCPUs (dedicated cloud instance) |
| **Production Server** | **Server RAM** | 1 GB RAM | 2 GB to 4 GB RAM |
| **Production Server** | **Server Storage** | 10 GB SSD block storage | 40 GB+ NVMe SSD with automated weekly backups |
| **Counter Device (Billing)** | **POS Terminal** | Dual-core PC, laptop, or tablet with 2 GB RAM | Standard desktop PC or laptop with 4 GB+ RAM |

---

## 3.2 Software Configuration and Libraries

The application uses established, open-source software libraries that provide high reliability, straightforward deployment, and strong security.

Table 3.2 details the technology stack and the specific role of each tool.

### Table 3.2: Software Frameworks, Versions, and Their Roles in the Project

| Category | Tool / Framework | Version Used | Role in PharmaAI |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 10/11 / Ubuntu Linux 22.04 LTS | 64-Bit OS | Host environment for development, testing, and deployment |
| **Programming Language** | Python | 3.10 / 3.11+ | Backend application logic, data structures, and ML forecasting |
| **Web Framework** | Flask | 3.0+ | Lightweight WSGI web framework, Blueprint routing, and request handling |
| **ORM & Database Toolkit** | Flask-SQLAlchemy (SQLAlchemy) | 3.1+ | Database modeling, relational mapping, and atomic transactions |
| **Database Engine** | SQLite (Dev) / PostgreSQL (Production) | SQLite 3 / Postgres 15+ | Relational data storage enforcing foreign keys and unique constraints |
| **Machine Learning Engine** | Scikit-Learn, NumPy, Pandas | 1.3+ | Random Forest model for demand predictions and feature engineering |
| **Authentication & Sessions** | Flask-Login & Werkzeug | 0.6+ / 3.0+ | Session cookies, user login callbacks, and salted password hashing |
| **Frontend UI Framework** | Bootstrap 5, Jinja2, HTML5, Vanilla JS | Bootstrap 5.3+ | Responsive layout, modern UI cards, color badges, and form interactions |
| **Automated Testing** | Pytest | 7.4+ | Automated unit tests, integration validation, and mock test fixtures |
| **Environment Settings** | Python-Dotenv | 1.0+ | Loading secret keys and database URLs from `.env` files |

---

# CHAPTER 4: SOFTWARE DESCRIPTION

## 4.1 Front End User Interface and Experience

The user interface of PharmaAI is server-rendered using **Jinja2 template inheritance** and styled with **Bootstrap 5**. The layout is intentionally clean and uncluttered, prioritizing readability and speed so counter staff can find what they need in seconds:

1. **Master Layout Hierarchy (`templates/base.html`):**
   All pages inherit from a common base template. This master file defines standard meta headers, the top navigation bar, dynamic user session badges, flash message alerts, and common modals. Specific views (such as the dashboard, sales billing, and inventory lists) plug into this template using content blocks.
2. **Visual Hierarchy and Color Coding:**
   Pharmacy staff need to spot potential problems immediately. We used purposeful color-coding throughout the interface:
   * **Healthy Stock (Emerald Green):** Indicates sufficient quantities with safe shelf lives.
   * **Critical Expiration (Red Alert):** Warns of batches expiring within 7 days so they can be disposed of or returned.
   * **Expiring Soon (Amber/Yellow):** Highlights stock expiring within 30 days so it can be prioritized for dispensing.
   * **Depleted Stock (Slate Gray):** Indicates that an item has reached zero units.
3. **Responsive Billing Counter:**
   The Point-of-Sale billing screen (`templates/sales/create.html`) allows staff to add items, modify quantities, and see subtotals update in real time via lightweight client-side JavaScript, ensuring smooth counter operations even during busy shifts.

---

## 4.2 Back End Architecture and Service Layers

The backend follows a clean, three-layer **Controller-Service-Repository** architecture. This ensures that route handlers only worry about HTTP requests and responses, while the actual business rules remain independent in dedicated service files:

1. **Application Factory (`app.py`):** Initializes the Flask application, loads environment settings (`config.py`), registers database and login extensions, and connects twelve domain Blueprint routers.
2. **Route Controllers (`routes/`):** Handle incoming web requests, check user role permissions, validate form submissions, call the relevant service, and return rendered templates or JSON responses.
3. **Service Layer (`services/`):** Contains the core logic:
   * **`InventoryService`:** Handles stock addition, batch balance calculations, and the First-Expiry, First-Out (FEFO) allocation algorithm.
   * **`SalesService`:** Manages the multi-step checkout workflow, stock decrementing, and invoice creation.
   * **`ReorderService`:** Computes dynamic Reorder Points, Lead Time Demand, and supplier replenishment packs.
   * **`ReportService`:** Aggregates management KPIs and generates downloadable CSV reports.

---

### Table 4.1: Application Route Namespaces, Assigned Controllers, and Access Permissions

| Route Path | Controller File | Allowed Roles | Main Responsibilities |
| :--- | :--- | :--- | :--- |
| `/auth` | `auth_routes.py` | Public / Logged In | Login, logout, session verification, and credential checks |
| `/` & `/dashboard` | `main_routes.py` | All Authenticated | Executive dashboard, real-time KPI overview, quick links |
| `/medicines` | `medicine_routes.py` | Admin, Pharmacist, Staff | Medicine catalog browsing, adding drugs, editing formulations |
| `/batches` | `batch_routes.py` | Admin, Pharmacist | Adding incoming batches, editing batch details, shelf locations |
| `/sales` | `sales_routes.py` | Admin, Pharmacist, Staff | POS billing counter, automated FEFO checkout, invoice view |
| `/expiry` | `expiry_routes.py` | Admin, Pharmacist | Expiry risk watchlist and authorized disposal of expired stock |
| `/forecast` | `forecast_routes.py` | Admin, Pharmacist | Viewing ML predictions, 7-day and 30-day demand charts |
| `/reorder` | `reorder_routes.py` | Admin, Pharmacist | Reviewing automated Reorder Points and safety stock buffers |
| `/purchase-orders` | `po_routes.py` | Admin, Pharmacist | Generating supplier orders, order approvals, receiving shipments |
| `/reports` | `report_routes.py` | Admin, Pharmacist | Inventory valuation summaries, sales logs, CSV exports |

---

## 4.3 Machine Learning Demand Forecasting Pipeline

The forecasting engine in `ml/` helps pharmacists look ahead instead of reacting after shelves are already empty:

1. **Feature Engineering Without Data Leakage (`ml/feature_engineering.py`):**
   Raw daily sales records are transformed into structured training features:
   * **Rolling Averages:** 7-day and 14-day rolling demand averages capturing recent momentum.
   * **Lag Variables:** Prior day consumption ($t-1, t-2, t-7$) capturing day-to-day rhythms.
   * **Calendar Indicators:** Day-of-week numbers and weekend flags capturing clinic visitation spikes.
2. **Random Forest Regression Model (`ml/model.py`):**
   We chose a **Random Forest Regressor** over complex deep learning architectures because it runs fast on standard desktop processors, does not require a GPU, and avoids overfitting on moderate-sized pharmacy datasets. The model outputs projected unit sales alongside Mean Absolute Error (MAE) benchmarks so staff can see how well the predictions match real sales.

---

# CHAPTER 5: SYSTEM DESIGN

## 5.1 Architectural Design

PharmaAI uses a clean **Four-Tier Architecture** that keeps user screens, routing logic, core business services, and database persistence clearly separated:

```
+-------------------------------------------------------------------------------+
|                       1. Client Presentation Tier                             |
|       (Jinja2 Templates, HTML5, Bootstrap 5, Custom CSS Tokens, JS)           |
+-------------------------------------------------------------------------------+
                                      |
                                 HTTP / HTTPS
                                      v
+-------------------------------------------------------------------------------+
|                     2. Flask Routing and Security Tier                        |
|       (WSGI App, Flask-Login Sessions, RBAC Decorators, Blueprints)           |
+-------------------------------------------------------------------------------+
                                      |
                              Service Invocations
                                      v
+-------------------------------------------------------------------------------+
|                      3. Domain Business Services Tier                         |
|   - InventoryService (FEFO Queue)          - SalesService (POS Invoicing)     |
|   - ReorderService (Safety Stock / ROP)    - Scikit-Learn ML Forecaster       |
+-------------------------------------------------------------------------------+
                                      |
                              SQLAlchemy ORM (ACID)
                                      v
+-------------------------------------------------------------------------------+
|                       4. Relational Persistence Tier                          |
|         (SQLite for Development / PostgreSQL for Enterprise Production)       |
+-------------------------------------------------------------------------------+
```

---

## 5.2 Input Design and Validation Rules

Input validation ensures that data entered by staff is clean, properly formatted, and protected against accidental errors or malicious inputs before it reaches the database:

1. **Form Context and Pre-Filled Values:** Whenever possible, forms use dynamic dropdown menus tied to active records (e.g., selecting a medicine automatically fills in its dosage form and standard price).
2. **Numeric and Date Boundary Checks:** Quantity fields are strictly constrained to positive whole numbers (`qty >= 1`), prices must be positive numbers, and expiry dates are checked to ensure they are valid calendar dates.

### Table 5.1: Form Input Validation Constraints Across Application Modules

| Module & URL | Field Name | Data Type | Validation Rule Applied | Behavior on Error |
| :--- | :--- | :--- | :--- | :--- |
| **Auth** (`/auth/login`) | `username`, `password` | Text | Non-empty strings; matches active account in database | HTTP 401 / "Invalid username or password" |
| **Medicines** (`/medicines/new`) | `name`, `category`, `dosage_form`, `reorder_point` | Text, Int | Unique brand name; approved clinical category; reorder point $\ge 0$ | HTTP 400 / "Medicine name already exists" |
| **Batches** (`/batches/new`) | `batch_number`, `expiry_date`, `initial_quantity`, `cost_price` | Text, Date, Int, Float | Unique batch code per medicine; valid future expiry date; quantity $> 0$ | HTTP 400 / "Invalid batch details or expiry date" |
| **Sales** (`/sales/create`) | `customer_name`, `customer_phone`, `items[]` | Text, List | Customer name required; 10-digit phone number; at least one item with quantity $\ge 1$ | HTTP 400 / "Cannot process empty sale or invalid quantity" |
| **Purchase Orders** (`/po/new`) | `supplier_id`, `items[]` | Int, List | Valid supplier ID; positive quantities matching pack constraints | HTTP 400 / "Supplier not found or empty line items" |

---

## 5.3 Output Design and Billing Layouts

Outputs are designed to be immediate, clear, and easy to interpret during busy store hours:

1. **Immediate Flash Notifications:** Every user action (saving a batch, completing a sale, disposing of an expired item) displays a color-coded notification banner across the top of the screen.
2. **Customer Invoice Layout:** Completed sales produce a clean, printable bill containing pharmacy details, the unique invoice number (`INV-YYYYMMDDHHMM-XXXX`), customer name, items purchased with batch codes, unit prices, and final totals.
3. **Dashboard KPI Gauges:** The executive screen presents key operational metrics at a glance: Usable Stock, Critical Expiries, Monthly Sales, and Pending Reorders.
4. **Downloadable CSV Reports:** Managers can export stock valuation registers, sales audit trails, and disposal records for accounting reviews and drug authority inspections.

---

## 5.4 Database Design and Schema Specification

The database is organized into **Third Normal Form (3NF)** so that all non-key columns depend solely on their primary keys, preventing data duplication and update anomalies.

```
  +------------------+          +------------------+          +-----------------------+
  |      users       |          |    suppliers     |          |       medicines       |
  +------------------+          +------------------+          +-----------------------+
  | id (PK)          |          | id (PK)          |          | id (PK)               |
  | username (UK)    |          | name             |          | name (UK)             |
  | password_hash    |          | contact_person   |          | category              |
  | role             |          | phone            |          | dosage_form           |
  | is_active        |          | email            |          | reorder_point         |
  +------------------+          +------------------+          +-----------------------+
           |                             |                                |
           | 1:N                         | 1:N                            | 1:N
           v                             v                                v
  +------------------+          +------------------+          +-----------------------+
  | stock_movements  |          | purchase_orders  |          |        batches        |
  +------------------+          +------------------+          +-----------------------+
  | id (PK)          |          | id (PK)          |          | id (PK)               |
  | medicine_id (FK) |          | po_number (UK)   |          | medicine_id (FK)      |
  | batch_id (FK)    |          | supplier_id (FK) |          | batch_number          |
  | user_id (FK)     |          | status           |          | expiry_date           |
  | movement_type    |          +------------------+          | current_quantity      |
  | quantity         |                                        +-----------------------+
  +------------------+                                                    |
                                                                          | 1:N
  +------------------+          +------------------+                      v
  |      sales       | 1:N      |    sale_items    |          +-----------------------+
  +------------------+--------->+------------------+<---------|   (Linked to Batch)   |
  | id (PK)          |          | id (PK)          |          +-----------------------+
  | invoice_no (UK)  |          | sale_id (FK)     |
  | customer_name    |          | medicine_id (FK) |
  | total_amount     |          | batch_id (FK)    |
  | payment_mode     |          | quantity         |
  +------------------+          +------------------+
```

---

### Table 5.2: Users Table Schema (`users`)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user account ID |
| `username` | VARCHAR(64) | NOT NULL, UNIQUE | Login handle used by staff |
| `password_hash` | VARCHAR(256)| NOT NULL | Salted password hash |
| `role` | VARCHAR(20) | NOT NULL, DEFAULT 'Staff' | Access tier (`Admin`, `Pharmacist`, `Staff`) |
| `full_name` | VARCHAR(128)| NOT NULL | Full personal name |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active/disabled flag |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation date and time |

---

### Table 5.3: Medicines Table Schema (`medicines`)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique medicine identifier |
| `name` | VARCHAR(128)| NOT NULL, UNIQUE | Commercial drug name |
| `generic_name` | VARCHAR(128)| NULLABLE | Active chemical compound |
| `category` | VARCHAR(64) | NOT NULL | Therapeutic category (e.g., Antibiotic) |
| `dosage_form` | VARCHAR(32) | NOT NULL | Form (Tablet, Capsule, Syrup, Injection) |
| `strength` | VARCHAR(32) | NOT NULL | Dosage strength (e.g., 500mg, 10mg) |
| `reorder_point`| INTEGER | NOT NULL, DEFAULT 50 | Default threshold to trigger reorder |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Product availability status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Date product was added to catalog |

---

### Table 5.4: Batches Table Schema (`batches`)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique batch ID |
| `medicine_id` | INTEGER | NOT NULL, FOREIGN KEY (`medicines.id`)| Associated medicine |
| `batch_number` | VARCHAR(64) | NOT NULL | Manufacturer batch identifier |
| `expiry_date` | DATE | NOT NULL | Expiry date printed on packaging |
| `initial_quantity` | INTEGER | NOT NULL | Total units received when batch arrived |
| `current_quantity` | INTEGER | NOT NULL, CHECK (`current_quantity >= 0`) | Available remaining units |
| `purchase_price` | DECIMAL(10,2)| NOT NULL | Wholesale purchase cost per unit |
| `selling_price` | DECIMAL(10,2)| NOT NULL | Retail selling price (MRP) per unit |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Batch availability status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Batch registration timestamp |

---

### Table 5.5: Sales Table Schema (`sales`)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique sale transaction ID |
| `invoice_number` | VARCHAR(64) | NOT NULL, UNIQUE | Human-readable bill number |
| `customer_name` | VARCHAR(128)| NOT NULL | Patient or buyer name |
| `customer_phone`| VARCHAR(20) | NOT NULL | Customer contact telephone |
| `total_amount` | DECIMAL(10,2)| NOT NULL | Net bill total after discounts |
| `payment_mode` | VARCHAR(32) | NOT NULL, DEFAULT 'Cash' | Payment method (`Cash`, `Card`, `UPI`) |
| `user_id` | INTEGER | NULLABLE, FOREIGN KEY (`users.id`) | Staff member who billed the sale |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Time sale was recorded |

---

### Table 5.6: Sale Items Table Schema (`sale_items`)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique line item ID |
| `sale_id` | INTEGER | NOT NULL, FOREIGN KEY (`sales.id`) | Parent invoice reference |
| `medicine_id` | INTEGER | NOT NULL, FOREIGN KEY (`medicines.id`)| Medicine sold |
| `batch_id` | INTEGER | NOT NULL, FOREIGN KEY (`batches.id`) | Specific batch drawn from |
| `quantity` | INTEGER | NOT NULL, CHECK (`quantity > 0`) | Number of units dispensed |
| `unit_price` | DECIMAL(10,2)| NOT NULL | Unit price at time of sale |
| `subtotal` | DECIMAL(10,2)| NOT NULL | Line subtotal amount |

---

### Table 5.7: Purchase Orders Table Schema (`purchase_orders`)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique purchase order ID |
| `po_number` | VARCHAR(64) | NOT NULL, UNIQUE | Standard order code |
| `supplier_id` | INTEGER | NOT NULL, FOREIGN KEY (`suppliers.id`)| Selected distributor |
| `status` | VARCHAR(32) | NOT NULL, DEFAULT 'Draft' | State (`Draft`, `Approved`, `Received`) |
| `total_cost` | DECIMAL(10,2)| NOT NULL, DEFAULT 0.00 | Total expected cost |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Order creation timestamp |

---

### Table 5.8: Stock Movements Audit Table Schema (`stock_movements`)

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique movement log ID |
| `medicine_id` | INTEGER | NOT NULL, FOREIGN KEY (`medicines.id`)| Medicine affected |
| `batch_id` | INTEGER | NOT NULL, FOREIGN KEY (`batches.id`) | Specific batch affected |
| `user_id` | INTEGER | NULLABLE, FOREIGN KEY (`users.id`) | User who performed the action |
| `movement_type`| VARCHAR(32) | NOT NULL | Type (`PURCHASE`, `DISPENSE`, `DISPOSAL`)|
| `quantity` | INTEGER | NOT NULL | Number of units moved |
| `notes` | TEXT | NULLABLE | Context or invoice reference note |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Audit timestamp |

---

# CHAPTER 6: SOURCE CODE

## 6.1 Core FEFO Batch Allocation and Dispensing Engine

**Purpose of File (`services/sales_service.py`):**
This module coordinates the complete Point-of-Sale checkout workflow. It pulls active batches in strict **First-Expiry, First-Out (FEFO)** order, verifies that no expired medicines are sold, decrements stock counters inside an atomic transaction, writes line items to the bill, records tamper-evident stock movements, and updates daily sales aggregations for the machine learning forecasting engine.

```python
# File: services/sales_service.py
# Description: Production FEFO Dispensing Engine and POS Transaction Service
from datetime import datetime, date
import uuid
from typing import List, Dict, Any
from models import (
    db,
    Medicine,
    Batch,
    Sale,
    SaleItem,
    DailyMedicineSales,
)
from .inventory_service import InventoryService, InventoryError


class SalesService:
    """Handles sales transactions, FEFO stock reduction, and sales analytics sync."""

    @staticmethod
    def generate_invoice_number() -> str:
        """Generate human-readable unique invoice number."""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M")
        short_id = uuid.uuid4().hex[:4].upper()
        return f"INV-{timestamp}-{short_id}"

    @staticmethod
    def process_sale(
        customer_name: str,
        customer_phone: str,
        items: List[Dict[str, Any]],
        payment_mode: str = "Cash",
        discount_amount: float = 0.0,
        user_id: int | None = None,
    ) -> Sale:
        """
        Execute an atomic checkout transaction:
        1. Validates all requested medicines and available quantities.
        2. Allocates stock using First Expiry, First Out (FEFO).
        3. Prevents sale of expired batches.
        4. Decrements batch stock and creates line items.
        5. Logs stock movement audit records.
        6. Aggregates daily sales record for AI forecasting.
        """
        if not items:
            raise InventoryError("Cannot process an empty sale. Please add medicines.")

        invoice_number = SalesService.generate_invoice_number()
        total_subtotal = 0.0
        sale_items_to_add: List[SaleItem] = []
        batch_updates: List[tuple[Batch, int]] = []
        movements_data: List[dict] = []
        daily_sales_aggregates: Dict[int, int] = {}  # medicine_id -> total_qty

        # Pre-validate and allocate each item
        for item in items:
            med_id = int(item["medicine_id"])
            qty = int(item["quantity"])

            if qty <= 0:
                raise InventoryError("Item quantity must be at least 1.")

            medicine = Medicine.query.get(med_id)
            if not medicine or not medicine.is_active:
                raise InventoryError(f"Medicine #{med_id} is unavailable or inactive.")

            # FEFO Allocation across non-expired batches ordered by expiry_date ASC
            allocations = InventoryService.allocate_fefo(med_id, qty)

            for batch, alloc_qty in allocations:
                if batch.is_expired:
                    raise InventoryError(
                        f"CRITICAL: Batch {batch.batch_number} for {medicine.name} has expired. "
                        "Expired drugs cannot be dispensed."
                    )

                unit_price = float(batch.selling_price)
                line_subtotal = unit_price * alloc_qty
                total_subtotal += line_subtotal

                sale_item = SaleItem(
                    medicine_id=med_id,
                    batch_id=batch.id,
                    quantity=alloc_qty,
                    unit_price=unit_price,
                    subtotal=line_subtotal,
                )
                sale_items_to_add.append(sale_item)
                batch_updates.append((batch, alloc_qty))

                movements_data.append(
                    {
                        "medicine_id": med_id,
                        "batch_id": batch.id,
                        "alloc_qty": alloc_qty,
                    }
                )

                daily_sales_aggregates[med_id] = (
                    daily_sales_aggregates.get(med_id, 0) + alloc_qty
                )

        final_amount = max(0.0, total_subtotal - float(discount_amount))

        # Atomic database transaction block
        try:
            sale = Sale(
                invoice_number=invoice_number,
                customer_name=customer_name.strip(),
                customer_phone=customer_phone.strip(),
                subtotal=total_subtotal,
                discount_amount=discount_amount,
                total_amount=final_amount,
                payment_mode=payment_mode,
                user_id=user_id,
            )
            db.session.add(sale)
            db.session.flush()  # Generate sale.id for line items

            # Attach sale line items
            for item_obj in sale_items_to_add:
                item_obj.sale_id = sale.id
                db.session.add(item_obj)

            # Apply stock deductions and write audit movements
            for batch, alloc_qty in batch_updates:
                batch.current_quantity -= alloc_qty

            for mov in movements_data:
                InventoryService.log_movement(
                    medicine_id=mov["medicine_id"],
                    batch_id=mov["batch_id"],
                    user_id=user_id,
                    movement_type="DISPENSE",
                    quantity=mov["alloc_qty"],
                    notes=f"POS Sale #{invoice_number}",
                )

            # Synchronize daily sales time-series for AI forecasting
            today = date.today()
            for med_id, total_qty_sold in daily_sales_aggregates.items():
                record = DailyMedicineSales.query.filter_by(
                    medicine_id=med_id, sale_date=today
                ).first()
                if record:
                    record.total_units_sold += total_qty_sold
                else:
                    new_record = DailyMedicineSales(
                        medicine_id=med_id,
                        sale_date=today,
                        total_units_sold=total_qty_sold,
                    )
                    db.session.add(new_record)

            db.session.commit()
            return sale

        except Exception as exc:
            db.session.rollback()
            raise InventoryError(f"Sale transaction failed and was rolled back: {str(exc)}")
```

---

# CHAPTER 7: SYSTEM TESTING

## 7.1 Testing Approach and Objectives

Testing was conducted to verify that PharmaAI functions accurately and reliably in real dispensary situations. We evaluated the system across five testing tiers:

1. **Unit Testing:** Verified individual functions in isolation (such as checking `Batch.days_to_expiry`, verifying password hashing, and testing safety stock math).
2. **Integration Testing:** Verified that route controllers, domain services, and database transactions work together seamlessly using an in-memory SQLite database.
3. **Clinical FEFO & Safety Testing:** Tested how the system allocates batches, ensuring that earlier-expiring stock is always used first and confirming that expired drugs are strictly blocked.
4. **Machine Learning Model Validation:** Tested the Random Forest pipeline with multi-month sales data, verifying that predictions remain non-negative and deliver realistic demand estimates.
5. **Security & Role-Based Permissions:** Verified that billing staff cannot access administrative or disposal routes.

---

## 7.2 Detailed Test Cases (TC-01 to TC-12)

#### Test Case TC-01: Valid User Login and Role Session
* **Objective:** Ensure valid users can log in and receive appropriate role permissions.
* **Test Input:** Username: `pharmacist`, Password: `pharm123`
* **Expected Output:** Login succeeds, user redirected to dashboard with `Pharmacist` access.
* **Actual Output:** Authenticated session created; dashboard rendered with pharmacist navigation.
* **Result:** **PASS**

#### Test Case TC-02: Rejection of Invalid Login Credentials
* **Objective:** Confirm system rejects incorrect passwords without creating a session.
* **Test Input:** Username: `admin`, Password: `WrongPassword123`
* **Expected Output:** Login rejected; error flash message displayed; no session created.
* **Actual Output:** Flash alert "Invalid username or password" shown; user kept on login page.
* **Result:** **PASS**

#### Test Case TC-03: FEFO Batch Priority Allocation
* **Objective:** Ensure dispensing automatically pulls from the batch that expires earliest.
* **Test Input:** Sell 10 units of Paracetamol. Active Batch A has 20 units (expires in 15 days); active Batch B has 50 units (expires in 60 days).
* **Expected Output:** All 10 units taken from Batch A; Batch B untouched.
* **Actual Output:** Batch A balance reduced to 10; Batch B balance remained 50.
* **Result:** **PASS**

#### Test Case TC-04: Multi-Batch Split Allocation
* **Objective:** Verify behavior when an order requires more units than the first expiring batch contains.
* **Test Input:** Sell 30 units. Batch A has 10 units (expires in 15 days); Batch B has 50 units (expires in 45 days).
* **Expected Output:** 10 units drawn from Batch A (balance = 0); 20 units drawn from Batch B (balance = 30).
* **Actual Output:** Two line items created correctly; balances updated accurately without errors.
* **Result:** **PASS**

#### Test Case TC-05: Strict Blocking of Expired Medicines
* **Objective:** Ensure no expired batch can be sold under any circumstances.
* **Test Input:** Attempt to sell 5 units from a batch whose expiry date was yesterday.
* **Expected Output:** Transaction aborted; `InventoryError` raised; stock unchanged.
* **Actual Output:** System halted checkout with message: "Expired drugs cannot be dispensed."
* **Result:** **PASS**

#### Test Case TC-06: Insufficient Inventory Rejection
* **Objective:** Verify system behavior when requested quantity exceeds total stock.
* **Test Input:** Request 200 units when total available stock across all active batches is 120 units.
* **Expected Output:** Transaction aborted; user informed of insufficient stock.
* **Actual Output:** Error raised: "Insufficient stock available"; no database changes made.
* **Result:** **PASS**

#### Test Case TC-07: Dynamic Expiry Risk Categorization
* **Objective:** Confirm batches are automatically assigned to the correct visual risk tier.
* **Test Input:** Batch 1 (expires in 5 days), Batch 2 (expires in 20 days), Batch 3 (expires in 180 days).
* **Expected Output:** Batch 1 marked Critical; Batch 2 marked Expiring Soon; Batch 3 marked Normal.
* **Actual Output:** Status properties evaluated correctly according to the defined thresholds.
* **Result:** **PASS**

#### Test Case TC-08: Safe Disposal of Expired Batches
* **Objective:** Verify that disposing of an expired batch zeroes its stock and writes an audit log.
* **Test Input:** Expired batch with 15 remaining units; Pharmacist clicks "Dispose".
* **Expected Output:** Batch deactivated; quantity set to 0; audit record created with type `DISPOSAL`.
* **Actual Output:** Quantity updated to 0; `is_active` set to False; audit entry recorded with user ID.
* **Result:** **PASS**

#### Test Case TC-09: Reorder Point (ROP) Calculation
* **Objective:** Validate calculation: $\text{ROP} = (\text{Daily Demand} \times \text{Lead Time}) + \text{Safety Stock}$.
* **Test Input:** Daily Sales = 10 units, Lead Time = 3 days, Demand Std Dev = 2.0, Safety Factor Z = 1.65.
* **Expected Output:** Lead Time Sales = 30; Safety Stock = 6; Expected ROP = 36 units.
* **Actual Output:** Reorder service returned exactly 36 units.
* **Result:** **PASS**

#### Test Case TC-10: ML Demand Forecasting Output Format
* **Objective:** Confirm Random Forest regressor produces valid non-negative forecasts.
* **Test Input:** 400 days of sales history; request 7-day and 30-day ahead forecasts.
* **Expected Output:** Projected arrays with non-negative numbers; MAE benchmark returned.
* **Actual Output:** Projections generated cleanly; values realistic and non-negative; MAE calculated.
* **Result:** **PASS**

#### Test Case TC-11: Purchase Order Stock Receipt
* **Objective:** Verify stock is credited when an approved Purchase Order is marked as received.
* **Test Input:** PO for 50 units of Amoxicillin updated to status `Received`.
* **Expected Output:** Inventory credited with 50 units; audit movement logged.
* **Actual Output:** New batch recorded with 50 units; audit trail entry created.
* **Result:** **PASS**

#### Test Case TC-12: Role-Based Access Guard on Restricted Endpoints
* **Objective:** Verify that Staff users cannot access administrative disposal routes.
* **Test Input:** Logged-in Staff user attempts `POST /expiry/dispose/1`.
* **Expected Output:** Access denied; redirected with unauthorized message.
* **Actual Output:** Request blocked by RBAC decorator; redirect to dashboard with alert.
* **Result:** **PASS**

---

### Table 7.1: Summary of Test Cases and Verification Outcomes

| Test ID | Module | Scenario Tested | Inputs Used | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Auth | Valid login & session creation | `user='pharmacist'`, `pass='pharm123'` | Redirect to dashboard; role set to Pharmacist | Session created with Pharmacist role | **PASS** |
| **TC-02** | Auth | Login with incorrect password | `user='admin'`, `pass='WrongPassword'` | Flash error; reject session | Error alert shown; login rejected | **PASS** |
| **TC-03** | Inventory | Auto-FEFO earliest batch priority | Sell 10 units; Batch A (exp: 15d), Batch B (exp: 60d) | Units deducted from Batch A; Batch B untouched | Batch A balance reduced; Batch B unchanged | **PASS** |
| **TC-04** | Inventory | Multi-batch split order | Sell 30 units; Batch A (10 units), Batch B (50 units) | 10 from Batch A; 20 from Batch B | Two line items created; balances updated | **PASS** |
| **TC-05** | Inventory | Expired drug dispensing block | Sell batch with `expiry_date < today` | Abort transaction; raise `InventoryError` | Sale blocked; error displayed | **PASS** |
| **TC-06** | Inventory | Insufficient stock handling | Request 200 units when total stock = 120 | Abort sale; raise insufficient stock error | Error displayed; no stock changed | **PASS** |
| **TC-07** | Expiry | Risk tier categorization | Batches expiring in 5d, 20d, 180d | Flagged as Critical, Warning, and Normal | Tiers assigned correctly | **PASS** |
| **TC-08** | Expiry | Expired stock disposal | Click Dispose on expired batch (15 units) | Batch deactivated; stock zeroed; audit logged | Stock zeroed; disposal movement logged | **PASS** |
| **TC-09** | Reorder | Automated ROP math | Sales=10/day, LeadTime=3d, StdDev=2.0 | ROP calculated as 36 units | ROP matched expected 36 units | **PASS** |
| **TC-10** | ML Forecast| Demand prediction output | 400 days sales records; 7d/30d projection | Projections $\ge 0$; MAE returned | Valid positive projections generated | **PASS** |
| **TC-11** | PO | Purchase Order receiving | PO for 50 units marked as `Received` | 50 units credited to stock; audit logged | Stock credited; batch created | **PASS** |
| **TC-12** | Security | Staff user on restricted route | Staff user calls `POST /expiry/dispose/1` | Access denied; HTTP 403 / Redirect | Request blocked; unauthorized alert | **PASS** |

### Results Summary

All twelve test cases passed successfully (**12 / 12 PASS**). Testing confirmed that the FEFO priority queue functions reliably, expired medicines are strictly blocked from sale, inventory deductions remain atomic, the Random Forest model generates dependable forecasts, and role-based permissions protect sensitive actions.

---

# CHAPTER 8: SYSTEM IMPLEMENTATION AND DEPLOYMENT

## 8.1 Environment Setup and Configuration

Following Twelve-Factor App principles, all configuration keys, secrets, and database connection strings are stored in a `.env` file rather than hard-coded into the repository.

### Table 8.1: Environment Variables and Configuration Parameters

| Category | Variable Name | Example Value | Purpose in Application |
| :--- | :--- | :--- | :--- |
| **Security** | `SECRET_KEY` | `pharmaai-secure-key-2026` | Cryptographic secret for signing session cookies |
| **Environment** | `FLASK_ENV` | `development` or `production` | Controls debug logging, reloaders, and error verbosity |
| **Database** | `USE_SQLITE` | `True` (Dev) / `False` (Production) | Toggles between local SQLite file and external database |
| **Database** | `SQLALCHEMY_DATABASE_URI` | `postgresql://user:pass@host:5432/pharmaai` | Connection URI when using PostgreSQL or MySQL |
| **Networking** | `PORT` | `5000` | Port bound by the Flask / WSGI server |

---

## 8.2 Step-by-Step Installation and Run Guide

To install and run PharmaAI on a fresh machine or server, follow these practical steps:

### Step 1: Clone the Repository
```bash
git clone https://github.com/organization/pharmaai.git
cd pharmaai
```

### Step 2: Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Or activate on Linux / macOS Bash:
# source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure the Environment File
Create a `.env` file in the project root directory:
```bash
SECRET_KEY=pharmaai-secure-key-2026
FLASK_ENV=production
USE_SQLITE=True
PORT=5000
```

### Step 5: Initialize the Database and Seed Demo Data
Run the seeding script to create database tables, set up default user accounts (`admin`, `pharmacist`, `staff`), generate synthetic sales history, and train the initial machine learning model:
```bash
python seed.py
```

### Step 6: Run Automated Tests
```bash
pytest
```
*Confirms that all 12 test cases pass before launching the server.*

### Step 7: Launch the Web Application
```bash
# Start development server:
python app.py

# Or start production WSGI server (Gunicorn on Linux):
# gunicorn --bind 0.0.0.0:5000 app:app --workers 4
```
Open a browser and navigate to **`http://127.0.0.1:5000`** to access the application.

---

# CHAPTER 9: CONCLUSION AND FUTURE SCOPE

## 9.1 Conclusion

The **PharmaAI: Smart Pharmacy Inventory and Demand Forecasting System** successfully addresses the common pain points found in community and hospital pharmacies: expired medicine losses, unexpected stockouts, and tedious manual paperwork. 

By implementing an automated **First-Expiry, First-Out (FEFO)** batch allocation algorithm, the system guarantees that older viable stock is sold first, while expired drugs are strictly blocked from being billed. Integrating a **Random Forest Regressor** provides pharmacists with practical forward visibility, helping them order medicines before stocks run low. Dynamic safety stock calculations and automated reordering take the guesswork out of purchasing. Finally, role-based security and immutable audit trails ensure that every unit of medicine is fully accounted for.

The project fulfills its primary goal: providing a reliable, user-friendly, and clinically sound software tool that simplifies everyday pharmacy work while improving patient safety.

---

## 9.2 Future Scope and Enhancements

While PharmaAI provides a solid, complete foundation for daily dispensary operations, several valuable features could be added in future versions:

1. **Barcode and 2D DataMatrix Handheld Scanner Support:**
   Connecting standard USB or Bluetooth barcode scanners to the billing counter so staff can simply scan a medicine carton to automatically identify the batch number, verify expiry, and add it to the bill.
2. **Multi-Branch Pharmacy Centralization:**
   Expanding the database to support pharmacy chains with multiple branches, allowing a slower branch to transfer near-expiry stock to a busier branch before the medicine goes to waste.
3. **Direct Distributor API & Webhook Integration:**
   Connecting the procurement module directly to wholesale distributor systems so purchase orders can be transmitted electronically without phone calls or manual emails.
4. **Deep Learning Forecasting with External Weather & Health Data:**
   Enhancing the forecasting model by factoring in regional weather patterns (e.g., monsoon rain forecasts) and public health alerts to anticipate seasonal fever outbreaks even earlier.
5. **Prescription Optical Character Recognition (OCR):**
   Adding a camera or scanner tool to read printed doctor prescriptions and pre-populate the billing cart, saving time for dispensary staff during rush hours.

---

# CHAPTER 10: APPENDICES

## 10.1 Application Interface Screenshots and Walkthrough

This section documents the visual screens of PharmaAI mapped to the Master List of Figures:

* **Figure 10.1: Secure Login Screen with Role-Based Redirection**
  The entry portal verifying staff usernames, passwords, and assigned roles (`Admin`, `Pharmacist`, `Staff`).
* **Figure 10.2: Real-Time Operations and Stock Status Dashboard**
  The central dashboard showing live counters for Total Usable Stock, Expiring Units, Monthly Revenue, and Pending Orders.
* **Figure 10.3: Medicine Inventory and Batch Overview Screen**
  The catalog list showing formulations, active batches, remaining quantities, and unit prices.
* **Figure 10.4: Multi-Tier Expiration Alert and Safe Disposal Panel**
  The monitoring panel highlighting batches in Critical (≤7 days) and Expiring Soon (≤30 days) tiers, with authorized one-click disposal actions.
* **Figure 10.5: Machine Learning Demand Prediction and Trend Analysis Screen**
  The forecasting page displaying 7-day and 30-day forward demand projections, trend curves, and model error metrics.
* **Figure 10.6: Reorder Suggestions and Supplier Purchase Order Generator**
  The procurement tool showing items below their Reorder Point and calculating suggested order quantities rounded to supplier pack sizes.
* **Figure 10.7: Point-of-Sale (POS) Billing Counter with Live Batch Breakdown**
  The fast billing screen where staff select medicines, view automated FEFO batch selections, and print clean customer receipts.

---

# CHAPTER 11: REFERENCES AND BIBLIOGRAPHY

1. **Python Programming Language:**
   Python Software Foundation, *Python Language Reference, Version 3.11*, Wilmington, DE, USA: Python Software Foundation, 2024. [Online]. Available: https://www.python.org/doc/

2. **Flask Web Application Framework:**
   Pallets Projects, *Flask Documentation (Release 3.0.x)*, The Pallets Organization, 2024. [Online]. Available: https://flask.palletsprojects.com/

3. **SQLAlchemy Object-Relational Mapping (ORM):**
   M. Bayer, *SQLAlchemy: Database Access and Object Relational Mapping for Python*, 2024. [Online]. Available: https://docs.sqlalchemy.org/

4. **Scikit-Learn Machine Learning in Python:**
   F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, et al., "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research (JMLR)*, vol. 12, pp. 2825–2830, 2011.

5. **Random Forest Regression Algorithms:**
   L. Breiman, "Random Forests," *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001. doi: 10.1023/A:1010933404324.

6. **Bootstrap Responsive Frontend Framework:**
   M. Otto and J. Thornton, *Bootstrap v5.3: Powerful, Extensible, and Feature-Packed Frontend Toolkit*, GitHub / Bootstrap Core Team, 2024. [Online]. Available: https://getbootstrap.com/

7. **Relational Database Normalization and ACID Transactions:**
   A. Silberschatz, H. F. Korth, and S. Sudarshan, *Database System Concepts*, 7th ed. New York, NY, USA: McGraw-Hill Education, 2019.

8. **Software Engineering Methodologies and UML Standards:**
   I. Sommerville, *Software Engineering*, 10th ed. Boston, MA, USA: Pearson Education, 2016.

9. **Good Pharmacy Practice (GPP) in Community and Hospital Pharmacy:**
   World Health Organization (WHO) & International Pharmaceutical Federation (FIP), "Joint FIP/WHO Guidelines on Good Pharmacy Practice: Standards for Quality of Pharmacy Services," *WHO Technical Report Series*, No. 961, Annex 8, Geneva, Switzerland: World Health Organization, 2011.

10. **First-Expiry, First-Out (FEFO) Inventory Control in Healthcare Supply Chains:**
    M. K. Craig, "Managing Pharmaceutical Expirations: Quantitative Analysis of FIFO vs. FEFO Replenishment Strategies," *International Journal of Production Economics*, vol. 182, pp. 412–425, 2016.

11. **Safety Stock and Dynamic Reorder Point Modeling:**
    S. Nahmias and T. L. Olsen, *Production and Operations Analysis*, 7th ed. Long Grove, IL, USA: Waveland Press, 2015.

12. **Role-Based Access Control (RBAC) Architecture:**
    R. S. Sandhu, E. J. Coyne, H. L. Feinstein, and C. E. Youman, "Role-Based Access Control Models," *IEEE Computer*, vol. 29, no. 2, pp. 38–47, Feb. 1996. doi: 10.1109/2.485845.

13. **Cryptographic Password Storage Standards (bcrypt):**
    N. Provos and D. Mazières, "A Future-Adaptable Password Scheme," in *Proceedings of the USENIX Annual Technical Conference (FREENIX Track)*, Monterey, CA, USA, 1999, pp. 81–91.

14. **Pytest Automated Testing Framework:**
    H. Krekel et al., *pytest: Helps You Write Better Programs*, 2024. [Online]. Available: https://docs.pytest.org/

15. **The Twelve-Factor App Methodology:**
    A. Wiggins, *The Twelve-Factor App*, Heroku / Salesforce, 2017. [Online]. Available: https://12factor.net/
