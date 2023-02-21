from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/slice', methods=['POST'])
def slice_file():
    file = request.files['file']
    file_path = './uploaded_files/' + file.filename
    file.save(file_path)
    # Run CuraEngine to slice the file
    command = ['slic3r','--load','slic3r-profiles/Creality.ini,'+file_path,'--output','../sliced_files/'+file.filename+'.gcode']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout,stderr)
    # Parse the print time from the CuraEngine output
    print_time = None
    for line in stdout.decode('utf-8').split('\n'):
        if line.startswith('Print time'):
            print_time = line.split(': ')[1]
            break

    # Return the print time
    if print_time:
        return {'print_time': print_time}
    else:
        return {'error': 'Failed to parse print time.'}

if __name__ == '__main__':
    app.run(debug=True)
