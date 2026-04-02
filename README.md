#CivilEngineeringTools

# 🚧 Civil Engineering Survey Automation (Python + Streamlit)

A Python-based automation tool for **Traverse and Leveling calculations** with visualization support.  
Built to reduce manual computation errors and improve efficiency in survey workflows.

---

## 📖 Overview

This project automates core surveying tasks:

- Traverse computations (Open & Closed)
- Leveling computations (Rise & Fall / HI method)
- Bearing conversion (DMS → Decimal → Radians)
- Latitude & Departure calculation
- Bowditch adjustment method
- Coordinate generation & plotting

Built using:
- **Python**
- **Pandas**
- **NumPy**
- **Streamlit**

---

## ⚙️ Features

### ✅ Traverse Automation
- Supports:
  - Open Traverse
  - Closed Traverse
- Bearing input in **DMS format**
- Automatic conversions:
  - DMS → Decimal Degrees
  - Decimal → Radians
- Computes:
  - Latitude & Departure
  - Closing error
  - Bowditch correction
- Generates coordinates from origin (0,0)
- Traverse plotting

---

### ✅ Leveling Automation
- Supports:
  - Rise & Fall Method
  - Height of Instrument (HI) Method
- Computes:
  - Reduced Levels (RL)
  - Rise and Fall values
  - Check: ΣRise - ΣFall = Last RL - First RL
- Handles:
  - BS (Back Sight)
  - IS (Intermediate Sight)
  - FS (Fore Sight)

---

### 📊 Data Handling
- CSV-based input
- Uses **Pandas DataFrame**
- Handles missing and structured data efficiently

---

### 📈 Visualization
- Traverse plotting
- Structured tables in Streamlit UI

---

## 🧠 Core Concepts Used

### Surveying
- Whole Circle Bearing (WCB)
- Latitude & Departure
- Bowditch Method
- Rise & Fall Method
- Height of Instrument Method

### Programming
- Object-Oriented Programming (OOP)
- Data processing with Pandas
- Numerical operations with NumPy

---

## 📂 Project Structure
CivilEngineeringTools/
│
├── logics/
│ ├── traverse_logics.py
│ ├── leveling_logics.py
│
├── app.py
├── data/
│ ├── traverse_sample.csv
│ ├── leveling_sample.csv
│
├── README.md


---

## 🚀 How to Run

### 1. Clone repository
```bash
git clone <your-repo-link>
cd CivilEngineeringTools

2. Install dependencies
pip install pandas numpy streamlit

3. Run app
streamlit run app.py

🧪 Example Inputs
Traverse Data
Station	Bearing (DMS)	Distance
A-B	10,20,30	100
B-C	120,15,0	150

Leveling Data
Station	BS	IS	FS
A	1.5		
B		1.2	
C			1.8

⚠️ Current Limitations
-Only Bowditch correction implemented (no Transit method yet)
-UI is functional but not optimized
-Limited input validation for incorrect formats

🎯 Why This Project Matters

Surveying computations are traditionally manual and error-prone.
This system demonstrates how Civil Engineering + Programming can:

Automate repetitive calculations
Improve accuracy
Enable scalable engineering workflows

👨‍💻 Author

Shivam
Civil Engineering Student | Python Developer | Future BIM + Automation Engineer