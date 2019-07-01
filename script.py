import bpy
import sys


def main():
    args = sys.argv

    try:
        args = args[args.index("--") + 1:]
    except ValueError:
        args = []

    if len(args) < 2:
        print('Use: blender -b -P plugin.py -P script.py -- [dff] [obj]')
        exit(1)

    [source, output] = args

    # Select all objects
    for obj in bpy.context.scene.objects:
        obj.select = True

    # Delete selected objects
    bpy.ops.object.delete()

    # Import dff object
    imported_object = bpy.ops.import_rw.dff(
        'EXEC_DEFAULT', filepath=source)

    # Export scene to obj file
    bpy.ops.export_scene.obj(filepath=output)


if __name__ == '__main__':
    main()
