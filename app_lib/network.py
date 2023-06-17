class Network():

    def scan_networks(self,access_point):
        all_networks = access_point.scan()
        wifi_networks = []
        for network in all_networks:
            item = network[0]
            wifi_networks.append(item)
        return wifi_networks


    def wifi_networks_options(self,wifi_networks):
        # need to create a string with all the wifis
        # this is required as the javascript in the front end will populate a dropdown
        # it is not possible to implement a loop directly through the form
        print("here inside")
        options_str = ""
        for option in wifi_networks:
            options_str += f"{option.decode('utf-8')}" + "---"
        print("options_str:")
        print(options_str)
        return options_str