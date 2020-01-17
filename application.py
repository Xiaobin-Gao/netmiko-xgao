# from __future__ import print_function, division, absolute_import # makes Python2 behaves like Python3
from flask import Flask, render_template, request, flash
import netmiko

application = app = Flask(__name__)
app.secret_key = 'ssssss'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.form['ip']
        dtype = request.form['dtype']
        uname = request.form['uname']
        pwd = request.form['pwd']
        if not ip or not dtype or not uname or not pwd:
            flash('All fields are required.')
        else:
            try:
                global conn
                conn = netmiko.ConnectHandler(ip=ip, device_type=dtype, username=uname, password=pwd)
                flash("You have successfully connected to device: " + conn.host, "succeed")
                return render_template('enter-command.html', conn = conn)
            except (netmiko.ssh_exception.NetmikoTimeoutException, netmiko.ssh_exception.NetmikoAuthenticationException) as e:
                flash(e, 'Error')
    with open('device_type_supported.txt', 'r') as dtype_file:
        device_supported = []
        for line in dtype_file.readlines():
            line = line.rstrip()
            device_supported.append(line)
    return render_template('index.html', devices = device_supported)

@app.route('/runcomand')
def run_command():
    cmd = request.args.get('cmd')
    if cmd == '':
        flash("Please enter a command.")
        return render_template('enter-command.html', conn=conn)
    try:
        result = conn.send_command(cmd)
    except:
        return '''
            <a href="/">>>>Please reconnect to device(Timeout Error)</a>
        '''
    result2 = []
    lines = result.split('\n')
    for line in lines:
        line = line.split()
        result2.append(line)
    return render_template('enter-command.html', conn=conn, cmd=cmd, result=result2)

if __name__ == '__main__':
    app.run(debug=True)