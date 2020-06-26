from project import db
from project.com.vo.LoginVO import LoginVO


class VideoVO( db.Model ):
    __tablename__ = 'videomaster'
    videoId = db.Column( 'videoId', db.Integer, primary_key=True, autoincrement=True )
    videoInputFileName = db.Column( 'videoInputFileName', db.String( 100 ), nullable=False )
    videoInputFilePath = db.Column( 'videoInputFilePath', db.String( 100 ), nullable=False )
    videoOutputFileName = db.Column( 'videoOutputFileName', db.String( 10 ), nullable=False )
    videoOutputFilePath = db.Column( 'videoOutputFilePath', db.String( 100 ), nullable=False )
    videoUploadDate = db.Column( 'videoUploadDate', db.String( 100 ), nullable=False )
    videoUploadTime = db.Column( 'videoUploadTime', db.String( 100 ), nullable=False )
    video_LoginId = db.Column( 'video_LoginId', db.Integer, db.ForeignKey( LoginVO.loginId ) )

    def as_dict(self):
        return {
            'videoId': self.videoId,
            'videoInputFileName': self.videoInputFileName,
            'videoInputFilePath': self.videoInputFilePath,
            'videoOutputFileName': self.videoOutputFileName,
            'videoOutputFilePath': self.videoOutputFilePath,
            'videoUploadDate': self.videoUploadDate,
            'videoUploadTime': self.videoUploadTime,
            'video_LoginId': self.video_LoginId
        }


db.create_all()
