from maya import cmds 
import math


def create_flower(petal_count = 30):
    if petal_count <= 0:
        raise ValueError("petal_count must be greater than zero")

    # create flower disk
    flower_disk = cmds.polyCylinder(r=1, h=0.1, sx=petal_count, sy=1, sz=1, ax=(0, 1, 0), rcp=0, cuv=3, ch=1)[0]
    flower_petals = []

    # create and shape petals
    petal = cmds.polyCube(w=0.8, h=0.1, d=0.2, sx=8, sy=1, name='petal')[0]
    # position left vertices of petal 
    petal_vertices_left = [
        (0.1, 0.13, 0.18), (0.2, 0.15, 0.21), 
        (0.4, 0.17, 0.23), (0.6, 0.15, 0.24),
        (0.8, 0.16, 0.18), (1, 0.2, 0)
    ]
    for i in range(12, 18):
        pos = petal_vertices_left[i - 12]
        cmds.move(pos[0], pos[1], pos[2], '{}.vtx[{}]'.format(petal, i))
    # position right vertices of petal
    petal_vertices_right = [
        (0.1, 0.13, -0.18), (0.2, 0.15, -0.21),
        (0.4, 0.17, -0.23), (0.6, 0.15, -0.24),
        (0.8, 0.16, -0.18), (1, 0.2, 0)
    ]
    for i in range(21, 27):
        pos = petal_vertices_right[i - 21]
        cmds.move(pos[0], pos[1], pos[2], '{}.vtx[{}]'.format(petal, i))

    cmds.select(clear=True)

    # calculate angle increment to evenly distribute petals around disk
    rotation_increment = 360 / petal_count

    for i in range(petal_count):
        angle = i * rotation_increment # calculate rotation angle for petal

        petal_instance = cmds.duplicate(petal)[0] # duplicate petal
        cmds.rotate(90, 0, 0, petal_instance) # lay petal flat

        # position petal at edge of disk
        radius = 1.3  
        x = radius * math.cos(math.radians(angle))
        z = radius * math.sin(math.radians(angle))
        cmds.move(x, 0, z, petal_instance)

        # rotate petal to align with disk's face
        cmds.rotate(0, -angle, 0, petal_instance)

        # save petal to list
        flower_petals.append(petal_instance)

    # delete original petal used for duplication
    cmds.delete(petal)

    return flower_disk, flower_petals
