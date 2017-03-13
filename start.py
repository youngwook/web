from web import app

if __name__ == "__main__":
    app.debug = True
    app.run(host="192.168.56.101")