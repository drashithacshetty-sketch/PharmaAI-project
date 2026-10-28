import os
from pathlib import Path
from datetime import date, timedelta
import numpy as np
import pandas as pd

FICTIONAL_MEDICINES = [
    {
        "id": 1,
        "name": "Paracetamol 500mg",
        "generic_name": "Acetaminophen",
        "category": "Analgesic & Antipyretic",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "unit": "Strip",
        "pack_size": 10,
        "base_daily_sales": 28.0,
        "trend": 0.015,
        "seasonality_phase": 0.2,
        "zero_sale_prob": 0.02,
        "noise_scale": 4.5,
        "reorder_level": 120,
        "purchase_price": 12.50,
        "selling_price": 25.00,
    },
    {
        "id": 2,
        "name": "Amoxicillin 500mg",
        "generic_name": "Amoxicillin Trihydrate",
        "category": "Antibiotic",
        "dosage_form": "Capsule",
        "strength": "500mg",
        "unit": "Strip",
        "pack_size": 10,
        "base_daily_sales": 15.0,
        "trend": 0.008,
        "seasonality_phase": 0.8,
        "zero_sale_prob": 0.06,
        "noise_scale": 3.2,
        "reorder_level": 80,
        "purchase_price": 45.00,
        "selling_price": 75.00,
    },
    {
        "id": 3,
        "name": "Cetirizine 10mg",
        "generic_name": "Cetirizine Hydrochloride",
        "category": "Antihistamine",
        "dosage_form": "Tablet",
        "strength": "10mg",
        "unit": "Strip",
        "pack_size": 10,
        "base_daily_sales": 18.0,
        "trend": 0.012,
        "seasonality_phase": 1.5,  # Higher in spring / seasonal changes
        "zero_sale_prob": 0.04,
        "noise_scale": 3.8,
        "reorder_level": 90,
        "purchase_price": 18.00,
        "selling_price": 38.00,
    },
    {
        "id": 4,
        "name": "Metformin 500mg",
        "generic_name": "Metformin Hydrochloride",
        "category": "Antidiabetic",
        "dosage_form": "Tablet",
        "strength": "500mg",
        "unit": "Strip",
        "pack_size": 10,
        "base_daily_sales": 22.0,
        "trend": 0.020,  # Steady chronic medication demand growth
        "seasonality_phase": 0.0,
        "zero_sale_prob": 0.01,
        "noise_scale": 2.5,
        "reorder_level": 100,
        "purchase_price": 20.00,
        "selling_price": 42.00,
    },
    {
        "id": 5,
        "name": "Atorvastatin 20mg",
        "generic_name": "Atorvastatin Calcium",
        "category": "Cardiovascular",
        "dosage_form": "Tablet",
        "strength": "20mg",
        "unit": "Strip",
        "pack_size": 10,
        "base_daily_sales": 14.0,
        "trend": 0.018,
        "seasonality_phase": 0.1,
        "zero_sale_prob": 0.03,
        "noise_scale": 2.2,
        "reorder_level": 70,
        "purchase_price": 55.00,
        "selling_price": 110.00,
    },
    {
        "id": 6,
        "name": "Azithromycin 250mg",
        "generic_name": "Azithromycin Dihydrate",
        "category": "Antibiotic",
        "dosage_form": "Tablet",
        "strength": "250mg",
        "unit": "Strip",
        "pack_size": 6,
        "base_daily_sales": 9.0,
        "trend": 0.005,
        "seasonality_phase": 2.1,  # Seasonal respiratory infections
        "zero_sale_prob": 0.12,
        "noise_scale": 2.8,
        "reorder_level": 50,
        "purchase_price": 60.00,
        "selling_price": 115.00,
    },
    {
        "id": 7,
        "name": "Omeprazole 20mg",
        "generic_name": "Omeprazole",
        "category": "Gastrointestinal",
        "dosage_form": "Capsule",
        "strength": "20mg",
        "unit": "Strip",
        "pack_size": 15,
        "base_daily_sales": 16.0,
        "trend": 0.010,
        "seasonality_phase": 0.4,
        "zero_sale_prob": 0.03,
        "noise_scale": 3.0,
        "reorder_level": 80,
        "purchase_price": 22.00,
        "selling_price": 48.00,
    },
    {
        "id": 8,
        "name": "Ibuprofen 400mg",
        "generic_name": "Ibuprofen",
        "category": "Analgesic & NSAID",
        "dosage_form": "Tablet",
        "strength": "400mg",
        "unit": "Strip",
        "pack_size": 10,
        "base_daily_sales": 20.0,
        "trend": 0.007,
        "seasonality_phase": 0.3,
        "zero_sale_prob": 0.03,
        "noise_scale": 4.0,
        "reorder_level": 110,
        "purchase_price": 15.00,
        "selling_price": 32.00,
    },
]


