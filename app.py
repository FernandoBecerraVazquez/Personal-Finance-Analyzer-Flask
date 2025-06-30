import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') # Lee la variable de entorno

# Opcional: Asegurarse de que la clave exista (para desarrollo o si es requerida)
if app.secret_key is None:
    raise RuntimeError("La variable de entorno 'FLASK_SECRET_KEY' no está configurada.")

CSV_FILE = 'transactions.csv' # Or transactions_2022_2023.csv

# Función para cargar el DataFrame de transacciones
# Asegúrate de que esta función maneje el caso en que el archivo no exista aún.
def load_transactions_df():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            # Aseguramos que la columna 'Date' sea datetime al cargar para evitar problemas futuros
            df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
            return df
        except Exception as e:
            print(f"Error al cargar CSV: {e}")
            # Si hay un error al cargar, creamos un DF vacío con las columnas esperadas
            # Asegúrate que estas columnas coincidan con la estructura de tu CSV después del merge
            return pd.DataFrame(columns=['Date', 'Name / Description', 'Expense/Income', 'Amount (EUR)', 'Category', 'Transaction', 'Transaction vs category'])
    else:
        # Si el archivo no existe, crea un DataFrame vacío con las columnas esperadas
        return pd.DataFrame(columns=['Date', 'Name / Description', 'Expense/Income', 'Amount (EUR)', 'Category', 'Transaction', 'Transaction vs category'])

# Función para guardar el DataFrame actualizado al CSV
def save_transactions_df(df):
    df.to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    # Cargar los datos actuales para mostrarlos si es necesario, o solo el formulario
    df = load_transactions_df()

    # Filtrar transacciones para mostrar sólo las del mes actual  
    df_display = pd.DataFrame() # DataFrame vacío por defecto
    if not df.empty:
        today = date.today() # Obtenemos la fecha actual
        current_year = today.year
        current_month = today.month
  
        # Aseguramos que la columna 'Date' esté en formato datetime para poder filtrar por año y mes
        df['Date'] = pd.to_datetime(df['Date']) 
        
        # Filtramos por el año Y el mes actuales
        df_display = df[(df['Date'].dt.year == current_year) & \
                        (df['Date'].dt.month == current_month)].copy() # Filtramos y hacemos una copia
    
    # Pasa la fecha de hoy al template para prellenar el campo de fecha en el formulario
    today_str = date.today().strftime('%Y-%m-%d')

    # Puedes pasar el DataFrame al template si quieres mostrar las transacciones actuales
    return render_template('index.html', transactions_data=df_display, today=today_str)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    if request.method == 'POST':
        # Obtener los datos del formulario
        date_str = request.form['date']
        description = request.form['description']
        type = request.form['type']
        amount = float(request.form['amount']) # Convertir a float

        # Inicio: Lógica de Validación de Fecha ---
        try:
            # Convertir la cadena de fecha a un objeto date para comparación
            input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            # Si el formato de fecha es incorrecto, devolver un error
            return "Error: Formato de fecha inválido. Por favor, usa YYYY-MM-DD.", 400 # Código de estado 400 para Bad Request

        today_date = date.today() # Obtener la fecha actual sin el componente de tiempo

        if input_date > today_date:
            # Si la fecha ingresada es posterior a hoy, devolver un error
            return "Error: No se puede ingresar una fecha posterior al día actual.", 400 # Código de estado 400 para Bad Request
        # FIN: Lógica de Validación de Fecha ---

        # Cargar el DataFrame existente
        df = load_transactions_df()

        # Crear una nueva fila como un diccionario
        new_transaction = {
            'Date': date_str,
            'Name / Description': description,
            'Expense/Income': type,
            'Amount (EUR)': amount
        }

        # Añadir la nueva transacción al DataFrame
        # Utiliza pd.concat para agregar la nueva fila
        df = pd.concat([df, pd.DataFrame([new_transaction])], ignore_index=True)

        # Guardar el DataFrame actualizado al archivo CSV
        save_transactions_df(df)

        # Redirigir de vuelta a la página principal o a una página de confirmación
        return redirect(url_for('index'))
    
# Borrar una transacción específica
@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    df = load_transactions_df()

    if df.empty:
        flash("No hay transacciones para eliminar.", "info")
        return redirect(url_for('index'))

    # Comprobamos si el transaction_id (índice) existe en el DataFrame
    if transaction_id in df.index:
        df_updated = df.drop(index=transaction_id) # Eliminamos la fila por su índice
        save_transactions_df(df_updated) # Guardamos el DataFrame actualizado
        flash(f"Transacción (ID: {transaction_id}) eliminada exitosamente.", "success")
    else:
        flash(f"Error: No se encontró la transacción con ID {transaction_id}.", "error")

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Esto ejecuta la aplicación Flask.
    # En un entorno de desarrollo, debug=True es útil para ver errores.
    # Para producción, se debe desactivar debug.
    app.run(debug=True)