from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "shopsphere.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def prepare_database():
    csv_files = list(RAW_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DIR}"
        )

    with sqlite3.connect(DB_PATH) as conn:
        for file in csv_files:
            table_name = file.stem.lower()
            df = pd.read_csv(file)

            # Keep raw files unchanged. This filtering is only
            # applied to the database copy of transaction tables.
            date_columns = {
                "orders": "order_date",
                "payments": "payment_date",
                "returns": "return_date",
                "website_sessions": "session_date",
            }

            date_col = date_columns.get(table_name)

            if date_col and date_col in df.columns:
                parsed = pd.to_datetime(
                    df[date_col], errors="coerce"
                )
                today = pd.Timestamp.now().normalize()

                # Exclude future-dated synthetic transactions.
                df = df.loc[
                    parsed.notna() & (parsed <= today)
                ].copy()

                df[date_col] = parsed.loc[df.index].dt.strftime(
                    "%Y-%m-%d"
                )

            df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

            print(
                f"Loaded {table_name}: "
                f"{len(df):,} rows, {len(df.columns)} columns"
            )

        # Add indexes when the expected columns exist.
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table'"
            )
        }

        index_specs = {
            "orders": ["order_id", "order_date"],
            "order_items": ["order_id", "product_id"],
            "payments": ["order_id", "payment_date"],
            "returns": ["order_id", "return_date"],
            "website_sessions": ["session_date"],
        }

        for table, columns in index_specs.items():
            if table not in tables:
                continue

            available = {
                row[1]
                for row in conn.execute(
                    f'PRAGMA table_info("{table}")'
                )
            }

            for col in columns:
                if col in available:
                    conn.execute(
                        f'CREATE INDEX IF NOT EXISTS '
                        f'"idx_{table}_{col}" '
                        f'ON "{table}"("{col}")'
                    )

    print(f"\nDatabase ready: {DB_PATH}")


if __name__ == "__main__":
    prepare_database()

from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "shopsphere.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def prepare_database():
    csv_files = list(RAW_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files found in {RAW_DIR}"
        )

    with sqlite3.connect(DB_PATH) as conn:
        for file in csv_files:
            table_name = file.stem.lower()
            df = pd.read_csv(file)

            # Keep raw files unchanged. This filtering is only
            # applied to the database copy of transaction tables.
            date_columns = {
                "orders": "order_date",
                "payments": "payment_date",
                "returns": "return_date",
                "website_sessions": "session_date",
            }

            date_col = date_columns.get(table_name)

            if date_col and date_col in df.columns:
                parsed = pd.to_datetime(
                    df[date_col], errors="coerce"
                )
                today = pd.Timestamp.now().normalize()

                # Exclude future-dated synthetic transactions.
                df = df.loc[
                    parsed.notna() & (parsed <= today)
                ].copy()

                df[date_col] = parsed.loc[df.index].dt.strftime(
                    "%Y-%m-%d"
                )

            df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False
            )

            print(
                f"Loaded {table_name}: "
                f"{len(df):,} rows, {len(df.columns)} columns"
            )

        # Add indexes when the expected columns exist.
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table'"
            )
        }

        index_specs = {
            "orders": ["order_id", "order_date"],
            "order_items": ["order_id", "product_id"],
            "payments": ["order_id", "payment_date"],
            "returns": ["order_id", "return_date"],
            "website_sessions": ["session_date"],
        }

        for table, columns in index_specs.items():
            if table not in tables:
                continue

            available = {
                row[1]
                for row in conn.execute(
                    f'PRAGMA table_info("{table}")'
                )
            }

            for col in columns:
                if col in available:
                    conn.execute(
                        f'CREATE INDEX IF NOT EXISTS '
                        f'"idx_{table}_{col}" '
                        f'ON "{table}"("{col}")'
                    )

    print(f"\nDatabase ready: {DB_PATH}")


if __name__ == "__main__":
    prepare_database()
