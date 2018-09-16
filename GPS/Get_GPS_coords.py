from PIL import Image

#ilepath = "/Users/artyomarchiyan/Desktop/binary_test_image_gps.jpg"

#im_obj = Image.open(filepath)
#tot_width_px, tot_height_px = im_obj.size

tot_width_px = 574
tot_height_px = 383

center_width_px = tot_width_px/2
center_height_px = tot_height_px/2

#Given this resolutio: width = 574, height = 383, center at: (287, 191.5)
#GPS coords pinged at center
#pixel location of obj1 = (65.4932, 264.2952)

feet_per_km = 3280.84
km_per_degree = (10000/90) #approximate 


#split at the desired separator.
def split(gps_center, separator):
    prev_index = gps_center.find(separator)
    degrees = int(gps_center[0:prev_index])
    current_index = gps_center.find(separator, prev_index + 1)
    minutes = int(gps_center[prev_index + 1: current_index])
    seconds = int(gps_center[current_index + 1:])
    
        
    return degrees, minutes, seconds

def get_GPS_coords(height_px, width_px, gps_center_lat, gps_center_lon, tot_height_ft, tot_width_ft):
    
    #height = latitude 
    #width = longitude
    
    #feet per pixel based on total based on total width of captured area
    #doesn't matter width or height since pixel is square
    feet_per_pixel = tot_height_ft/tot_height_px
    
    degrees_lat, minutes_lat, seconds_lat = split(gps_center_lat, ".")
    degrees_lon, minutes_lon, seconds_lon = split(gps_center_lon, ".")
    
    
    if degrees_lat < 0: #center is south 
        degrees_lat = degrees_lat - ((minutes_lat + (seconds_lat/60))/60)
        
    elif degrees_lat > 0: #center is north 
        degrees_lat = degrees_lat + ((minutes_lat + (seconds_lat/60))/60)
        
    
    if degrees_lon < 0: #center is west
        degrees_lon = degrees_lon - ((minutes_lon + (seconds_lon/60))/60)
    
    elif degrees_lon > 0: #center is east
        degrees_lon = degrees_lon + ((minutes_lon + (seconds_lon/60))/60)
    
    degrees_lat_km = degrees_lat * km_per_degree
    degrees_lon_km = degrees_lon * km_per_degree
    
    degrees_lat_ft = degrees_lat_km * feet_per_km
    degrees_lon_ft = degrees_lon_km * feet_per_km
    
    
    if (height_px > center_height_px) and (degrees_lat < 0): #south and south
        distance_height_px = height_px - center_height_px 
        eq_distance_ft = degrees_lat_ft - (distance_height_px * feet_per_pixel)
    
    elif (height_px < center_height_px) and (degrees_lat < 0): #north and south
        distance_height_px = center_height_px - height_px
        eq_distance_ft = degrees_lat_ft + (distance_height_px * feet_per_pixel)
        
    elif (height_px > center_height_px) and (degrees_lat > 0): #south and north
        distance_height_px = height_px - center_height_px
        eq_distance_ft = degrees_lat_ft - (distance_height_px * feet_per_pixel)
        
    elif (height_px < center_height_px) and (degrees_lat > 0): #north and north
        distance_height_px = center_height_px - height_px
        eq_distance_ft = degrees_lat_ft + (distance_height_px * feet_per_pixel)
        
    
    if (width_px < center_width_px) and (degrees_lon < 0): #west and west
        distance_width_px = center_width_px - width_px
        pm_distance_ft = degrees_lon_ft - (distance_width_px * feet_per_pixel)
        
    elif (width_px > center_width_px) and (degrees_lon < 0): #east and west
        distance_width_px = width_px - center_width_px
        pm_distance_ft = degrees_lon_ft + (distance_width_px * feet_per_pixel)
        
    elif (width_px < center_width_px) and (degrees_lon > 0): #west and east
        distance_width_px = center_width_px - width_px
        pm_distance_ft = degrees_lon_ft - (distance_width_px * feet_per_pixel)
        
    elif (width_px > center_width_px) and (degrees_lon > 0): #east and east
       distance_width_px = width_px - center_width_px
       pm_distance_ft = degrees_lon_ft + (distance_width_px * feet_per_pixel)
       
    eq_distance_km = eq_distance_ft * (1/feet_per_km)
    pm_distance_km = pm_distance_ft * (1/feet_per_km)
    
    gps_lat_coord = eq_distance_km * (1/km_per_degree)
    gps_lon_coord = pm_distance_km * (1/km_per_degree)
    
    return gps_lat_coord, gps_lon_coord

gps_lat_coord, gps_lon_coord = get_GPS_coords(65.4932, 264.2952, "41.68.48", "-85.33.30", 300, 200.174)

print(gps_lat_coord, gps_lon_coord)
