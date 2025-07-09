# 🅿️ Dynamic Pricing for Urban Parking Lots

**Capstone Project – Summer Analytics 2025**  
Hosted by Consulting & Analytics Club × Pathway

---

## 📌 Project Overview

In urban cities, static parking prices often lead to inefficient use of parking resources—some lots get overcrowded while others remain underused. This project aims to solve that with an **intelligent, real-time pricing system**.

We developed a dynamic pricing engine for 14 city parking spaces, simulating real-world conditions and constraints using:

- Historical occupancy trends  
- Queue length and congestion  
- Traffic levels and special days  
- Vehicle type (car, bike, truck)  
- Nearby competitor pricing  



---

## 🧰 Tech Stack

| Layer           | Technology                  |
|----------------|-----------------------------|
| Language        | Python 3.x                  |
| Libraries       | Pandas, NumPy, Matplotlib   |
| Visualization   | Bokeh                       |
| Optional Tools  | Pathway (for streaming)     |
| Platform        | Google Colab / Jupyter Lab  |

---





## ⚙️ Project Architecture & Workflow

### 1. 🔄 Data Preprocessing
- Combine `LastUpdatedDate` and `LastUpdatedTime` into a `Datetime` column.
- Map categorical values (`TrafficConditionNearby`, `VehicleType`) to numerical scores.
- Clean column names and normalize weights for vehicle types.

---

### 2. 📈 Baseline Pricing
Linear model based on occupancy:

```python
Price = BasePrice + α × (Occupancy / Capacity)
```

---

### 3. 📊 Demand-Based Pricing
Multi-variable pricing function that considers:
- Occupancy ratio
- Queue length
- Traffic level
- Special day indicator
- Vehicle type weight

Normalized demand determines the final price:

```python
Price = BasePrice × (1 + λ × NormalizedDemand)
```

---

### 4. 🧠 Competitive Pricing (Geo-aware)
- Uses the **Haversine formula** to find nearby lots (within 1 km).
- Adjusts price by averaging with prices of nearby competitors:

```python
Final Price = (Own Price + Nearby Mean Price) / 2
```

---

### 5. 🚘 Rerouting Logic (Optional)
- If a parking lot’s utilization exceeds 90%, reroute incoming vehicles to:
  - Nearby
  - Less congested
  - Cheaper parking lots

---

### 6. ⏱️ Real-Time Simulation
- Simulates a real-time stream at **30-minute intervals**.
- Prints the following info in the console:
  - Time
  - Lot number
  - Baseline Price
  - Demand-Based Price
  - Competitive Price
  - Reroute suggestions

---

### 7. 📊 Bokeh Visualization
- Real-time interactive line graph showing:
  - Baseline Price
  - Demand-Based Price
  - Competitive Price

---



## ▶️ How to Run

### 🔧 Clone the repo
```bash
git clone https://github.com/yourusername/dynamic-parking-pricing.git
cd dynamic-parking-pricing
```

### 📦 Install required libraries
```bash
pip install pandas numpy bokeh matplotlib
```

### 🚀 Run the script or open notebook
```bash
python pricing_model.py
# or open the interactive notebook
main.ipynb



