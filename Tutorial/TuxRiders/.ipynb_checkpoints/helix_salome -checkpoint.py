# Creation of a PipeBiNormalAlongVector
import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New()
from math import pi


def MakeHelix(radius, height, rotation, direction):
    #  - create a helix -
    radius = 1.0 * radius
    height = 1.0 * height
    rotation = 1.0 * rotation
    if direction > 0:
        direction = +1
    else:
        direction = -1
        pass
    from math import sqrt
    length_z  = height
    length_xy = radius*rotation
    length = sqrt(length_z*length_z + length_xy*length_xy)
    nb_steps = 1
    epsilon = 1.0e-6
    while 1:
        z_step = height / nb_steps
        angle_step = rotation / nb_steps
        z = 0.0
        angle = 0.0
        helix_points = []
        for n in range(nb_steps+1):
            from math import cos, sin
            x = radius * cos(angle)
            y = radius * sin(angle)
            p = geompy.MakeVertex(x, y, z)
            helix_points.append( p )
            z += z_step
            angle += direction * angle_step
            pass
        helix = geompy.MakeInterpol(helix_points)
        length_test = geompy.BasicProperties(helix)[0]
        prec = abs(length-length_test)/length
        # print nb_steps, length_test, prec
        if prec < epsilon:
            break
        nb_steps *= 2
        pass
    return helix

def MakeSpring(radius, height, rotation, direction, thread_radius, base_rotation=0.0):
    #  - create a pipe -
    thread_radius = 1.0 * thread_radius
    # create a helix
    helix = MakeHelix(radius, height, rotation, direction)
    # base in the (Ox, Oz) plane
    base = geompy.MakeDiskR(thread_radius, 3)
    geompy.TranslateDXDYDZ(base, radius, 0, 0)
    # create a binormal vector
    binormal = geompy.MakeVectorDXDYDZ(0.0, 0.0, 10.0)
    # create a pipe
    spring = geompy.MakePipeBiNormalAlongVector(base, helix, binormal)
    # do rotation
    geompy.Rotate(spring, OY, 10*pi/180.0)
    geompy.Rotate(spring, OZ, 15*pi/180.0)
    # Publish in the study
    geompy.addToStudy(base, "base")
    geompy.addToStudy(helix, "helix")
    geompy.addToStudy(binormal, "binormal")
    geompy.addToStudy(spring, "spring")
    return spring


O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

spring = MakeSpring(50, 200, 10*pi, 1, 14.5, 0)
