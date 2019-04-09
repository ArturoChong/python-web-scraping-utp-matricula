import selenium, sys

def get_credentials():
    credentials = {'user': '', 'password':''}
    if len(sys.argv) == 3:
        credentials['user'] = str(sys.argv[1])
        credentials['password'] = str(sys.argv[2])
    return credentials
def print_credentials(credentials):
    print(f'User: {credentials["user"]} \nPassword: {credentials["password"]}')
credentials = get_credentials()
print_credentials(credentials)
url = 'http://matricula.utp.ac.pa/'
