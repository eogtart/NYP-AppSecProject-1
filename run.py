from website import app
from website import admin_user


if __name__ == '__main__':

    app.run(host='0.0.0.0', port='5000', debug=True, use_reloader=False)

    # app.run(host='127.0.0.1', port="5000" ,debug=True, use_reloader=False, ssl_context=('appsec+3.pem', 'appsec+3-key.pem'))
    
    # For VMWARE
    # app.run(host='127.0.0.1', port="5000" ,debug=True, use_reloader=False, ssl_context=('appsec+5.pem', 'appsec+5-key.pem'))



