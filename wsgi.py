import os
import urllib.request, json

def application(environ, start_response):

    ctype = "text/plain"
    if environ['PATH_INFO'] == "/health":
        file_body = "1"
    elif environ['PATH_INFO'] == "/env":
        file_body = ["%s: %s" % (key, value)
                    for key, value in sorted(environ.items())]
        file_body = '\n'.join(file_body)
    elif environ["PATH_INFO"].startswith("/img"):

       ctype = "image/jpeg"

       FileLoc = environ["PATH_INFO"][1:]
       #Location of static resources which is different in the deployment of the website
       if __name__ == "__main__":
         TestLoc = FileLoc
       else:
         TestLoc = environ["OPENSHIFT_REPO_DIR"]+FileLoc

       image = open(TestLoc, "rb")

       status = "200 OK"
       response_headers = [('Content-Type', ctype)]
   
       start_response(status, response_headers)
       if "wsgi.file_wrapper" in environ:
           return environ["wsgi.file_wrapper"](image, 1000)
       else:
           return iter(lambda: image.read(1000), "")

    elif environ["PATH_INFO"] == "/":
        ctype = "text/html"

        FileLoc = "Test.html"
        #
        if __name__ == "__main__":
          TestLoc = FileLoc
        else:
          TestLoc = environ["OPENSHIFT_REPO_DIR"]+FileLoc


        myfile = open(TestLoc, "r")

        file_body = myfile.read();

        myfile.close()


        url_obj = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?units=metric&q=London,uk")
         
        str_JSON = url_obj.readall().decode("utf-8")

        dataWeather = json.loads(str_JSON)

        #converted to int to lose decimal places when grabbing the weather data from the api
        windspeed = str(int(dataWeather["wind"]["speed"]))

        maxtemp = str(dataWeather["main"]["temp_max"])

        mintemp = str(dataWeather["main"]["temp_min"])

        temp = str(dataWeather['main']["temp"])

        humidity = str(int(dataWeather["main"]["humidity"]))

        description = str(dataWeather["weather"][0]["description"])

        name = str(dataWeather["name"])

        weather = str(dataWeather["weather"][0]["main"]).lower()


        file_body = file_body.replace("#windspeed", windspeed)

        file_body = file_body.replace("#maxtemp", maxtemp)

        file_body = file_body.replace("#mintemp", mintemp)

        file_body = file_body.replace("#temp", temp)

        file_body = file_body.replace("#weather", weather)

        file_body = file_body.replace("#description", description)

        file_body = file_body.replace("#name", name)

        file_body = file_body.replace("#humidity", humidity)

        #if statements for loading the correct image to th html



        print(weather)
        if weather == "clear":
            image = "/img/image1.png"
        elif weather == "thunderstorm" or weather == "rain":
            image = "/img/image2.png"
        elif weather == 'drizzle':
            image = "/img/image3.png"
        elif weather== "snow" or weather == "extreme":
            image = "/img/image4.png"
        elif weather == "clouds":
            image = "/img/image5.png"
 
        file_body = file_body.replace("#IMAGE", image)


    else:
        if environ["PATH_INFO"].endswith(".html"):
           ctype = "text/html"
        elif environ["PATH_INFO"].endswith(".css"):
           ctype = "text/cssv"
        elif environ["PATH_INFO"].endswith(".js"):
           ctype = "text/js"

            

        FileLoc = environ["PATH_INFO"][1:]
        #Reading the repsonse from the file
        if __name__ == "__main__":
         TestLoc = FileLoc
        else:
         TestLoc = environ['OPENSHIFT_REPO_DIR']+FileLoc
         
        fo = open(TestLoc, "r")
        file_body = fo.read();
        fo.close()

    status = "200 OK"
    response_headers = [("Content-Type", ctype), ("Content-Length", str(len(file_body)))]
    #
    start_response(status, response_headers)
    return [file_body.encode("utf-8") ]

#
# Below for testing only on own webserver only
#
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server("localhost", 8051, application)
    # Wait for a single request, serve it and quit.
    while(True):
     httpd.handle_request()
