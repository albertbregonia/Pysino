import os

#checks for full setup and returns 'full' if true, otherwise prints error messages
def fullSetup(server, user):
    if os.path.exists(server):
        if os.path.exists(user):
            return 'full'
        else:
            return ', please run `*register` before you use this command.'
    return ', please run `*setup` before you use this command.'