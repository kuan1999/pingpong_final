from games.pingpong.ml.Moduls import CSV_Read_1P
"""
The template of the script for the machine learning process in game pingpong
"""

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the MLPlay is used by
               which side.
        """
        self.ball_served = False
        self.side = "1P"

    def update(self, scene_info):
        # Make the caller to invoke reset() for the next round.
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else: 
            #print(scene_info)
            BallCoordinate_Now = scene_info["ball"]
            ball_speed = scene_info["ball_speed"]
            BallCoordinate_Last = (BallCoordinate_Now[0] + ball_speed[0] , BallCoordinate_Now[1] + ball_speed[1])
            PlatformX = scene_info["platform_1P"][0] + 20
            PlatformY = scene_info["platform_1P"][1] + 20
            PlatformX_2P = scene_info["platform_2P"][0] + 20
            PlatformY_2P = scene_info["platform_2P"][1] + 20
            Frame = scene_info["frame"]
            BallUpAndDown = ''
            aid = 0
            m = 1
            BallUpAndDown_NUM = 0
            if BallCoordinate_Now[0] - BallCoordinate_Last[0] != 0:
                m = ball_speed[1] / ball_speed[0]
                aid = BallCoordinate_Now[0] + ((420 - BallCoordinate_Now[1]) / ball_speed[1] * ball_speed[0])

            if aid < 0:
                aid = -aid
            elif aid > 200:
                aid = aid - 200
                aid = 200 - aid
            
            if BallCoordinate_Now[1] - BallCoordinate_Last[1] > 0:
                BallUpAndDown = 'Down'
                BallUpAndDown_NUM = 0
            else:
                BallUpAndDown = 'Up'
                BallUpAndDown_NUM = 1
            CSV_Read_1P.doWrite(Frame, BallCoordinate_Now[0], BallCoordinate_Now[1], m, ball_speed[0], ball_speed[1], PlatformX, PlatformY, PlatformX_2P, PlatformY_2P, BallUpAndDown_NUM)

            if BallUpAndDown == 'Up' and PlatformX > aid :
                return "MOVE_LEFT"
            if BallUpAndDown == 'Up' and PlatformX < aid :
                return "MOVE_RIGHT"

            if BallUpAndDown == 'Down' and PlatformX < 100:
                return "MOVE_RIGHT"

            if BallUpAndDown == 'Down' and PlatformX > 100:
                return "MOVE_LEFT"
                
            if BallUpAndDown == 'Down' and PlatformX == 100:
                return "NONE"

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False