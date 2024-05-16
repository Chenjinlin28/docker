import time
import redis
from flask import Flask, render_template, url_for
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name="BIPM", count=count)

@app.route('/titanic')
def titanic(): 
    df = pd.read_csv('titanic.csv')
    titanic_data = df.head().to_html(classes='table table-striped', border=0)
    survival_counts = df[df['survived'] == 1]['sex'].value_counts().reset_index()
    survival_counts.columns = ['Sex', 'Count']
    plt.figure(figsize=(10, 5))
    plt.bar(survival_counts['Sex'], survival_counts['Count'], color=['blue', 'pink'])
    plt.title('Survival Counts by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Number of Survivors')
    image_path = 'static/survival_counts.png'
    plt.savefig(image_path)
    plt.close()
    image_url = url_for('static',filename='survival_counts.png')
    return render_template('titanic.html', titanic_data=titanic_data,image_path=image_url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
