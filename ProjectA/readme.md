# 🗄️ Database Management Systems Project – Part 1

<p align='center'>
  <a href="https://github.com/yuvalmar16">Yuval Margolin</a> | 
  <a href="https://github.com/RavidGersh59">Ravid Gersh</a>
</p>

---

## 🧠 Project Overview

This project is the **first part** of a comprehensive database management system (DBMS) project developed for the **Database Management Systems** course.  
The project models a cable television company's operations, including households, devices, programs, channels, employees, and family memberships.  
The work includes full database design, schema creation, complex view definitions, and analytical SQL querying.

The goal is to apply fundamental and advanced concepts in relational modeling, SQL query writing, integrity constraint handling, and view management.

---

## 📁 Files Included

| File | Description |
|:---|:---|
| `ERD.pdf` | Entity-Relationship Diagram (ERD) and detailed description of design limitations and non-enforceable constraints. |
| `q2.sql` | Database schema (DDL) and basic data manipulation (DML) commands (e.g., table creation, initial inserts). |
| `Views.py` | Python script containing all SQL view creation scripts as required by the project. |
| `Queries.py` | Python script containing SQL queries answering project analytical questions. |

---

## 🛠️ Key Components

### 1. **Database Design**

- **ERD Diagram** modeling:
  - Employees, Technicians, Managers
  - Families and Family Types (Regular, Premium)
  - Devices and Converter Boxes
  - Channels and Programs
  - Viewing Activity
  - Requests and Device Movements
- **Design Limitations** discussed:
  - Constraints that cannot be enforced strictly by the ERD or SQL (e.g., unique manager swaps, premium wealth validation).

---

### 2. **Schema Creation (DDL)**

- Creation of all required tables with appropriate keys, foreign key references, and types.
- Notable table groups:
  - `Employee`, `Department`
  - `Family`, `Person`, `Device`, `Viewing`
  - `Programs`, `Channels`
  - `MoveRequests`

---

### 3. **Views Implementation**

- **bigRichFamily**: Families with ≥3 members and net worth >5.
- **familyWithClass**: Subset of wealthy families who do *not* watch "Reality" genre programs.
- **LongestPrograms**: Programs that are the longest within their genre.
- **PopularShow**: Popular programs watched by ≥3 different households.
- **modernFamily**: Modern families linked to long and popular shows.
- **firstShowsWatched**: First show watched by each family based on earliest timestamp.

---

### 4. **Query Execution**

- Count the number of devices per qualifying family.
- Identify the first shows watched by modern families with ≥3 members.
- Use SQL JOINs, aggregations, filtering, and ordering to retrieve correct results based on the views.

---

## 📚 Topics and Concepts Demonstrated

- Entity-Relationship (ER) Modeling
- SQL DDL and DML commands
- View Creation and Management
- Complex SQL Queries using JOINs, GROUP BY, HAVING, and Subqueries
- Data Integrity Discussions (enforceable vs. non-enforceable constraints)
- Database normalization thinking

---

## 🛠️ Technologies and Tools

- SQL (ANSI standard)
- Python (for organizing views and queries)
- PostgreSQL / SQL Server / MySQL (compatible syntax)
- ERD Design Tools (drawn and exported manually)

---

## 🤝 Contributors

- [Yuval Margolin](https://github.com/yuvalmar16)
- [Ravid Gersh](https://github.com/RavidGersh59)

---


