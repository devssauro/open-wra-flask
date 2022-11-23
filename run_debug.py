from app import create_app

app = create_app()
app.run(port=5010, debug=True)
