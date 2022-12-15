# Ray-Tracer
A basic implementation of a ray tracer using python that exploits numpy arrays and functions. The program handles local illumination of spheres, reflections and shadows, and will output result images in PPM format (P3).

# Input

The program takes a single argument, which is the name of the file to be parsed. Some test files are provided in the folder "Tests-and-Keys". The test files contains the following contents:

* The near plane\*\*, left\*\*, right\*\*, top\*\*, and bottom\*\*
* The resolution of the image nColumns\* and nRows\*
* The position\*\* and scaling\*\* (non-uniform), color\*\*\*, Ka\*\*\*, Kd\*\*\*, Ks\*\*\*, Kr\*\*\* and the specular exponent n\* of a sphere
* The position** and intensity*** of a point light source
* The background colour \*\*\*
* The scene’s ambient intensity\*\*\*
* The output file name    

\*int &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; \*\*float &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; \*\*\*float between 0 and 1
<br></br>
The format of the test files is as follows:   

NEAR \<n\>   
LEFT \<l\>   
RIGHT \<r\>   
BOTTOM \<b\>    
TOP \<t\>    
RES \<x\> \<y\>    
SPHERE \<name\> \<pos x\> \<pos y\> \<pos z\> \<scl x\> \<scl y\> \<scl z\> \<r\> \<g\> \<b\> \<Ka\> \<Kd\> \<Ks\> \<Kr\> \<n\>   
LIGHT \<name\> \<pos x\> \<pos y\> \<pos z\> \<Ir\> \<Ig\> \<Ib\>   
BACK \<r\> \<g\> \<b\>     
AMBIENT \<Ir\> \<Ig\> \<Ib\>   
OUTPUT \<name\>   

# Examples

Here are some examples of input and output:
```
python RayTracer.py testSample.txt
```
<img src="https://github.com/Tianennnn/Ray-Tracer/blob/main/Tests-and-Keys/keySample.png" width="200" height="200">

```
python RayTracer.py testShadow.txt
```
<img src="https://github.com/Tianennnn/Ray-Tracer/blob/main/Tests-and-Keys/keyShadow.png" width="200" height="200">

```
python RayTracer.py testReflection.txt
```
<img src="https://github.com/Tianennnn/Ray-Tracer/blob/main/Tests-and-Keys/keyReflection.png" width="200" height="200">
