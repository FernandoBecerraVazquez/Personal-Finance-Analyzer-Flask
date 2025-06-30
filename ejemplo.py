import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Definir la fecha de inicio y fin para los datos
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 6, 26) # Fecha actual

# Lista de posibles categorías de gastos
expense_categories = [
    "Groceries", "Transport", "Rent", "Utilities", "Dining Out",
    "Entertainment", "Shopping", "Health", "Education", "Subscriptions",
    "Travel", "Personal Care"
]

# Lista de posibles categorías de ingresos
income_categories = [
    "Salary", "Freelance Income", "Investment", "Gift", "Bonus", "Refund"
]

# Descripciones de transacciones (simulando las originales y luego las limpiadas)
transaction_descriptions = {
    "Groceries": ["supermercado la esquina", "walmart compra semanal", "tienda de abarrotes", "oxxo comida rapida"],
    "Transport": ["gasolinera magna", "uber viaje", "taxi de noche", "recarga mi transporte"],
    "Rent": ["pago renta mensual"],
    "Utilities": ["cfe recibo luz", "telmex internet", "agua y drenaje"],
    "Dining Out": ["restaurante italiano", "cafeteria la pausa", "mcdonalds burger"],
    "Entertainment": ["cineplex boletos", "concierto ticketmaster", "videojuego steam"],
    "Shopping": ["ropa de marca", "electronicos gadget", "amazon compra online"],
    "Health": ["farmacia benavides", "consulta medico", "seguro de gastos medicos"],
    "Education": ["colegiatura universidad", "libros de texto"],
    "Subscriptions": ["netflix premium", "spotify ab by adyen", "gimnasio membresia"],
    "Travel": ["vuelo aeromexico", "hotel la playa", "alquiler coche"],
    "Personal Care": ["peluqueria corte", "spa masaje"],
    "Salary": ["deposito nomina mensual"],
    "Freelance Income": ["pago cliente proyecto"],
    "Investment": ["dividendo acciones"],
    "Gift": ["regalo de cumpleaños"],
    "Bonus": ["bono de fin de año"],
    "Refund": ["reembolso compra"]
}

data = []
current_date = start_date
while current_date <= end_date:
    # Simular unas 1-3 transacciones por día
    num_transactions = random.randint(1, 3)
    for _ in range(num_transactions):
        is_expense = random.random() < 0.85 # 85% de probabilidad de ser gasto
        
        if is_expense:
            category = random.choice(expense_categories)
            amount = round(random.uniform(5, 300), 2) # Montos más pequeños para gastos
            desc_options = transaction_descriptions.get(category, [f"Gasto {category}"])
            name_description_raw = random.choice(desc_options) + (f" {random.randint(1, 100)}" if random.random() < 0.2 else "") # Añadir algo extra a veces
            name_description_cleaned = name_description_raw.lower().replace("  ", " ").strip()
            # Para Transaction, podemos simular que es la versión limpia
            transaction_col = name_description_cleaned
            # Para Transaction vs category, puede ser igual o un poco más explícito
            transaction_vs_category = f"{name_description_cleaned} ({category})"
            expense_income_type = "Expense"
        else:
            category = random.choice(income_categories)
            amount = round(random.uniform(100, 2000), 2) # Montos más grandes para ingresos
            desc_options = transaction_descriptions.get(category, [f"Ingreso {category}"])
            name_description_raw = random.choice(desc_options) + (f" {random.randint(1, 50)}" if random.random() < 0.1 else "")
            name_description_cleaned = name_description_raw.lower().replace("  ", " ").strip()
            transaction_col = name_description_cleaned
            transaction_vs_category = f"{name_description_cleaned} ({category})"
            expense_income_type = "Income"

        data.append({
            'Date': current_date.strftime('%Y-%m-%d'),
            'Name / Description': name_description_raw, # Mantener la "raw" para simular antes de la limpieza
            'Expense/Income': expense_income_type,
            'Amount (EUR)': amount,
            'Category': category, # Ya categorizado
            'Transaction': transaction_col, # Simula la columna Transaction de tu categories_df_final
            'Transaction vs category': transaction_vs_category # Simula la columna Transaction vs category
        })
    
    current_date += timedelta(days=1)

# Crear el DataFrame
df_sample = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
output_csv_file = 'transactions_2023_2025_sample.csv'
df_sample.to_csv(output_csv_file, index=False)

print(f"Archivo '{output_csv_file}' generado exitosamente con {len(df_sample)} transacciones.")
print("Primeras 5 filas del archivo generado:")
print(df_sample.head())
print("\nÚltimas 5 filas del archivo generado:")
print(df_sample.tail())
print("\nAños presentes en el archivo:")
print(pd.to_datetime(df_sample['Date']).dt.year.unique())