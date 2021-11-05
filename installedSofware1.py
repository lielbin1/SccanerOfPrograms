import winreg
from winreg import QueryValueEx, EnumKey

hkey_dict = {winreg.HKEY_LOCAL_MACHINE: 'HKEY_LOCAL_MACHINE', winreg.HKEY_CURRENT_USER: 'HKEY_CURRENT_USER'}
dir_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"


def print_lists(lst):
    for k, elm in enumerate(lst):
        print("{}: {}".format(k, elm))


class RegistryConnection:
    def __init__(self):
        self.registry_cursor = ''

    def connect_to_registry(self, key):
        self.registry_cursor = winreg.ConnectRegistry(None, key)

    def open_reg_element_by_key(self, connection_cursor, key):
        try:
            return winreg.OpenKey(connection_cursor, key)
        except EnvironmentError:
            print("***cursor is empty ***")

    def get_software_data_by_field(self, software_key, requested_data_field):
        return QueryValueEx(software_key, requested_data_field)

    def get_software_enum_key(self, directory_conn, software_index):
        return EnumKey(directory_conn, software_index)


if __name__ == "__main__":
    requested_data_field = "DisplayName"  # choose here which field you need
    reg_conn = RegistryConnection()
    for hkey in hkey_dict:
        software_lst = []
        reg_conn.connect_to_registry(hkey) # establish connection to registry
        dir_conn = reg_conn.open_reg_element_by_key(reg_conn.registry_cursor, dir_path) # establish connection to registry dir
        for i in range(1024):
            try:
                software_key = reg_conn.get_software_enum_key(dir_conn, i)
                software_conn = reg_conn.open_reg_element_by_key(dir_conn, software_key) # establish connection to software file
                val = reg_conn.get_software_data_by_field(software_conn, requested_data_field)
                software_lst.append(val)
            except FileNotFoundError:
                continue
            except EnvironmentError:
                print(r"*** %s files was found in %s ***" % (i, hkey_dict[hkey]))
                print_lists(software_lst)
                break
