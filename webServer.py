from flask import Flask, request, send_file
import dataParser
import io
app = Flask(__name__)

@app.route("/")
def test():
    # create file in directory

    # TODO: Create HTML form that requests pdf file from client

    #dataParser.dataParser('examplePDFs/todiego.pdf')
    dataParser.dataParser('examplePDFs/webregMain.pdf')
    call = send_file('dataParserOutput.ics',
                mimetype = 'text/calendar',
                as_attachment = True,
                download_name = 'WebRegCalendar.ics')
    return call
    # "<title> WebReg AutoCalendar </title> <h1> Hewo Wurld </h1>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)