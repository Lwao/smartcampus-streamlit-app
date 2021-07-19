from imports import *

def generate_pin_points(vector, conditions):
  pin_points = []
  for i in range(len(conditions)):
    pin_points.append(np.where(conditions[i](vector))[-1][-1])
  return pin_points

  
class RangedRegression():
  def __init__(self, x, y, degree=1, pin_points=[]):
    # x and y must have the same size
    # if len(pin_points)==0 limits are 0:len(x)
    # len(g) = len(s)+1
    # all pin_points<n

    self.n = min(len(x), len(y))
    self.x = np.array(x, dtype=np.float64)[:self.n]
    self.y = np.array(y, dtype=np.float64)[:self.n]
    self.degree = degree#np.array(degree, dtype=np.int32)
    self.pin_points = pin_points# np.array(pin_points, dtype=np.int32) 

    self.nDivs = len(self.pin_points)+1

    if(len(pin_points)==0): self.pin_points = [self.n]

    self.modelList = []
    self.c = []
    self.r = np.zeros(self.nDivs, dtype=np.float64)
    for i in range(self.nDivs): self.c.append(np.zeros(self.degree[i]+1, dtype=np.float64))

  def extract_section(self, nDiv): 
    if(nDiv==1): # if it is the first division
      x = self.x[:self.pin_points[0]+1].reshape(-1,1)
      y = self.y[:self.pin_points[0]+1].reshape(-1,1)
    elif(nDiv==self.nDivs): # if it is the last division
      x = self.x[self.pin_points[-1]+1:].reshape(-1,1)
      y = self.y[self.pin_points[-1]+1:].reshape(-1,1)
    else:
      x = self.x[self.pin_points[nDiv-2]+1:self.pin_points[nDiv-1]+1].reshape(-1,1)
      y = self.y[self.pin_points[nDiv-2]+1:self.pin_points[nDiv-1]+1].reshape(-1,1)
    return x, y

  def run_regression(self):
    for i in range(self.nDivs):
      nDiv = i+1
      x_ext, y_ext = self.extract_section(nDiv)
      x_feat = PolynomialFeatures(degree=self.degree[i], include_bias=True).fit_transform(x_ext)
      model = LinearRegression(fit_intercept=False).fit(x_feat, y_ext)
      self.r[i], self.c[i] = model.score(x_feat, y_ext), model.coef_
      self.modelList.append(model)

  def get_score(self): return self.r
  def get_coefficients(self): return self.c
  def ranged_prediction(self):
    if(len(self.modelList)==0): self.run_regression() # if regression was not already executed
    y_ori = np.array([], dtype=np.float64).reshape(-1,1) # original data that matches the real value
    y_pred = np.array([], dtype=np.float64).reshape(-1,1) # predicted data
    for i in range(self.nDivs):
      nDiv = i+1
      x, y = self.extract_section(nDiv)
      x_ = PolynomialFeatures(degree=self.degree[i], include_bias=True).fit_transform(x)
      y_ = self.modelList[i].predict(x_)
      y_ori = np.concatenate((y_ori, y))
      y_pred = np.concatenate((y_pred, y_))
    return y_pred, y_ori