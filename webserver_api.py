from phew import access_point, connect_to_wifi, is_connected_to_wifi, dns, server
from phew.server import redirect
from phew.template import render_template
# from network import WLAN
import json
import machine
import os
import utime
# from app_lib.ultrasonic import ultra
import _thread

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
# from motor_main import Motor_Main
# from servo_new import Servo
from app_lib.network import Network
from app_lib.motor import Motor_Main
from app_lib.servo import Servo

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=40000)
oled = SSD1306_I2C(128, 64, i2c)

AP_NAME = "PicoRobot"
AP_PASSWORD = "PicoRobot"
AP_DOMAIN = "pipico.net"
TEMPLATE_PATH = "templates"
# FRONT_CAMERA_IP = "192.168.2.243"

# initial IP addresses for cameras
FRONT_CAMERA_IP = "192.168.2.185"
BACK_CAMERA_IP = "192.168.2.39"

CONFIG_FILE = "config.json"  # include all the configurations here

IP_ADDRESS = ""


def machine_reset():
    utime.sleep(1)
    print("Resetting...")
    machine.reset()


def setup_mode():
    print("Entering setup mode...")

    ap = access_point(AP_NAME, AP_PASSWORD)

    ip = ap.ifconfig()[0]

    print(f'ip:{ip}')
    oled.fill(0)
    oled.text("SSID: PicoRobot", 0, 0)
    oled.text("Pwd: PicoRobot", 0, 10)
    oled.text("use 192.168.4.1", 0, 20)

    oled.show()
    # add code to visualise that the system started as a AP

    dns.run_catchall(ip)
    def ap_index(request):
        print("index")
        print(f"request headers: {request.headers}")
        host = request.headers.get("host")

        # if host != AP_DOMAIN:
        #   print(f"index AP domain different host:{host} AP_DOMAIN:{AP_DOMAIN}")
        #   return render_template(f"{TEMPLATE_PATH}/redirect.html", domain=AP_DOMAIN)

        wifi_networks = network.scan_networks(ap)
        print(f'wifi_networks: {wifi_networks}')

        wifi_options = network.wifi_networks_options(wifi_networks)
        print(f'wifi_options: {wifi_options}')

        return render_template(f"{TEMPLATE_PATH}/ap_index_2.html", wifi_networks_options=wifi_options)

    # verify how this function is called and verify if the application need to be reset
    def ap_configure(request):
        print("Saving wifi credentials...")

        with open(CONFIG_FILE) as f:
            print("Reading json ... ")
            file = json.load(f)
            ip_address = connect_to_wifi(file["ssid"], file["password"])

            if not is_connected_to_wifi():
                print("didnt connected ... ")
                return ap_index(request)  # add a value to let the user know that the connection failed

            print(f"Connected to wifi, IP address {ip_address}")
            application_mode()
            return render_template(f"{TEMPLATE_PATH}/index.html")

        return render_template(f"{TEMPLATE_PATH}/configured.html", ssid=request.form["ssid"])

    def app_connect(request):
        print("inside APP")
        print("form:")
        print(request.form)
        request_string = str(request.form)
        # read the form and save the info on a file
        try:
            # print("inside try")
            if 'button_wifi' in request_string:
                print("inside if")
                with open(CONFIG_FILE) as f:
                    print("inside with")
                    file_string = str(json.load(f))
                    # it is checking with a workaround if the string is in the file
                    if "ap_wifi" in file_string:
                        file_string = {"ap_wifi": "wifi", "ssid": request.form.get('ssid'),
                                       "password": request.form.get('password'), "front_camera_ip": FRONT_CAMERA_IP,
                                       "back_camera_ip": BACK_CAMERA_IP}
                    else:
                        file_string = {"ap_wifi": "wifi", "ssid": request.form.get('ssid'),
                                       "password": request.form.get('password'), "front_camera_ip": FRONT_CAMERA_IP,
                                       "back_camera_ip": BACK_CAMERA_IP}
                os.remove(CONFIG_FILE)
                with open(CONFIG_FILE, "w") as f:
                    json.dump(file_string, f)
                f.close()

                # by using the return ap_configure the pico connect wifi but the parameters remains those of the access point
                # the other option is to restart the machine to restart with the wifi
                ##   return ap_configure(request)
                machine_reset()

            else:
                print("inside else")
                return app_app()
        except Exception:
            print("exception")
            return app_app()

    def app_app():
        print("app_app")
        return render_template(f"{TEMPLATE_PATH}/dashboard_app.html")

    def ap_catch_all(request):
        print("CATCH ALL")

        print(f"request headers: {request.headers}")
        host = request.headers.get("host")
        # return render_template(f"{TEMPLATE_PATH}/redirect.html", domain=AP_DOMAIN)
        if host != AP_DOMAIN:
            print(f"index AP domain different host:{host} AP_DOMAIN:{AP_DOMAIN}")
            return redirect("http://192.168.4.1/")
        return "Not found.", 404

    def ap_config(request):
        print("ap_config")
        request_string = str(request.form)
        if request.method == "POST":
            print(f'request: {request}')
            ap_wifi = request.form.get("ap_wifi")
            #            workaround
            if ap_wifi == None:
                ap_wifi = "ap"
            ssid = request.form.get("ssid")
            password = request.form.get("password")
            front_camera_ip = request.form.get("front_camera_ip")
            back_camera_ip = request.form.get("back_camera_ip")
            os.remove(CONFIG_FILE)
            with open(CONFIG_FILE, "w") as f:
                # with open(CONFIG_FILE) as f:
                file_string = {"ap_wifi": ap_wifi,
                               "ssid": ssid,
                               "password": password,
                               "front_camera_ip": front_camera_ip,
                               "back_camera_ip": back_camera_ip}
            # os.remove(CONFIG_FILE)
            with open(CONFIG_FILE) as f:
                json.dump(file_string, f)
            f.close()

            #           add logic to check the save or the restart and code the restarting routine
            if 'save_restart' in request_string:
                print("save and restart")
                machine_reset()

            elif 'save' in request_string:
                wifi_networks = network.scan_networks(ap)
                print(f'wifi_networks: {wifi_networks}')

                wifi_options = network.wifi_networks_options(wifi_networks)
                print(f'wifi_options: {wifi_options}')

                return render_template(f"{TEMPLATE_PATH}/config.html", saved=1, domain=AP_DOMAIN, ap_wifi=ap_wifi,
                                       ssid=ssid, password=password, front_camera_ip=front_camera_ip,
                                       back_camera_ip=back_camera_ip, wifi_networks_options=wifi_options)
            else:
                # restart routine
                print("verify code for the post")
                pass

        elif request.method == "GET":

            with open(CONFIG_FILE) as f:
                file = json.load(f)
                ap_wifi = file["ap_wifi"]
                ssid = file["ssid"]
                password = file["password"]
                front_camera_ip = file["front_camera_ip"]
                back_camera_ip = file["back_camera_ip"]
                f.close()
            # verify how to add elements to template
            wifi_networks = network.scan_networks(ap)

            print(f'wifi_networks: {wifi_networks}')

            wifi_options = network.wifi_networks_options(wifi_networks)
            print(f'wifi_options: {wifi_options}')

            return render_template(f"{TEMPLATE_PATH}/config.html", domain=AP_DOMAIN, ap_wifi=ap_wifi, ssid=ssid,
                                   password=password, front_camera_ip=front_camera_ip, back_camera_ip=back_camera_ip,
                                   wifi_networks_options=wifi_options)


        else:
            pass
            # machine_reset()
        pass

    # print("adding routes")
    server.add_route("/", handler=ap_index, methods=["GET"])
    server.add_route("/connect", handler=app_connect, methods=["POST", "GET"])
    server.add_route("/configure", handler=ap_configure, methods=["POST", "GET"])
    server.add_route("/config", handler=ap_config, methods=["GET", "POST"])

    # print("adding set_callback")
    server.set_callback(ap_catch_all)

    # print("adding access_point")



