from website import app
from website import admin_user


if __name__ == '__main__':


    app.run(debug=True)
    # Ensure that debugger is set to FALSE after we're done with app sec dev.

    app.run(debug=True, ssl_context=('appsec+3.pem', 'appsec+3-key.pem'))
    # Whoever who enabled debugger mode in production, you're fired.



