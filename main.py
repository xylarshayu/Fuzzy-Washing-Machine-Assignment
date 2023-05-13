class FuzzyVar:
  def __init__(self, memberships = ('small', 'medium', 'large'), range = (0, 100), isInput = True):
    self.memberships = memberships
    self.range = range
    self.isInput = isInput
    self.mfs = self.generate_mfs()

  def generate_mfs(self):
    num_mem = len(self.memberships)
    mfs = {}
    
    if num_mem == 3:
      mfs[self.memberships[0]] = (self.range[0], self.range[0], self.range[0] + self.range[1] / 3)
      mfs[self.memberships[1]] = (self.range[0], self.range[0] + self.range[1] / 3, 2 * self.range[1] / 3)
      mfs[self.memberships[2]] = (self.range[0] + self.range[1] / 3, 2 * self.range[1] / 3, self.range[1])
    elif num_mem == 5:
      mfs[self.memberships[0]] = (self.range[0], self.range[0] + self.range[1] / 10, self.range[1] * 3 / 10)
      mfs[self.memberships[1]] = (self.range[0] + self.range[1] / 10, self.range[1] * 3 / 10, self.range[1] / 2)
      mfs[self.memberships[2]] = (self.range[1] * 3 / 10, self.range[1] / 2, self.range[1] * 7 / 10)
      mfs[self.memberships[3]] = (self.range[1] / 2, self.range[1] * 7 / 10, self.range[1] * 9 / 10)
      mfs[self.memberships[4]] = (self.range[1] * 7 / 10, self.range[1] * 9 / 10, self.range[1])
    else:
      raise ValueError("This function supports either 3 or 5 memberships only")

    return mfs

  def compute_membership(self, mem, value):
    a, b, c = self.mfs[mem]
    if (value < a): return 0
    if (value > c): return 0
    if (a <= value <= b): return (value - a) / (b - a)
    if (b < value <= c): return (c - value) / (c - b)


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

  # Some assumed rules based on common sense
  washing_time_mf = {
    'short': min(dirtiness_mf['small'], typeof_dirt_mf['not greasy'], typeof_fabric_mf['silk'], cloth_volume_mf['small']),
    'very long': min(dirtiness_mf['large'], typeof_dirt_mf['greasy'], typeof_fabric_mf['cotton'], cloth_volume_mf['large']),
    'medium': min(dirtiness_mf['medium'], typeof_dirt_mf['medium'], typeof_fabric_mf['woolen'], cloth_volume_mf['medium'])
  }

  water_intake_mf = {
    'little': min(dirtiness_mf['small'], typeof_dirt_mf['not greasy'], typeof_fabric_mf['silk'], cloth_volume_mf['small']),
    'a lot': min(dirtiness_mf['large'], typeof_dirt_mf['greasy'], typeof_fabric_mf['cotton'], cloth_volume_mf['large']),
    'normal': min(dirtiness_mf['medium'], typeof_dirt_mf['medium'], typeof_fabric_mf['woolen'], cloth_volume_mf['medium'])
  }

  water_temperature_mf = {
    'low': min(dirtiness_mf['small'], typeof_dirt_mf['not greasy'], typeof_fabric_mf['silk'], cloth_volume_mf['small']),
    'high': min(dirtiness_mf['large'], typeof_dirt_mf['greasy'], typeof_fabric_mf['cotton'], cloth_volume_mf['large']),
    'normal': min(dirtiness_mf['medium'], typeof_dirt_mf['medium'], typeof_fabric_mf['woolen'], cloth_volume_mf['medium'])
  }

  # Computing defuzzified values for output variables
  washing_speed_defuzzified = defuzzify(washing_speed, washing_speed_mf)
  washing_time_defuzzified = defuzzify(washing_time, washing_time_mf)
  water_intake_defuzzified = defuzzify(water_intake, water_intake_mf)
  water_temperature_defuzzified = defuzzify(water_temperature, water_temperature_mf)

  # Return output variables
  return {
    'washing_time': washing_time_defuzzified,
    'washing_speed': washing_speed_defuzzified,
    'water_intake': water_intake_defuzzified,
    'water_temperature': water_temperature_defuzzified
  }

dirtiness_value = float(input("Enter dirtiness value (0-100): "))
typeof_dirt_value = float(input("Enter type of dirt value (0-100): "))
typeof_fabric_value = float(input("Enter type of fabric value (0-100): "))
cloth_volume_value = float(input("Enter cloth volume value (0-100): "))

print(fuzzy_washing_machine(dirtiness_value, typeof_dirt_value, typeof_fabric_value, cloth_volume_value))