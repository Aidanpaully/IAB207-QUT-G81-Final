from flask import Flask, render_template
from EventBuddyPro import create_app # Import create_app and db

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)
