
from flask import Flask, render_template

import sentetic_data as sentetic_data

app = Flask(__name__)


@app.route('/')
def main():
    return "main page i guess"



@app.route("/data")
def gen_data():
    return sentetic_data.get_data()



@app.route('/table')
def table_page():
    
    # request actual data from db processed by ml model
    table_data = sentetic_data.get_final_data().to_dict("records")

    return render_template("table.html", table_data=table_data)



@app.route('/organization/info/<inn>')
def extansive_info_page(inn):

    # data_html = generate_data.get_data().to_html(classes='table table-striped table-hover table-bordered',
    #     index=False,
    #     escape=False,
    #     border=1)
    
    # request actual data from db
    organization_data = sentetic_data.get_organization_data(inn)

    return render_template("organization_info.html", organization_data=organization_data)



@app.route('/table_simple')
def table_apge_simple():
    return render_template("table_simple.html")



if __name__ == '__main__':
    app.run()
