#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Markup
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ueditor/', methods=['GET', 'POST'])
def ueditor():
    action = request.args.get("action", "")
    if action == 'config':
        return jsonify(get_config())
    elif action == 'uploadimage':
        return jsonify(upload_image())
    elif action == 'listimage':
        return jsonify(list_images())
    return ''

@app.route('/show/', methods=['GET', 'POST'])
def show():
    content = request.form['content']
    return render_template('display.html',content=content)



def get_config():
    return {
            # "imagePath": "/upload_image",
            "imageActionName": "uploadimage",
            "imageFieldName": "upfile",
            "imageMaxSize": 2048000,
            "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif"],
            "imageCompressEnable": True,
            "imageCompressBorder": 1600,
            "imageInsertAlign": "none",
            #返回路径的添加前缀
            "imageUrlPrefix": "",
            "imagePathFormat": "",
            #list images
            #列出指定目录下的图片
            "imageManagerActionName":"listimage",
            # imageManagerActionName {String} [默认值："listimage"] //执行图片管理的action名称
            # imageManagerListPath {String} [默认值："/ueditor/php/upload/image/"] //指定要列出图片的目录
            # imageManagerListSize {String} [默认值：20] //每次列出文件数量
            # "imageManagerUrlPrefix":"http://ueditor.baidu.com",
            "imageManagerUrlPrefix":"http://127.0.0.1:5000/static/upload/",
            # imageManagerUrlPrefix {String} [默认值：""] //图片访问路径前缀
            # imageManagerInsertAlign {String} [默认值："none"] //插入的图片浮动方式
            # imageManagerAllowFiles {Array}, //列出的文件类型
            }


def upload_image():
    import hashlib
    file_storage = request.files['upfile']
    name, extension = os.path.splitext(file_storage.filename)
    m = hashlib.md5()
    m.update(name)
    name = m.hexdigest()
    filename = name + extension
    file_path = os.path.join("static/upload/", filename)
    file_storage.save(file_path)
    return {"state": "SUCCESS",
            "url": '/'+file_path,
            "title": file_storage.filename,
            "original": file_storage.filename,
            "type": extension,
            "size": ""}


def list_images():
    folder = 'static/upload/'
    r = os.listdir(folder)
    images = [{'url': i} for i in r]
    total = len(images)
    start = 0
    return {'state': 'SUCCESS', 'list': images, 'start': start, 'total': total}


if __name__ == '__main__':
    app.run(debug=True)