def application_mode():
    print("Entering application mode.")
    onboard_led = machine.Pin("LED", machine.Pin.OUT)

    def app_index(request):

        if request.method == "GET":
            print("GET")
            return render_template(f"{TEMPLATE_PATH}/dashboard_app.html")
        else:
            print("POST")
            return render_template(f"{TEMPLATE_PATH}/dashboard_app.html")

    def app_app(request):
        if request.method == "POST":
            return render_template(f"{TEMPLATE_PATH}/dashboard_app.html", ip=IP_ADDRESS, ap_wifi=ap_wifi,
                                   front_camera_ip=FRONT_CAMERA_IP, back_camera_ip=BACK_CAMERA_IP)
        return render_template(f"{TEMPLATE_PATH}/dashboard_app.html", ip=IP_ADDRESS, ap_wifi=ap_wifi,
                               front_camera_ip=FRONT_CAMERA_IP, back_camera_ip=BACK_CAMERA_IP)

    def app_toggle_led(request):
        onboard_led.toggle()
        return "OK"

    def app_catch_all(request):
        return "Not found.", 404

    def app_api(request):

        print("api")
        if request.method == "POST":

            print("POST")
            api = request.data.get("frontCameraIp")  # use this if it is from json otherwise use
            # api = request.form.get("key") # use this if it is from form otherwise use
            print("data:")
            for key in request.data:
                print(key)
                print(request.data.get(key))
                # add code to change the parameters
            print(request.data)
            print(f'{api}')

        elif request.method == "GET":
            print("GET")
            if "=" in request.query_string:
                api = request.query_string.split("=")[1]
            else:
                api = "no context"

            print(f'api:{api}')

            # if api == "up":
            #     print("up")
            # elif api == "down":
            #     print("down")
            # elif api == "left":
            #     print("left")
            # elif api == "right":
            #     print("right")
            # else:
            #     print(f'{api}')

        else:
            pass

        return (f'{api}')

    def app_config(request):
        request_string = str(request.form)
        if request.method == "POST":
            print("inside post")
            ap_wifi = request.form.get("ap_wifi")

            #            workaround
            if ap_wifi == None:
                ap_wifi = "ap"

            ssid = request.form.get("ssid")
            password = request.form.get("password")
            front_camera_ip = request.form.get("front_camera_ip")
            back_camera_ip = request.form.get("back_camera_ip")
            # os.stat(CONFIG_FILE)
            print("inside post before deliting file")
            os.remove(CONFIG_FILE)
            with open(CONFIG_FILE, "w") as f:
                #             with open(CONFIG_FILE) as f:
                file_string = {"ap_wifi": ap_wifi,
                               "ssid": ssid,
                               "password": password,
                               "front_camera_ip": front_camera_ip,
                               "back_camera_ip": back_camera_ip}

                FRONT_CAMERA_IP = front_camera_ip
                BACK_CAMERA_IP = back_camera_ip
                print(f'file_string: {file_string}')
                print("inside with")
                json.dump(file_string, f)
                f.close()
            #           add logic to check the save or the restart and code the restarting routine
            if 'save_restart' in request_string:
                machine_reset()

            elif 'save' in request_string:
                wifi_networks = network.scan_networks(wlan)
                print(f'wifi_networks: {wifi_networks}')

                wifi_options = network.wifi_networks_options(wifi_networks)
                print(f'wifi_options: {wifi_options}')

                return render_template(f"{TEMPLATE_PATH}/config.html", ip=IP_ADDRESS, saved=1, domain=AP_DOMAIN,
                                       ap_wifi=ap_wifi,
                                       ssid=ssid, password=password, front_camera_ip=front_camera_ip,
                                       back_camera_ip=back_camera_ip, wifi_networks_options=wifi_options)
            else:
                # restart routine

                pass

        #            return render_template(f"{TEMPLATE_PATH}/config.html", ip=IP_ADDRESS, domain=AP_DOMAIN, ap_wifi=ap_wifi,
        #                                   ssid=ssid, password=password, front_camera_ip=front_camera_ip,
        #                                   back_camera_ip=back_camera_ip)

        elif request.method == "GET":

            # os.stat(CONFIG_FILE)
            with open(CONFIG_FILE) as f:
                file = json.load(f)
                ap_wifi = file["ap_wifi"]
                ssid = file["ssid"]
                password = file["password"]
                front_camera_ip = file["front_camera_ip"]
                back_camera_ip = file["back_camera_ip"]
                f.close()

            # verify how to add elements to template

            # print(f'wlan:{WLAN}')
            #            wifi_networks = network.scan_networks(WLAN)
            wifi_networks = network.scan_networks(wlan)
            print(f'wifi_networks: {wifi_networks}')

            wifi_options = network.wifi_networks_options(wifi_networks)
            print(f'wifi_options: {wifi_options}')

            return render_template(f"{TEMPLATE_PATH}/config.html", ip=IP_ADDRESS, domain=AP_DOMAIN, ap_wifi=ap_wifi,
                                   ssid=ssid,
                                   password=password, front_camera_ip=front_camera_ip, back_camera_ip=back_camera_ip,
                                   wifi_networks_options=wifi_options)

        else:
            pass
        pass

    server.add_route("/", handler=app_index, methods=["GET", "POST"])
    server.add_route("/toggle", handler=app_toggle_led, methods=["GET"])
    server.add_route("/connect", handler=app_app, methods=["GET", "POST"])
    server.add_route("/config", handler=app_config, methods=["GET", "POST"])
    server.add_route("/api", handler=app_api, methods=["GET", "POST"])
    server.set_callback(app_catch_all)


