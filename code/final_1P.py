"""
The template of the script for the machine learning process in game pingpong
"""
#from games.pingpong.ml.Moduls import DropPointCalculator
import math
import time
import os
import pickle
import numpy as np
import csv
import random

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the MLPlay is used by
               which side.
        """
        self.ball_served = False
        self.side = "1P"
        self.ServePosition = random.randrange(20,180, 5) #亂數5的倍數 發球座標
    def update(self, scene_info):
        Mode = "KNN" #KNN or RULE

        # Make the caller to invoke reset() for the next round.
        #------------------------隨機發球------------------------
        #print("self.ball_served>>>> ", self.ball_served)
        if self.ball_served:
            pass
        else:
            #print("self.ServePosition>>> ", self.ServePosition)
            PlatformX = scene_info["platform_1P"][0] + 20
            #print("PlatformX>>> ", PlatformX)
            if PlatformX < self.ServePosition:
                return "MOVE_RIGHT"
            if PlatformX > self.ServePosition:
                return "MOVE_LEFT"
            if PlatformX == self.ServePosition:
                self.Serve = random.randint(0,2)
                #print("Serve>>> ", self.Serve)
                if self.Serve == 1:
                    self.ball_served = True
                    return "SERVE_TO_RIGHT"
                if self.Serve == 2:
                    self.ball_served = True
                    return "SERVE_TO_LEFT"
                else:
                    self.ball_served = True
                    return "SERVE_TO_RIGHT"
        #--------------------------------------------------------
        if Mode == "RULE":
            if scene_info["status"] == "GAME_2P_WIN": #移除失敗log檔, 以利學習
                print('GAME_2P_WIN!!!')
                Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                print(Time)
                time.sleep(1.5)
                print('Discard failed LOGs=> ' + 'ml_NORMAL_1000_' + Time + '.pickle')
                os.remove('/Users/hykuan/Desktop/MLGame-master-1/games/pingpong/log/ml_NORMAL_10_' + Time + '.pickle')
                ball_speed = scene_info["ball_speed"]
                with open('./games/pingpong/ml/RULE_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    writer.writerow([Time ,ball_speed, "Lose", self.ServePosition, self.Serve])
            if scene_info["status"] != "GAME_ALIVE":
                return "RESET"

            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else: 
                BallCoordinate_Now = scene_info["ball"]
                ball_speed = scene_info["ball_speed"]
                BallCoordinate_Last = (BallCoordinate_Now[0] + ball_speed[0] , BallCoordinate_Now[1] + ball_speed[1])
                PlatformX = scene_info["platform_1P"][0] + 20
                BallUpAndDown = ''
                aid = 0
                m = 1
                
                if BallCoordinate_Now[0] - BallCoordinate_Last[0] != 0:
                    m = ball_speed[1] / ball_speed[0]
                    aid = BallCoordinate_Now[0] + ((BallCoordinate_Now[1] - 80) / -m)

                if aid < 0:
                    aid = -aid
                elif aid > 200:
                    aid = aid - 200
                    aid = 200 - aid
                
                if BallCoordinate_Now[1] - BallCoordinate_Last[1] > 0:
                    BallUpAndDown = 'Down'
                else:
                    BallUpAndDown = 'Up'

                if BallUpAndDown == 'up' and PlatformX > aid :
                    return "MOVE_LEFT"
                if BallUpAndDown == 'up' and PlatformX < aid :
                    return "MOVE_RIGHT"

                if BallUpAndDown == 'Down' and PlatformX < 100:
                    return "MOVE_RIGHT"

                if BallUpAndDown == 'Down' and PlatformX > 100:
                    return "MOVE_LEFT"
                    
                if BallUpAndDown == 'Down' and PlatformX == 100:
                    return "NONE"
                    
        if Mode == "KNN":
            filename = "/Users/hykuan/Documents/machinelearning/MLGame-master-1/games/pingpong/ml/Knn1pf.sav"
            model = pickle.load(open(filename, 'rb'))
            '''
            if scene_info["status"] == "GAME_2P_WIN": #移除失敗log檔, 以利學習
                print('GAME_2P_WIN!!!')
                Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                print(Time)
                time.sleep(1)
                print('Discard failed LOGs=> ' + 'ml_NORMAL_30_' + Time + '.pickle')
                os.remove('D:/※NKFUST/00-學期科目資料/109 academic year/機器學習/MLGame-master/games/pingpong/log/ml_NORMAL_30_' + Time + '.pickle')
                ball_speed = scene_info["ball_speed"]
                with open('./games/pingpong/ml/Knn_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    writer.writerow([Time ,ball_speed, "Lose", self.ServePosition, self.Serve])
            if scene_info["status"] == "GAME_1P_WIN":
                with open('./games/pingpong/ml/Knn_lose_1P_log.csv', 'a+', newline='') as csvfile: #a+ => 追加
                    writer = csv.writer(csvfile)
                    Time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
                    ball_speed = scene_info["ball_speed"]
                    writer.writerow([Time ,ball_speed, "WIN", self.ServePosition, self.Serve])
            '''
            if scene_info["status"] != "GAME_ALIVE":
                return "RESET"
                
            if not self.ball_served:
                self.ball_served = True
                return "SERVE_TO_LEFT"
            else:
                BallCoordinate_Now = scene_info["ball"]
                ball_speed = scene_info["ball_speed"]
                PlatformX_1P = scene_info["platform_1P"][0] + 15
                PlatformY_1P = scene_info["platform_1P"][1] + 15
                PlatformX_2P = scene_info["platform_2P"][0] + 15
                PlatformY_2P = scene_info["platform_2P"][1] + 15             


                input = []
                inp_temp = np.array([PlatformX_1P, PlatformY_1P, BallCoordinate_Now[0], BallCoordinate_Now[1], ball_speed[0], ball_speed[1]])

                input = inp_temp[np.newaxis, :]
                   
                move = model.predict(input)
                print("input>>> ", move)
                if move < 0:
                    return "MOVE_LEFT"
                elif move > 0:
                    return "MOVE_RIGHT"
                else:
                    return "None"
    def reset(self):
        """
        Reset the status
        """
        self.ServePosition = random.randrange(20,180, 5)
        self.ball_served = False