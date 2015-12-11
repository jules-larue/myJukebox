from .app import app, manager, db
import app.commands

if __name__=="__main__":
    manager.run()
