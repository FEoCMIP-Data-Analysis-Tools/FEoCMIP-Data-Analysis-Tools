#Created by Keighan Gemmell (keighan@chem.ubc.ca)
#This code will do a weighted grid box correction as a function of latitude and longitude
#You will need to import your data and extract the lat-lon grid to do this correction 
#The final variable, A_weighted_global can be used to correct for grid box size 

lat= #define latitude
lon= #define latitude

#-------------------------Size of Each Gridbox---------------------------------#
r=6371000 #radius of Earth in m
A=np.zeros(.shape) #put your grid in here
for i in range(0,len(lat)-1):
  for j in range(0,len(lon)-1):
    A[i,j]=np.pi/180.*r**2*np.abs(np.sin(lat[i]*np.pi/180.)-np.sin(lat[i+1]*np.pi/180.))*np.abs(lon[j]-lon[j+1])
A[-1,:]=A[0,:]
A[:,-1]=A[:,0]

A_weighted_global=A/np.sum(A) #gives gridbox weighting globally
