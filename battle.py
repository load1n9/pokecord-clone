import pokebase as pb
import random

class Battle:
    def __init__(self, a,b):
      self.data = {
          "pokemon": "test",
          "msg": []
      }
      self.setStats(a,b)
      self.setMoves()

    def setStats(self,a,b):
      self.p1 = {
        "name": pb.pokemon(a).name,
        "health": 1000
      }
      self.p2 = {
       "name": pb.pokemon(b).name,
       "health": 1000
      }

    def setMoves(self):
      p1int = random.randint(0,len(pb.pokemon(self.p1["name"]).moves)-1)
      p2int = random.randint(0,len(pb.pokemon(self.p2["name"]).moves)-1)
      self.p1["move"] = pb.pokemon(self.p1["name"]).moves[p1int].move.name
      self.p2["move"] = pb.pokemon(self.p2["name"]).moves[p2int].move.name
      self.attack()
    def attack(self):
      if int(self.p1["health"]) > 0 and int(self.p2["health"]) > 0:
        try:  
          self.data["msg"].append(self.p1["name"]+" uses "+self.p1["move"])
          self.p1["health"] -= int(pb.move(str(self.p2["move"])).power)
          self.data["msg"].append(self.p2["name"]+" uses "+self.p2["move"])
          self.p2["health"] -= int(pb.move(str(self.p1["move"])).power)
          self.data["msg"].append(self.p1["name"]+": "+str(self.p1["health"]))
          self.data["msg"].append(self.p2["name"]+": "+str(self.p2["health"]))
          self.setMoves()
        except:
          self.setMoves()
      elif self.p1["health"] <= 0:
        self.data["pokemon"] = pb.pokemon(self.p2["name"])
      elif self.p2["health"] <= 0:
        self.data["pokemon"] = pb.pokemon(self.p1["name"])
