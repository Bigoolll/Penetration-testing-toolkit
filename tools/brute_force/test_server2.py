from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('UserName')
        password = request.form.get('Password')
        
        if username == 'testuser' and password == 'secret':
            return "Login successful!"
        return "Invalid credentials"
    
    html = '''
    <form method="post">
        <input type="text" name="UserName" placeholder="Username">
        <input type="password" name="Password" placeholder="Password">
        <input type="submit" name="Log In" value="submit">
    </form>
    '''
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000)