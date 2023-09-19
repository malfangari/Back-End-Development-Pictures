from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        picture_URLs = [] 
        for picture in data:
            picture_URLs.append(picture)
        return jsonify(picture_URLs),200
    #pass

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    query = id
    matching  = None
    for picture in data:
        if query == picture["id"]:
            matching = picture
            break
    if matching:    
        return jsonify(dict(matching)), 200
    else:
        return {"message": "picture not found"}, 404
    #pass


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.get_json()
    if data:
        flag = False
        for exist_pic in data:
            if exist_pic["id"] == new_pic["id"]:
                flag = True
                break
        if flag == True:
           return {"Message":  f"picture with id {exist_pic['id']} already present"},302
        else:
            data.append(new_pic)
            return {"Message": "Picture added successfully"},201
   #pass

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pic = request.get_json()
    if data:
        flag = False
        for exist_pic in data:
            if exist_pic["id"] == id:
                flag = True
                break
        if flag == True:   
            exist_pic["pic_url"] = new_pic["pic_url"]
            exist_pic["event_country"] = new_pic["event_country"]
            exist_pic["event_state"] = new_pic["event_state"]
            exist_pic["event_city"] = new_pic["event_city"]
            exist_pic["event_date"] = new_pic["event_date"]
            return {"message": f"Pictuer Number:  {id}  is updated"},202
        else:
            return {"message": "picture not found"},404
    #pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data
    to_be_deleted = id
    flag = False
    if data:
       for exist_pic in data:
          if exist_pic["id"] == id:
             flag = True
             break
       if flag == True:   
          data = [item for item in data if item["id"] != to_be_deleted]
          return jsonify(dict(status="HTTP_204_NO_CONTENT")), 204
       else:
          return {"message": "picture not found"},404
    #pass