# Figure out which mode to start up in...
try:

    # First check into the configuration file what option the system should start up with
    # this can force to start up with AP or WIFI and evventually change the wifi

    os.stat(CONFIG_FILE)  # verify if it is required ...
    with open(CONFIG_FILE) as f:
        file = json.load(f)
        ap_wifi = file["ap_wifi"]
        ssid = file["ssid"]
        password = file["password"]
        front_camera_ip = file["front_camera_ip"]
        back_camera_ip = file["back_camera_ip"]
        file_string = {"ap_wifi": ap_wifi,
                       "ssid": ssid,
                       "password": password,
                       "front_camera_ip": front_camera_ip,
                       "back_camera_ip": back_camera_ip}
        f.close()

    #        print(f'inside')
    #        config_file = json.load(f)
    #        print(f'config loaded: {config_file}')
    #        ap_wifi = config_file["ap_wifi"]
    #        print(f'ap_wifi: {ap_wifi}')

    if ap_wifi == "ap":
        # json.dump(config_file, f)
        f.close()
        IP_ADDRESS = "192.168.4.1"
        setup_mode()  # starts in AP mode

    else:  # ap_wifi == "WIFI"
        print(f'inside wifi')
        wlan = connect_to_wifi(file["ssid"], file["password"])
        if not is_connected_to_wifi():
            # Bad configuration, delete the credentials file, reboot
            # into setup mode to get new credentials from the user.
            print("Bad wifi connection!")
            print(file)
            # restore the ap and rewrite on the file as a start-up mode or the system will loop post startup

            file["ap_wifi"] = "ap"
            os.remove(CONFIG_FILE)
            with open(CONFIG_FILE, "w") as f:
                json.dump(CONFIG_FILE, f)  # issues with the wifi password restart as ap
                f.close()
            # os.remove(CONFIG_FILE) # change back the ap_wifi to ap and notify that the app will restart i ap mode given wrong credentials
            machine_reset()

        f.close()
        ip_address = wlan.ifconfig()[0]
        print(f"Connected to wifi, IP address {ip_address}")
        IP_ADDRESS = ip_address
        oled.fill(0)
        oled.text("WiFi mode", 0, 0)
        oled.text(ip_address, 0, 15)
        oled.show()
        application_mode()

except Exception as e:
    # Either no wifi configuration file found, or something went wrong,
    # so go into setup mode.
    print("exception")
    print(e)
    setup_mode()

print("netwrok created")
network = Network()

# Start the web server...
print("server created")
server.run()