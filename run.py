# run.py

from app import create_app

# Vytvoření Flask aplikace
app = create_app()

# Spuštění aplikace
if __name__ == "__main__":
    app.run(debug=True)
