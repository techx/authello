from authenticate import app

app.config.from_object('authenticate.config.DevConfig')
app.run()
