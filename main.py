from cv2 import VideoWriter, VideoWriter_fourcc, flip # Video Writing
from PIL import Image, ImageDraw                      # Image creation
from random import randint                            # Random numbers
from numpy import array                               # Pillow to cv2
import math as m                                      # Maths

# Video Object
class Video:
  def __init__(self, width, height, fps, fn = 'out'):
    self.video = VideoWriter(f'./{fn}.mp4', VideoWriter_fourcc(*'FMP4'), float(fps), (width, height))
    self.width, self.height = width, height

  def __del__(self):
    self.video.release()

  def write(self, img):
    self.video.write(flip(img, 0))

# Object object
class Obj:
  def __init__(self, x, y, m, xv, yv):
    self.x, self.y = x, y     # Position
    self.m = m                # Mass
    self.xv, self.yv = xv, yv # Velocity

  # Update - built in for simplicity
  def upd(self):
    self.x += self.xv
    self.y += self.yv

# World Object
class World:
  def __init__(self):
    self.objs = [] # Objects

  # Add an object - velocity optionally specified
  def add(self, x, y, m, xv=0, yv=0):
    self.objs.append(Obj(x, y, m, xv, yv))

  # Draw the image
  def draw(self, width, height):
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img) # Editable map
    for o in self.objs:
      x, y = round(o.x)+(width/2), round(o.y)+(height/2)
      if (0<=x<width) and (0<=y<height):
        r = m.sqrt(o.m)
        draw.ellipse((x-r,y-r,x+r,y+r), fill=(0,0,0,0))
    return img

  # Update every object
  def upd(self):
    for ac,a in enumerate(self.objs):
      for bc,b in enumerate(self.objs):
        if bc>ac: # Used to avoid double updates
          f = (a.m*b.m)/((abs(a.x-b.x)**2)+(abs(a.y-b.y)**2)) # Overall force
          xs = a.x-b.x  # X scale
          ys = a.y-b.y  # Y scale
          ts = abs(xs)+abs(ys) # Total Scale
          xs /= ts # Refactor X into a multiplier
          ys /= ts # Refactor Y into a multiplier
          # UPDATE
          a.xv -= (f*xs)/a.m
          a.yv -= (f*ys)/a.m
          b.xv += (f*xs)/b.m
          b.yv += (f*ys)/b.m
    for o in self.objs:
      o.upd()

def main():
  w = World()
  v = Video(1920, 1080, 60)
  for i in range(100):
    w.add(randint(-500,500),randint(-500,500),randint(10,100))

  try:
    for i in range(900):
      w.upd()
      v.write(array(w.draw(v.width, v.height)))
      print(i)
  except KeyboardInterrupt:
    pass
  except:
    raise
  finally:
    del v

if __name__ == '__main__':
  main()
