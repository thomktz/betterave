from create_app import create_app

app, local_ip = create_app()
print(f"Running on http://{local_ip}:5000")

if __name__ == "__main__":
    app.run(debug=True, host=local_ip, port=5000)
