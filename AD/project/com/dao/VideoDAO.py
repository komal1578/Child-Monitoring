from project import db
from project.com.vo.VideoVO import VideoVO
from project.com.vo.LoginVO import LoginVO


class VideoDAO:
    def insertVideo(self, videoVO):
        db.session.add( videoVO )
        db.session.commit()

    def viewVideo(self, videoVO):
        videoVOList = VideoVO.query.filter_by( video_LoginId=videoVO.video_LoginId ).all()
        return videoVOList

    def adinViewVideo(self):
        videoVOList = db.session.query( VideoVO, LoginVO ).join( LoginVO,
                                                                 VideoVO.video_LoginId == LoginVO.loginId ).all()

        return videoVOList

    def deleteVideo(self, videoVO):
        videoVOList = VideoVO.query.get( videoVO.videoId )
        db.session.delete( videoVOList )
        db.session.commit()

        return videoVOList
