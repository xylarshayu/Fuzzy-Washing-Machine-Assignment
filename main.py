# Fuzzy variable
class FuzzyVar:
  def __init__(self, memberships = ('small', 'medium', 'large'), range = (0, 100), isInput = True):
    self.memberships = memberships
    self.range = range
    self.isInput = isInput
    self.mfs = self.generate_mfs()

  # Generate a, b, c of each member
  def generate_mfs(self):
    num_mem = len(self.memberships)
    step = (self.range[1] - self.range[0]) / (num_mem - 1)
    mfs = {}
    for i, mem in enumerate(self.memberships):
      a = self.range[0] + step*(i-1)
      b = self.range[0] + step*(i)
      c = self.range[0] + step*(i + 1)
      mfs[mem] = (a, b, c)
    return mfs
  
  # Triangle membership function
  def compute_membership(self, mem, value):
    a, b, c = self.mfs[mem]
    if (value < self.range[0]): return (int(a < self.range[0])) # If value < range, membership is 0 except for first member
    if (value > self.range[1]): return (int(c > self.range[1])) # If value > range, membership is 0 except for last member
    return max(0, min((value - a) / (b - a), (c - value) / (c - b)))
  
  

# Input variables
dirtiness = FuzzyVar()
typeof_dirt = FuzzyVar(memberships=('not greasy', 'medium', 'greasy'))
typeof_fabric = FuzzyVar(memberships=('silk', 'woolen', 'cotton'))
cloth_volume = FuzzyVar()

# Output variables
washing_time = FuzzyVar(memberships=('very short', 'short', 'medium', 'long', 'very long'), isInput=False)
washing_speed = FuzzyVar(memberships=('very slow', 'slow', 'medium', 'fast', 'very fast'), range=(0, 1200), isInput=False)
water_intake = FuzzyVar(memberships=('little', 'normal', 'a lot'), isInput=False)
water_temperature = FuzzyVar(memberships=('low', 'normal', 'high'), range=(0, 80), isInput=False)



