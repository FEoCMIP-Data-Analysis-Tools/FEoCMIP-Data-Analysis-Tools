#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by anjakatzenberger (anja.katzenberger@pik-potsdam.de)
"""

### This code provides changes in wind speed and wind direction for a subset of CMIP6 models
### The first figure (a panel of 2x3 wind fields) is written for 6 CMIP6 models
### The second figure gives a multi model mean of the models given
### The input data is preprocessed using CDOs (selected time period, selected altitude of winds, as well as mean over time for specific months)
### Adapt the preprocessing as adequate for your research question


import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import os


# CMIP6 future wind data for different models (ideally 6)
udir_future = "/Users/UserX/ua_future_output"
vdir_future = "/Users/UserX/va_future_output"

#CMIP historiy wind data for different models (ideally 6)
udir = "/Users/UserX/ua_output"
vdir= "/Users/UserX/va_output"

# Where to save the output
dir_save = "/Users/UserX/figures"


#%%-------------
### CMIP WIND
#----------------

file_list_u_future = os.listdir(udir_future)
file_list_v_future = os.listdir(vdir_future)
file_list_u = os.listdir(udir)
file_list_v  = os.listdir(vdir)


file_list_u.sort()
file_list_v.sort()
file_list_u_future.sort()
file_list_v_future.sort()

### Creating panel for 6 CMIP models

# Plotting
fig, axs = plt.subplots(nrows=2, ncols=3, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(14, 7))
fig.subplots_adjust(hspace=0.04)  # Adjust the vertical spacing between subplots
fig.subplots_adjust(bottom=0.05)
fig.subplots_adjust(wspace=0.1)

axs = axs.flatten()  # Flatten the array of subplots

for i in range(2):
    for j in range(3):
        u_file_path_future = udir_future + "/" + file_list_u_future[i * 3 + j]
        v_file_path_future = vdir_future + "/" + file_list_v_future[i * 3 + j]
        u_file_path = udir + "/" + file_list_u[i * 3 + j]
        v_file_path = vdir + "/" + file_list_v[i * 3 + j]

        # Load u and v data from NetCDF
        u_data_future = xr.open_dataset(u_file_path_future)
        v_data_future = xr.open_dataset(v_file_path_future)
        u_data = xr.open_dataset(u_file_path)
        v_data = xr.open_dataset(v_file_path)

        # Extract u, v, lon, and lat data (wind at 850hPa)
        ua_future = u_data_future['ua'].isel(time=0, plev=0)
        va_future = v_data_future['va'].isel(time=0, plev=0)

        ua = u_data['ua'].isel(time=0, plev=0)
        va = v_data['va'].isel(time=0, plev=0)

        ua_diff = ua_future - ua
        va_diff = va_future - va

        lon = u_data['lon']
        lat = u_data['lat']

        # Calculate wind speed from u and v components
        wind_speed = np.sqrt(ua_diff**2 + va_diff**2)

        # Extract the subplot axis
        ax = axs[i * 3 + j]  # Use the flattened index

        # Set up the subplot
        ax.set_extent([60, 159, 1, 59], crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle='--')
        ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='gray')  # Set facecolor to green for land

        # Create the filled contour plot
        contourf_plot = ax.contourf(lon, lat, wind_speed.values, transform=ccrs.PlateCarree(), cmap=plt.cm.RdYlBu_r,
                                    levels=np.arange(0,4,0.5), extend='max')

        # Show every 3rd u and v vector using quiver
        stride = [4, 4, 4, 4, 4, 4]
        quiver_plot = ax.quiver(lon[::stride[i * 3 + j]], lat[::stride[i * 3 + j]], ua_diff.values[::stride[i * 3 + j], ::stride[i * 3 + j]],
                                va_diff.values[::stride[i * 3 + j], ::stride[i * 3 + j]], transform=ccrs.PlateCarree(), scale=200,
                                color='black')

        # Set x-axis and y-axis ticks
        ax.set_xticks(np.arange(60, 159, 20))  # Adjust the range and interval as needed
        ax.set_yticks(np.arange(10, 59, 10))  # Adjust the range and interval as needed

        # Set x-axis and y-axis tick labels
        ax.set_xticklabels(np.arange(60, 159, 20), fontsize=8)
        ax.set_yticklabels(np.arange(10, 59, 10), fontsize=8)

        ax.set_title(file_list_u[i * 3 + j].split("_")[2])

# Create a common colorbar for all subplots
fig.subplots_adjust(bottom=0.2)  # Adjust the bottom margin to make room for the colorbar
cbar_ax = fig.add_axes([0.31, 0.15, 0.4, 0.02])  # Adjust the position and size of the colorbar
cbar = plt.colorbar(contourf_plot, cax=cbar_ax, orientation='horizontal')
cbar.set_label('Wind Speed (m/s)')

plt.savefig(dir_save + "/filename.pdf", bbox_inches='tight')
#plt.show()






#%%
### Multi-model mean


# Create an array to store wind speed data for each subplot
wind_speed_data = []

# Create arrays to store ua_diff and va_diff data for each subplot
ua_diff_data = []
va_diff_data = []

file_list_u_future = os.listdir(udir_future)
file_list_v_future = os.listdir(vdir_future)
file_list_u = os.listdir(udir)
file_list_v = os.listdir(vdir)

file_list_u.sort()
file_list_v.sort()
file_list_u_future.sort()
file_list_v_future.sort()

# Plotting
fig, axs = plt.subplots(nrows=2, ncols=3, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(14, 7))
fig.subplots_adjust(hspace=0.04)
fig.subplots_adjust(bottom=0.05)
fig.subplots_adjust(wspace=0.1)

axs = axs.flatten()

for i in range(2):
    for j in range(3):
        u_file_path_future = udir_future + "/" + file_list_u_future[i * 3 + j]
        v_file_path_future = vdir_future + "/" + file_list_v_future[i * 3 + j]
        u_file_path = udir + "/" + file_list_u[i * 3 + j]
        v_file_path = vdir + "/" + file_list_v[i * 3 + j]

        # Load u and v data from NetCDF
        u_data_future = xr.open_dataset(u_file_path_future)
        v_data_future = xr.open_dataset(v_file_path_future)
        u_data = xr.open_dataset(u_file_path)
        v_data = xr.open_dataset(v_file_path)

        # Extract u, v, lon, and lat data (wind at 850hPa)
        ua_future = u_data_future['ua'].isel(time=0, plev=0)
        va_future = v_data_future['va'].isel(time=0, plev=0)

        ua = u_data['ua'].isel(time=0, plev=0)
        va = v_data['va'].isel(time=0, plev=0)

        ua_diff = ua_future - ua
        va_diff = va_future - va

        lon = u_data['lon']
        lat = u_data['lat']

        # Calculate wind speed from u and v components
        wind_speed = np.sqrt(ua_diff**2 + va_diff**2)

        # Append wind speed data to the array
        wind_speed_data.append(wind_speed)

        # Append ua_diff and va_diff data to the arrays
        ua_diff_data.append(ua_diff)
        va_diff_data.append(va_diff)

#%%

# Calculate the mean wind speed
mean_wind_speed = np.mean(wind_speed_data, axis=0)

# Calculate the mean of all ua_diff and va_diff values
mean_ua_diff = np.mean(ua_diff_data, axis=0)
mean_va_diff = np.mean(va_diff_data, axis=0)

#%%

# Create a separate plot for the mean wind speed
fig_mean, ax_mean = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(7, 5.8))

# Set up the subplot for the mean wind speed
ax_mean.set_extent([60, 159, 1, 59], crs=ccrs.PlateCarree())
ax_mean.add_feature(cfeature.COASTLINE)
ax_mean.add_feature(cfeature.BORDERS, linestyle='--')
ax_mean.add_feature(cfeature.LAND, edgecolor='black', facecolor='gray')

# Create the filled contour plot for the mean wind speed
contourf_mean = ax_mean.contourf(lon, lat, mean_wind_speed, transform=ccrs.PlateCarree(), cmap=plt.cm.RdYlBu_r,
                                levels=np.arange(0, 3, 0.25), extend='max')

# Show every 3rd u and v vector using quiver for the mean wind speed
stride_mean = 2
quiver_mean = ax_mean.quiver(lon[::stride_mean], lat[::stride_mean],
                             mean_ua_diff[::stride_mean, ::stride_mean],
                             mean_va_diff[::stride_mean, ::stride_mean],
                             transform=ccrs.PlateCarree(), scale=200, color='black')

# Set x-axis and y-axis ticks for the mean wind speed plot
ax_mean.set_xticks(np.arange(60, 159, 20))
ax_mean.set_yticks(np.arange(10, 59, 10))

# Set x-axis and y-axis tick labels for the mean wind speed plot
ax_mean.set_xticklabels(np.arange(60, 159, 20), fontsize=8)
ax_mean.set_yticklabels(np.arange(10, 59, 10), fontsize=8)


# Create a colorbar for the mean wind speed plot
fig_mean.subplots_adjust(bottom=0.2)
cbar_ax_mean = fig_mean.add_axes([0.31, 0.15, 0.4, 0.02])
cbar_mean = plt.colorbar(contourf_mean, cax=cbar_ax_mean, orientation='horizontal')
cbar_mean.set_label('Wind Speed (m/s)')

plt.savefig(dir_save + "filename_mmm.pdf", bbox_inches='tight')

