from create_app import create_app

app, PORT = create_app()
print(f"Running on port {PORT}")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=True)

