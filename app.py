# Básicamente éste código es de una aplicación web basada en el framework de Python llamado Flask

# Para que funcione ésta aplicación necesitamos de dos herramientas: Redis y Flask

import time # modulo de python el cual nos permite poder esperar un tiempo
            # para ejecutar determinada sentencia o determinada tarea dentro del código.

# Redis es una aplicación de db, tendríamos que instalar la db
# Entonces para ésto vamoa a utilizar Docker.
import redis # módulo de conexión de python hacia la db Redis
from flask import Flask # flask es un módulo, lo cual lo podemos instalar con pip

app = Flask(__name__) # ejecución de Flask
cache = redis.Redis(host='redis', port=6379) # ejecución de Redis
# conexión de python con redis
# nota que no esta tipeado localhost sino 'redis'

# intentar hacer reconexiones en caso de que la db este caída
# y si no se conecta no podrá guardar datos en la db
def get_hit_count(): # Fx para incrementar un contador de uno en uno
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/about')
def about():
    return "<h1>About</h1>"
