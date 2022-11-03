from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, AntialiasAttrib, Texture, PerspectiveLens
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from math import pi, sin, cos
from itertools import product
from time import sleep
import sys

FIGURES = {"cube", "pyramid", "sphere"}
COLORS = {"red", "blue", "green"}
START_POS = (0,0,-1)
DIRS = {"top":(0,0,2), "left":(0,2,0), "right":(0,-2,0), "front":(2,0,0), "back":(-2,0,0)}
REFS = {i for i in range(2)}

class Figures(ShowBase):
    def __init__(self):

        ShowBase.__init__(self, windowType='offscreen')
        self.id = 0
        self.setupLights()  
        self.setupCamera()
        
        figure1 = set(product(FIGURES,COLORS))
        figure2 = set(product(figure1,DIRS.keys()))
        figure3 = set(product(figure2,REFS))

        self.createFigure("cube.glb", (0,0,-2), 'white', scale=(3,3, .001))
        for d1 in figure1:
            f1 = self.createFigure(f"{d1[0]}.glb", START_POS, d1[1])
            s1 = f"a {d1[1]} {d1[0]}"
            self.renderScene(s1)
            for d2 in figure2:
                if d2 and (p2 := self.getPos(d2[1], 0, [START_POS])):
                    f2 = self.createFigure(f"{d2[0][0]}.glb", self.fuzz(p2, d2[1]), d2[0][1])
                    s2 = s1 + f" with a {d2[0][1]} {d2[0][0]} on the {d2[1]}"
                    self.renderScene(s2)
                    for d3 in figure3:
                        if d3 and (p3 := self.getPos(d3[0][1], d3[1], [START_POS, p2])):
                            s3 = s2 + (" with" if d3[1] else " and") + f" a {d3[0][0][1]} {d3[0][0][0]} on the {d3[0][1]}"
                            f3 = self.createFigure(f"{d3[0][0][0]}.glb", self.fuzz(p3, d3[0][1]), d3[0][0][1])
                            self.renderScene(s3)
                            f3.removeNode()
                    f2.removeNode()
            f1.removeNode()
        
        sys.exit()
    
    def fuzz(self, pos, direction):
        n_pos = [pos[i] for i in range(3)]
        for i in range(3):
            if DIRS[direction][i]:
                n_pos[i] = (abs(pos[i]) + .01) * (-1 if pos[i]<0 else 1)
        return tuple(n_pos)

    def getPos(self, direction, ref, elements):
        target = tuple([elements[ref][i] + DIRS[direction][i] for i in range(3)])
        if target in elements or \
           abs(target[0]) > 2 or\
           abs(target[1]) > 2 or \
           (target[2]>START_POS[2] and (target[0],target[1],target[2]-DIRS["top"][2]) not in elements):
                return None
        return target

    def renderScene(self, s):
        print(f"{self.id} : " + s)
        base.graphicsEngine.renderFrame()
        base.screenshot(namePrefix=f"screenshots/{self.id}.jpg", defaultFilename=False)
        with open(f'prompts/{self.id}.txt','w') as f:
            f.write(s)
        self.id+=1

    def createFigure(self,model, pos, color, scale=(1,1,1)):
        tex = loader.loadTexture(f'textures/{color}.png')
        #tex = base.win.getScreenshot()
        fig = loader.loadModel(f"models/{model}")
        fig.setScale(scale)
        fig.setTexture(tex,1)
        fig.reparentTo(render)
        fig.setPos(pos)
        return fig

    def setupCamera(self):
        render.setAntialias(AntialiasAttrib.M_better)
        self.disableMouse()  
        camera.setPos(13, 11, 12)
        camera.lookAt(0, 0, 0)
        
    def setupLights(self):
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor((0.6, 0.6, 0.6, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)
        #render.setShaderAuto()

p = Figures()
p.run()
