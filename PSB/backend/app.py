
from flask import Flask, render_template, jsonify, request

import sentetic_data as sentetic_data
import operator as op



data = sentetic_data.get_final_data()

app = Flask(__name__)


@app.route('/')
def main():
    return "main page i guess"



@app.route("/data")
def gen_data():
    return data
    # return sentetic_data.get_data()



@app.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search_term', '').lower()

    if not search_term:
        return jsonify({"res":"nodata"})
    
    # filter dataframe
    # data = sentetic_data.get_final_data()
    filtered = data[
        data["inn"].astype(str).str.contains(search_term) |
        data["name"].astype(str).str.contains(search_term) |
        data["reason"].astype(str).str.contains(search_term)
    ]

    print(filtered.head)
    return jsonify(filtered.to_dict("records"))

# for tesing
@app.route("/reload_data")
def reload_data():
    global data
    data= sentetic_data.get_final_data()
    return "reloaded"

@app.route('/table')
def table_page():
    
    # request actual data from db processed by ml model
    # table_data = data #sentetic_data.get_final_data().to_dict("records")
    return render_template("table.html", table_data=data.to_dict("records"))



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
    
    # get data from db
    data = sentetic_data.get_data()

    app.run()
