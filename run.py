from app import create_app
from config import get_config

# Criar app com configurações
config = get_config()
app = create_app(config)

if __name__ == '__main__':
    # Usar configurações do .env
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
