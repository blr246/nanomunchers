def printMuncherList(munchers):
  for i, muncher in enumerate(munchers):
    print muncher.to_s()

class MuncherPresenter:
  xMin = 0
  xMax = 20
  yMin = 0
  yMax = 10
  class MuncherInvalidException(Exception):
    pass

  def __init__(self, dropTime, x, y, program):
    if dropTime < 0:
      raise MuncherInvalidException("You must drop munchers after the program begins!")
    self.dropTime = dropTime

    if self.xMin > x:
      raise MuncherInvalidException("You cannot place a muncher at an x value less than " + str(xMin))
    if self.xMax <= x:
      raise MuncherInvalidException("You cannot place a muncher at an x value greater than or equal to " + str(xMax))
    self.x = x
    
    if self.yMin > y:
      raise MuncherInvalidException("You cannot place a muncher at a y value less than " + str(yMin))
    if self.yMax <= y:
      raise MuncherInvalidException("You cannot place a muncher at a y value greater than or equal to " + str(yMax))
    self.y = y
    
    if program.count("U") > 1:
      raise MuncherInvalidException("Your program: " + program + " has more than one U.")
    if program.count("U") < 1:
      raise MuncherInvalidException("Your program: " + program + " has no U.")

    if program.count("L") > 1:
      raise MuncherInvalidException("Your program: " + program + " has more than one L.")
    if program.count("L") < 1:
      raise MuncherInvalidException("Your program: " + program + " has no L.")

    if program.count("D") > 1:
      raise MuncherInvalidException("Your program: " + program + " has more than one D.")
    if program.count("D") < 1:
      raise MuncherInvalidException("Your program: " + program + " has no D.")

    if program.count("R") > 1:
      raise MuncherInvalidException("Your program: " + program + " has more than one R.")
    if program.count("R") < 1:
      raise MuncherInvalidException("Your program: " + program + " has no R.")
    
    self.program = program

  def to_s(self):
    return str(self.dropTime) + " " + str(self.x) + " " + str(self.y) + " " + self.program

#ml = []
#ml.append(MuncherPresenter(0,1,5,"LURD"))
#printMuncherList(ml)
