import env


def loadConf(environ):
    match environ:
        case "src":
            return {
                "host": env.ipSrc,
                "port": env.portSrc,
                "user": env.userSrc,
                "password": env.passSrc,
                "database": "",
            }
        case "dst":
            return {
                "host": env.ipDst,
                "port": env.portDst,
                "user": env.userDst,
                "password": env.passDst,
                "database": "",
            }
        case default:
            return None
