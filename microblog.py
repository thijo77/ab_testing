from app import app, db
from app.models import User, Post, Testeur

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Testeur': Testeur}
    
from app import app

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)



