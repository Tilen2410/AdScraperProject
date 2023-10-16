from flask import Flask, render_template
import psycopg2


app = Flask("apartment_ads")

@app.route("/")
def index():
    try:
        conn = psycopg2.connect(
            #host="localhost",
            host="postgres",
            database="ads",
            user="postgres",
            password="postgres",
            port="5432"
        )

        cur = conn.cursor()

        cur.execute("SELECT * FROM apartments;")
        data = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('index.html', data=data)
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)