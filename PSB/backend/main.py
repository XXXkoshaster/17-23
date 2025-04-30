

import db.session as di

from fastapi import FastAPI


app = FastAPI()




@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/download")
async def download():
    return {"message": "Hello World"}

@app.get("/load")
async def get_chunk():
    return di.load("sentetic_data").to_dict("records")



# from io import BytesIO
# from flask import Flask, render_template, jsonify, request, session, send_file, Response
# from flask_cors import CORS



# import sentetic_data as sentetic_data
# import datetime
# import pandas as pd
# import gzip

# def load_data():
#     data = sentetic_data.get_final_data()
#     session['data'] = data.to_dict("records")
#     session["filtered"] = session["data"]


# app = Flask(__name__)
# CORS(app)

# app.secret_key = "yout-secret-key"

# @app.route('/download', methods=['POST'])
# def download():    
#     time_stamp_now = datetime.datetime.now() #.strftime("%y_%m_%d_%s")
    
#     return Response(
#         pd.DataFrame().from_dict(session["filtered"]).to_csv(),
#         mimetype='text/csv',
#         headers={'Content-disposition': 'attachment; filename=data.csv'}
#     )



# @app.route('/search', methods=['POST'])
# def search():
#     search_term = request.form.get('search_term', '').lower()

#     if not search_term:
#         return jsonify({"res":"nodata"})
    
#     # filter dataframe
#     data = pd.DataFrame(session["data"])
#     session["filtered"] = data[
#         data["inn"].astype(str).str.contains(search_term) |
#         data["name"].astype(str).str.contains(search_term) |
#         data["reason"].astype(str).str.contains(search_term)
#     ].to_dict("records")

#     return jsonify(session["filtered"])



# # for tesing
# @app.route("/reload")
# def reload_data():
#     # global data
#     load_data()

#     return "reloaded"



# @app.route('/')
# def table_page():

#     load_data()
#     # request actual data from db processed by ml model
#     # table_data = data #sentetic_data.get_final_data().to_dict("records")
#     return render_template("table.html", table_data=session["filtered"])



# @app.route('/organization/info/<inn>')
# def extansive_info_page(inn):

#     # data_html = generate_data.get_data().to_html(classes='table table-striped table-hover table-bordered',
#     #     index=False,
#     #     escape=False,
#     #     border=1)
    
#     # request actual data from db
#     organization_data = sentetic_data.get_organization_data(inn)

#     return render_template("organization_info.html", organization_data=organization_data)



# @app.route('/table_simple')
# def table_apge_simple():
#     return render_template("table_simple.html")



# if __name__ == '__main__':
    
#     # get data from db
#     # data = sentetic_data.get_data()

#     app.run(debug=True)
