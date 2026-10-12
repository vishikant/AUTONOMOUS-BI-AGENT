import pandas as pd  # pyright: ignore[reportMissingModuleSource]
import numpy as np

np.random.seed(42)

n_customers = 100000

customers = pd.DataFrame({
    "customer_id":  [
        f"C{i:06d}" for i in range(1, n_customers + 1)
    ],

    "gender": np.random.choice(
        ["Male", "Female"],
        n_customers
    ),

    "age": np.random.randint(
        18, 65,
        n_customers
    ),

    "city": np.random.choice(
        ["Delhi", "Mumbai", "Bangalore",
         "Hyderabad", "Chennai", "Pune",
         "Jaipur", "Kolkata"],
        n_customers
    ),

    "signup_date": pd.to_datetime(
        np.random.choice(
            pd.date_range(
                "2024-01-01",
                "2025-12-31"
            ),
            n_customers
        )
    )
})