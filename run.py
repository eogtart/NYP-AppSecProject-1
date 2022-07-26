from website import app
from website import admin_user


if __name__ == '__main__':


    app.run(host='127.0.0.1', debug=True, use_reloader=False, ssl_context=('appsec+3.pem', 'appsec+3-key.pem'))
    # Whoever who enabled debugger mode in production, you're fired.



