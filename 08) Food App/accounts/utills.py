def detect(user):
    if user.role ==1:
        redirecturl = 'vendordashboard'
    elif user.role ==2:
        redirecturl = 'custdashboard'
    elif user.role ==None and user.issuperadmin:
        redirecturl = 'admin'
    return redirecturl
