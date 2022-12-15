import sys
import numpy as np
import math


def parse_input (content):
    """
    Parses the passed-in file and extracts the information.
    Then stores the information in a dictionary.
    """
    file = open(content)
    # create a dictionary to store all the input contents
    information = {}
    # create a list to store the information of all the spheres.
    spheres = []
    # create a list to store the information of all the light sourses.
    lights = []
    lines = file.readlines()
    for line in lines:
        info_list=line.split()
        if(info_list)!=[]:      # if the line is not empty
            key = info_list[0]
            if key == 'LEFT' or key == 'RIGHT' or key == 'BOTTOM' or key =='TOP' or key =='NEAR':
                information[key] = float(info_list[1])
            if key == 'AMBIENT' or key == 'BACK':
                value_list = []
                for item in info_list[1:]:
                    item = float(item)
                    value_list.append(item)
                information[key] = value_list
            if key == 'RES':
                value_list = []
                for item in info_list[1:]:
                    item = int(item)
                    value_list.append(item)
                information[key] = value_list

            if key == 'SPHERE':
                sphere_info = []
                sphere_info.append(info_list[1])
                sphere_info.append(float(info_list[2]))
                sphere_info.append(float(info_list[3]))
                sphere_info.append(float(info_list[4]))
                sphere_info.append(float(info_list[5]))
                sphere_info.append(float(info_list[6]))
                sphere_info.append(float(info_list[7]))
                sphere_info.append(float(info_list[8]))
                sphere_info.append(float(info_list[9]))
                sphere_info.append(float(info_list[10]))
                sphere_info.append(float(info_list[11]))
                sphere_info.append(float(info_list[12]))
                sphere_info.append(float(info_list[13]))
                sphere_info.append(float(info_list[14]))
                sphere_info.append(int(info_list[15]))

                spheres.append(sphere_info)

            if key == 'LIGHT':
                light_info = []
                light_info.append(info_list[1])
                light_info.append(float(info_list[2]))
                light_info.append(float(info_list[3]))
                light_info.append(float(info_list[4]))
                light_info.append(float(info_list[5]))
                light_info.append(float(info_list[6]))
                light_info.append(float(info_list[7]))

                lights.append(light_info)
            
            if key == 'OUTPUT':
                information[key] = info_list[1]
                
    information['SPHERE'] = spheres
    information['LIGHT'] = lights
    file.close()

    return information


def save_imageP3(Width, Height,fname,pixels):
    """
    Generate a ppm text file in P3 format.
    """
    maxVal=255
    print("Saving image " + fname + ": " + str(Width) + " x " + str(Height) + "\n")
    
    file = open(fname, "w")

    file.write("P3\n")
    file.write(str(Width) + " " + str(Height) + "\n")
    file.write(str(maxVal) + "\n")
    
    k = 0
    curRow = 0
    while curRow < Height:
        curCol = 0
        while curCol < Width:
            file.write(" " + str(pixels[k]) + " " + str(pixels[k+1]) + " " + str(pixels[k+2]) + "  ")
            k = k+3
            curCol = curCol +1
        file.write("\n")
        curRow = curRow +1

    file.close()


def intersect(origin, ray_dir):
    """
    Check if the ray intersects the sphere. If so, calculate the value of t (the distance). 
    """
    a = (np.linalg.norm(ray_dir))**2
    b = np.dot(origin, ray_dir)
    c = ((np.linalg.norm(origin))**2)-1

    deter = b**2-a*c
    if deter > 0:        # Otherwise the ray does not intersect any spheres
        t1 = -b/a + math.sqrt(b**2-a*c)/a
        t2 = -b/a - math.sqrt(b**2-a*c)/a
        if t1 > 0 and t2 > 0:
            return min(t1, t2)      # Only want the first intersection.
    else:
        return None

def nearest_intersection(spheres,origin,ray_dir):
    """
    Finds the first intersected sphere in the untransformed space and the distance from 
    the origin to the sphere. 
    Also, keep track of the normal in the untransformed space.
    """
    # Create a list to store all the values of t (the distance).
    all_intersect = []
    # Create a list to store all the values of the normal in the untransformed space.
    normals = []
    for sphere in spheres:
        modelMatrix = np.array([[sphere[4], 0, 0, sphere[1]],
                               [0, sphere[5], 0, sphere[2]],
                               [0, 0, sphere[6], sphere[3]],
                                [0,0,0,1]])
        inv_model = np.linalg.inv(modelMatrix)
        inv_transpose = inv_model.transpose()
        
        homo_point = np.array([1])
        # convert the vertex into the homogeneous representation.
        homo_origin = np.append(origin, homo_point)
        inv_origin = np.matmul(inv_model, homo_origin)
        # convert the vertex back from the homogeneous representation.
        new_origin = np.delete(inv_origin, 3)

        homo_vertex = np.array([0])
        # convert the vertex into the homogeneous representation.
        homo_ray_dir = np.append(ray_dir, homo_vertex)
        inv_ray_dir = np.matmul(inv_model, homo_ray_dir)
        # convert the vertex back from the homogeneous representation.
        new_ray_dir = np.delete(inv_ray_dir, 3)
        
        t_h = intersect(new_origin, new_ray_dir)
        if(t_h == None):
            all_intersect.append(np.inf)
            normals.append(np.inf)
        else:
            all_intersect.append(t_h)

            # gets the normal in the untransformed space
            canonical_intersect_pixel = np.add(new_origin, new_ray_dir*t_h)
            canonical_normal = np.append(canonical_intersect_pixel, homo_vertex)
            untrans_normal = np.matmul(inv_transpose, canonical_normal)
            normal = np.delete(untrans_normal, 3)
            new_normal = normal / np.linalg.norm(normal)      # normalize
            normals.append(new_normal)

    nearest_t = min(all_intersect)
    sphere_index = all_intersect.index(nearest_t)
    s_normal = normals[sphere_index]

    return sphere_index, nearest_t, s_normal
    

