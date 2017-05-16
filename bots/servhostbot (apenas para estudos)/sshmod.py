import fabric
from fabric.api import env, sudo, local, settings
import config

env.user = 'franklin'
env.host_string = '94.177.241.134'
env.password = config.senha_sudo

def useradd(nome, senha):
    env.password = config.senha_sudo
    resultado = sudo("useradd -M -s /bin/false {0}".format(nome), quiet=True)
    if not resultado.failed:
        sudo("(echo {0} ; echo {0} ) | passwd {1}".format(senha, nome), quiet=True)
        return True
    else:
        return False
