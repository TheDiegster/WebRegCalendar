from flask import Blueprint, render_template, request, send_file, redirect, url_for
import dataParser
views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template('index.html', name="Diego")

@views.route("/", methods=['POST'])
def user_schedule():
    data = request.files.get("webregFile")
    dataParser.dataParser(data)
    return redirect(url_for('views.success'))

@views.route("/success")
def success():
    return render_template('success.html')

@views.route("/success/download")
def download():
    return send_file('dataParserOutput.ics',
                        mimetype='text/calendar',
                        as_attachment=True,
                        download_name='yourSchedule.ics')