def generate_synthetic_sales_data(
    num_days: int = 400,
    output_path: str | Path | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate reproducible synthetic daily pharmaceutical sales records for >= 12 months.
    Includes:
    - Base demand per drug
    - Day-of-week weekly cyclical patterns (higher weekday doctor consultations, lower Sundays)
    - Macro trends (gradual population/chronic therapy adoption)
    - Annual seasonal sinusoidal components (respiratory/allergy cycles)
    - Realistic zero-sales probability
    - Normal/Poisson random disturbance
    """
    np.random.seed(seed)
    end_date = date.today()
    start_date = end_date - timedelta(days=num_days)

    date_range = [start_date + timedelta(days=i) for i in range(num_days)]
    records = []

    # Day of week multiplier (Mon=0, Tue=1, ..., Sun=6)
    # Pharmacy clinic surges happen on Mon-Tue and Fri-Sat; Sun has reduced footfall
    dow_multipliers = {
        0: 1.18,  # Monday doctor clinic rush
        1: 1.08,  # Tuesday steady
        2: 1.02,  # Wednesday
        3: 1.00,  # Thursday
        4: 1.12,  # Friday pre-weekend refills
        5: 1.15,  # Saturday outpatient clinic visits
        6: 0.65,  # Sunday reduced operating hours
    }

    for med in FICTIONAL_MEDICINES:
        med_id = med["id"]
        med_name = med["name"]
        base = med["base_daily_sales"]
        trend_rate = med["trend"]
        season_phase = med["seasonality_phase"]
        zero_prob = med["zero_sale_prob"]
        noise_std = med["noise_scale"]
        unit_price = med["selling_price"]

        for idx, current_dt in enumerate(date_range):
            # 1. Day of week effect
            dow = current_dt.weekday()
            dow_factor = dow_multipliers[dow]

            # 2. Linear trend
            trend_factor = 1.0 + (trend_rate * (idx / 30.0))

            # 3. Annual Seasonality cycle (sine wave period = 365.25 days)
            day_of_year = current_dt.timetuple().tm_yday
            seasonality = 1.0 + 0.25 * np.sin(
                (2 * np.pi * day_of_year / 365.25) + season_phase
            )

            # 4. Expected mean sales
            expected_sales = base * dow_factor * trend_factor * seasonality

            # 5. Add random noise
            sales_val = expected_sales + np.random.normal(0, noise_std)

            # 6. Apply zero-sales day probability
            if np.random.random() < zero_prob:
                sales_val = 0.0

            # Ensure non-negative integers
            final_units = max(0, int(round(sales_val)))

            # Number of transactions
            num_tx = (
                max(1, int(round(final_units / np.random.uniform(1.2, 2.5))))
                if final_units > 0
                else 0
            )
            revenue = round(final_units * unit_price, 2)

            records.append(
                {
                    "medicine_id": med_id,
                    "medicine_name": med_name,
                    "sale_date": current_dt.strftime("%Y-%m-%d"),
                    "total_units_sold": final_units,
                    "total_revenue": revenue,
                    "num_transactions": num_tx,
                    "day_of_week": dow,
                    "is_weekend": 1 if dow in (5, 6) else 0,
                    "month": current_dt.month,
                    "day_of_month": current_dt.day,
                }
            )

    df = pd.DataFrame(records)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out, index=False)

    return df


if __name__ == "__main__":
    df = generate_synthetic_sales_data(
        num_days=400, output_path="data/synthetic_sales.csv"
    )
    print(f"Generated {len(df)} daily sales records across {df['medicine_id'].nunique()} medicines.")
