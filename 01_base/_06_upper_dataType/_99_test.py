
# 1、user login system

# 用户名、密码、黑名单
users = {
    '小红':{'name':'小红', 'password':'123', 'status':True},
    'mia':{'name':'mia', 'password':'456', 'status':True},
    'jack':{'name':'jack', 'password':'789', 'status':False},
}

for i in range(3):
    user = input('please input user:')
    pwd = input('please input pwd:')
    if (user in users and pwd == users[user]['password'] and users[user]['status']):
        print('login success')
        break
    else:
        print('user or passwd error')


# 2、user login system
