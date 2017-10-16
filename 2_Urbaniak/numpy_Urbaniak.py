import numpy as np
import matplotlib.pyplot as plt

basicMatrix = np.array([[ 1, 3, 1, 2],
[ 1, 2, 5, 8],
[ 3, 1, 2, 9],
[ 5, 4, 2, 1]])

cuttedMatrix = basicMatrix[1:3,:3]

transponedMatrix = np.array([[ 2, 3, 1],
[ 5, 1, 3]
]).T

dotMatrix = cuttedMatrix.dot(transponedMatrix)

x = [np.linspace(-np.pi,np.pi,n.pi), np.linspace(-np.pi,np.pi,np.pi/10), np.linspace(-np.pi,np.pi,np.pi/100)]  # STEPS
v = [np.sin(x)] # albo bedzie v = [np.sin(i) for i in range(len(x))] 

for i, x_i, y_i in range(len(x)),x,v:
  fig = plt.figure(figsize=(3,3))
  fig.set_size_inches(6.7,6.5)
  sinPlot = plt.subplot(3,1,1+i)
  sinPlot.plot(x_i,v_i, label='y=sin(x)')
  sinPlot.set_xlim(-np.pi,np.pi)
  sinPlot.set_xlabel('x')
  sinPlot.set_ylabel('y')
  sinPlot.grid(True)
  sinPlot.tick_params('both',direction = 'in')
  sinPlot.grid(color='#D3D3D3', linestyle='dotted', linewidth=1)
  sinPlot.legend()
  sinPlot.set_title('y=sin(x), −π<=x<=π')
plt.savefig('sinusPlot_Urbaniak.pdf')
plt.close()

