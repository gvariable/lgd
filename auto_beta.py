import os
import random
import time

beta_file = "/sys/module/tcp_lgd/parameters/beta"


def change_beta(beta):
    """
    change the beta in congestion control process
    """
    if os.access(beta_file, os.R_OK) == False:
        print(f"Take action failed! {beta_file} is not writable!\n")
        return False
    f = open(beta_file, 'w', encoding="utf-8")
    f.write(str(beta))
    f.close()


if __name__ == "__main__":
    while 1:
        time.sleep(0.001)
        beta = random.randint(1, 10)
        change_beta(beta)
