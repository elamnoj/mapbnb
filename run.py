
from app import create_app, db 
from app.models import Submit
from app.blueprints.authentication.models import User

app = create_app()

@app.shell_context_processor
def make_shell_contextP():
    return {
        'db': db,
        'User': User,
        'Submit': Submit
    }