import pandas as pd
import utility

hosts = pd.read_excel(utility.get_hosts_export())

if __name__ ==  '__main__':

    device_inventory = pd.read_csv('/mnt/c/Users/jules.shearer/Downloads/DevicesWithInventory_99ae7db0-8855-4f6b-9ffb-bb596ff8146d.csv')
    hosts = pd.read_excel(utility.get_hosts_export())

