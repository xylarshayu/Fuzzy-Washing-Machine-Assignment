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

# Defuzzification using Centroid Method
def defuzzify(output_var, memberships):
  num = 0
  den = 0
  for mem in memberships:
    a, b, c = output_var.mfs[mem]
    centroid = (a + b + c) / 3
    num += memberships[mem] * centroid
    den += memberships[mem]
  return num / den if den != 0 else 0

# Fuzzy Inference System
def fuzzy_washing_machine(dirtiness_value, typeof_dirt_value, typeof_fabric_value, cloth_volume_value):
  # Computing membership functions of each
  dirtiness_mf = { mem: dirtiness.compute_membership(mem, dirtiness_value) for mem in dirtiness.memberships }
  typeof_dirt_mf = { mem: typeof_dirt.compute_membership(mem, typeof_dirt_value) for mem in typeof_dirt.memberships }
  typeof_fabric_mf = { mem: typeof_fabric.compute_membership(mem, typeof_fabric_value) for mem in typeof_fabric.memberships }
  cloth_volume_mf = { mem: cloth_volume.compute_membership(mem, cloth_volume_value) for mem in cloth_volume.memberships }

  # Applying rules of inference to compute membership values for output variables via Mamdani inference
  washing_speed_mf = {
    'very slow': min(dirtiness_mf['small'], typeof_dirt_mf['not greasy'], typeof_fabric_mf['silk'], cloth_volume_mf['small']),
    'very fast': min(dirtiness_mf['large'], typeof_dirt_mf['greasy'], typeof_fabric_mf['cotton'], cloth_volume_mf['large']),
    'medium': min(dirtiness_mf['large'], typeof_dirt_mf['not greasy'], typeof_fabric_mf['woolen'], cloth_volume_mf['medium'])
  }

  print(washing_speed_mf)

  # Computing defuzzified values for output variables
  washing_speed_defuzzified = defuzzify(washing_speed, washing_speed_mf)

  # Return output variables
  return {
    'washing_time': 'NA', # Rules unavailable
    'washing_speed': washing_speed_defuzzified,
    'water_intake': 'NA', # Rules unavailable
    'water_temperature': 'NA' # Rules unavailable
  }

dirtiness_value = float(input("Enter dirtiness value (0-100): "))
typeof_dirt_value = float(input("Enter type of dirt value (0-100): "))
typeof_fabric_value = float(input("Enter type of fabric value (0-100): "))
cloth_volume_value = float(input("Enter cloth volume value (0-100): "))

print(fuzzy_washing_machine(dirtiness_value, typeof_dirt_value, typeof_fabric_value, cloth_volume_value))




