import http.client

def send_msg(message, webhookurl):

    # compile the form data (BOUNDARY can be anything)
    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; " \
               "name=\"content\"\r\n\r\n" + message + "\r\n------:::BOUNDARY:::--"
    formdata = formdata.encode(encoding='UTF-8')

    # get the connection and make the request
    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
        'charset': "UTF-8"
    })

    # get the response
    response = connection.getresponse()
    result = response.read()

    # return back to the calling function with the result
    return result.decode("utf-8")
