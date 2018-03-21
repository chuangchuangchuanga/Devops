#conding: utf-8

import sys
# sys.path.append('..')


from library.new_main import main

option=["-H", "192.168.1.144", "-u", "root", "-i", "id_rsa", "git"]

if __name__ == "__main__":
    main(option)
