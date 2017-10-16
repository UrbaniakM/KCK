import numpy as np
import matplotlib.pyplot as plt

def draw(xi, vi, n):
  sinPlot = plt.subplot(3, 1, n+1)
  sinPlot.plot(xi, vi, label='y=sin(x)')
  sinPlot.set_xlim(-np.pi, np.pi)
  sinPlot.set_xlabel('x')
  sinPlot.set_ylabel('y')
  sinPlot.grid(True)
  sinPlot.tick_params('both', direction='in')
  sinPlot.grid(color='#D3D3D3', linestyle='dotted', linewidth=1)
  sinPlot.legend()
  sinPlot.set_title('y=sin(x), −π<=x<=π')

basicMatrix = np.array([[ 1, 3, 1, 2],
[ 1, 2, 5, 8],
[ 3, 1, 2, 9],
[ 5, 4, 2, 1]])

cuttedMatrix = basicMatrix[1:3,:3]

transponedMatrix = np.array([[ 2, 3, 1],
[ 5, 1, 3]
]).T

dotMatrix = cuttedMatrix.dot(transponedMatrix)


x = [np.linspace(-np.pi,np.pi,np.pi), np.linspace(-np.pi,np.pi,10), np.linspace(-np.pi,np.pi,100)]  # STEPS
v = [np.sin(i) for i in x]
label = ['krok pi', 'krok 10', 'krok 100']

for i in range(len(x)):
  draw(x[i],v[i],i)
plt.savefig('sinusPlot_Urbaniak.pdf')
plt.close()

