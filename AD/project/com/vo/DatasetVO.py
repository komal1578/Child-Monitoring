from project import db


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetId = db.Column('datasetId', db.Integer, primary_key=True, autoincrement=True)
    datasetFilename = db.Column('datasetFilename', db.String(100))
    datasetFilepath = db.Column('datasetFilepath',db.String(100))
    datasetUploadDate = db.Column('datasetUploadDate', db.Date)
    datasetUploadTime = db.Column('datasetUploadTime', db.Time)

    def as_dict(self):
        return {
            'datasetId': self.datasetId,
            'datasetFilename': self.datasetFilename,
            'datasetFilepath': self.datasetFilepath,
            'datasetUploadDate': self.datasetUploadDate,
            'datasetUploadTime':self.datasetUploadTime
        }


db.create_all()
