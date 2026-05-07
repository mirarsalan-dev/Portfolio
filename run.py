from app import create_app

# Generate the app using our factory function
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode so it auto-updates when you save files
    app.run(debug=True, port=5000)