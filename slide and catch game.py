#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 00:37:12 2024

@author: ieiuser
"""

import pygame, simpleGE, random


class Ball(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("soccerBall.png")
        self.setSize(25, 25)
        self.reset()
        self.ballSound = simpleGE.Sound("sound.mp3")
        
        
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(2, 5)

    def process(self):
        self.y += self.dy
        self.checkBounds()

    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Bike(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("bike.png")
        self.setSize(60, 60)
        self.position = (300, 380)
        self.moveSpeed = 6
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "score: 0"
        self.center = (120, 30)
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.centre = (500, 100)        
        

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("bg.png")
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.score = 0
        
        self.sndBall = simpleGE.Sound("sound.mp3")
        
        self.bike = Bike(self)
        self.ball = []
        for i in range(3):
            self.ball.append(Ball(self))
            
        self.lblScore = LblScore()
        self.lblTime = LblTime()
        
        self.sprites = [self.bike,
                        self.ball,
                        self.lblScore,
                        self.lblTime]

    def process(self):
        for ball in self.ball:
            if ball.collidesWith(self.bike):
                ball.ballSound.play()
                ball.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
            self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
            if self.timer.getTimeLeft() < 0:
                print(f"Final Score: {self.score}")
                self.stop()
                
class Instruction(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("bg.png")
        
        self.response = "quit"
        
        self.instruction = simpleGE.MultiLabel()
        self.instruction.textLines = [
        "You are bike the rider.",
        "Move with the left and right arrow keys",
        "and catch as much ball as you can",
        "in only ten seconds",
        "",
        "Good Luck!"]
        
        self.instruction.center = (320, 240)
        self.instruction.size = (500, 250)
        
        self.prevScore = score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.center = (320, 50)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "play (up)"
        self.btnPlay.centre = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quite (down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instruction,
                        self.lblScore,
                        self.btnQuit,
                        self.btnPlay]
        
    def process(self):
        #buttons
        if self.btnQuit.clicked:
            self.response = "quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "play"
            self.stop()

        #arrow keys
        if self.isKeyPressed(pygame.K_UP):
            self.response = "play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "quit"
            self.stop()
            
                
def main():
     
     keepGoing = True
     score = 0
     while keepGoing:
         
         instruction = Instruction(score)
         instruction.start()
         
         if instruction.response == "play":
             game = Game()
             game.start()
             score = game.score
         else:
            keepGoing = False
            
if __name__ == "__main__":
    main()
         


