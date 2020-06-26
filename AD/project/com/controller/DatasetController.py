from flask import request, render_template, url_for, redirect
from project import app
from werkzeug.utils import secure_filename
import os
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO
from datetime import datetime
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession

UPLOAD_FOLDER = 'project/static/adminResource/dataset/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset')
def adminLoadDataset():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addDataset.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()
            datasetDAO = DatasetDAO()

            file = request.files['file']
            print(file)

            datasetFilename = secure_filename(file.filename)
            print(datasetFilename)
            now = datetime.now()
            print("now=", now)
            datasetUploadDate = now.strftime("%Y/%m/%d")
            print("date =", datasetUploadDate)
            datasetUploadTime = now.strftime("%H:%M:%S")
            print("time =", datasetUploadTime)

            datasetFilepath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(datasetFilepath)

            file.save(os.path.join(datasetFilepath, datasetFilename))

            datasetVO.datasetFilename = datasetFilename
            datasetVO.datasetUploadDate = datasetUploadDate
            datasetVO.datasetUploadTime = datasetUploadTime

            datasetVO.datasetFilepath = datasetFilepath.replace("project", "..")

            datasetDAO.insertDataset(datasetVO)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/viewDataset')
def adminViewDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetDAO = DatasetDAO()
            datasetVOList = datasetDAO.viewDataset()
            print("__________________", datasetVOList)
            return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset')
def adminDeleteDataset():
    try:
        if adminLoginSession() == 'admin':
            datasetVO = DatasetVO()

            datasetDAO = DatasetDAO()

            datasetId = request.args.get('datasetId')

            datasetVO.datasetId = datasetId

            datasetList = datasetDAO.deleteDataset(datasetVO)
            print(datasetList)

            path = datasetList.datasetFilepath.replace("..", "project") + datasetList.datasetFilename

            os.remove(path)

            return redirect(url_for('adminViewDataset'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
