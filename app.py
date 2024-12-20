from flask import redirect, url_for
from app import app
@app.route('/')
def h():
    return redirect(url_for("authentication.login_page"))

if __name__ == '__main__':
    app.run()