def main():
    information = parse_input(sys.argv[1])
    
    eye = np.array([0, 0, 0])

    left = information['LEFT']
    top = information['TOP']
    right = information['RIGHT']
    bottom = information['BOTTOM']

    nRows = information['RES'][0]
    nCols = information['RES'][1]

    height = (top-bottom)/2
    width = (right-left)/2

    # initialize the list to store the rgb of each pixel
    pixels = [None] * 3 *nCols*nRows
    k = 0
    for i in range(nRows-1,0,-1):       # for each row starts from top
        for j in range(nCols):          # for each column starts from left
            ray_dir = np.array([width*(2*j/nCols-1), height*(2*i/nRows-1),-information['NEAR']])
            sphere_index, nearest_t, s_normal = nearest_intersection(information['SPHERE'], eye, ray_dir)
            depth = 0       # Initialize the depth of the recursion
            if(nearest_t == np.inf):
                #   if the ray hit nothing return the colour of the background
                color = np.array([information['BACK'][0],information['BACK'][1],information['BACK'][2]])
            else:
                color = raytrace(nearest_t, information, sphere_index, eye, ray_dir,depth,s_normal)
            
            # for each rgb component of the returned colour, 
            # if the value go above 1, clamp the value to 1.
            if color[0]>1:
                color[0]=1
            if color[1]>1:
                color[1]=1
            if color[1]>1:
                color[1]=1

            pixels[k] = 255*color[0]
            pixels[k+1] = 255*color[1]
            pixels[k+2] = 255*color[2]
            k = k + 3

    fname = information['OUTPUT']
    save_imageP3(nCols, nRows, fname, pixels)
            

def raytrace(nearest_t, information, sphere_index, origin, ray_dir,depth,s_normal):
    if depth>3:     # spawn no more than three reflection rays for each pixel
        colour = np.zeros((3))
        return colour
    if(nearest_t == np.inf):        #   if no intersection
        colour = np.zeros((3))
        return colour
    else:
        clocal = np.zeros((3))
        # first, add ambient to colour
        l_a = np.array([information['AMBIENT'][0], information['AMBIENT'][1], information['AMBIENT'][2]])
        sphere_colour = np.array([information['SPHERE'][sphere_index][7], information['SPHERE'][sphere_index][8],information['SPHERE'][sphere_index][9]])
        ambient = information['SPHERE'][sphere_index][10] * l_a * sphere_colour
        clocal += ambient

        intersect_pixel = np.add(origin, ray_dir*nearest_t)
        adjusted_intersect_pixel = intersect_pixel + s_normal*0.0001      # to avoid false intersections due to numerical errors

        for light in information['LIGHT']:
            light_pos = np.array([light[1], light[2], light[3]])
            light_dir_m = light_pos - intersect_pixel
            light_dir = light_dir_m / np.linalg.norm(light_dir_m)
            temp, to_light_t, temp2 = nearest_intersection(information['SPHERE'], adjusted_intersect_pixel, light_dir)
        
            if to_light_t == np.inf:       # if no intersection
                light_colour = np.array([light[4], light[5], light[6]])
                
                # diffuse
                k_d = information['SPHERE'][sphere_index][11]
                clocal += k_d * light_colour * np.dot(s_normal, light_dir) * sphere_colour
                
                # specular
                k_s = information['SPHERE'][sphere_index][12]
                spec_exp = information['SPHERE'][sphere_index][14]
                origin_dir_m = origin-intersect_pixel
                origin_dir = origin_dir_m / np.linalg.norm(origin_dir_m)
                r = 2*np.dot(s_normal, light_dir)*s_normal - light_dir
                spec = k_s * light_colour * ((np.dot(r, origin_dir)) ** spec_exp)     
                clocal = clocal + spec

            else:       # no contribute to the colour
                clocal = clocal
    depth += 1

    # reflection
    v = -2 * (np.dot(s_normal,ray_dir)) * s_normal + ray_dir
    v = v / np.linalg.norm(v)
    re_sphere_index, re_ray_t, re_normal = nearest_intersection(information['SPHERE'], adjusted_intersect_pixel, v)
    c_re = raytrace(re_ray_t, information, re_sphere_index, adjusted_intersect_pixel, v,depth,re_normal)

    return clocal + information['SPHERE'][sphere_index][13] * c_re
    

if __name__ == '__main__':
    main()
