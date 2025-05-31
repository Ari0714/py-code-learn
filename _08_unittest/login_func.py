


def login_func(username,password):
    if(username == 'admin' and password == 'admin'):
        return {'msg': 'login success'}
    else:
        return {'msg':'login fail, username or password is wrong'}


if __name__ == '__main__':
    print(login_func('admin','admin666'))



