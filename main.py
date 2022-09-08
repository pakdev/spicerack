from solid import circle, scad_render_to_file
from solid.utils import arc, translate, rotate
from solid.objects import linear_extrude, color, cube

ROTATION = 45
SEGMENTS = 100
JAR_UPPER = 67
JAR_LOWER = 62
JAR_HEIGHT = 80
JAR_BUFFER = 4
LID_BUFFER = 10
HOLDER_LENGTH = 300
HOLDER_HEIGHT = 120


def rotate_point(y, z, point, child):
    return translate(point)(rotate([0, y, z])(translate((-x for x in point))(child)))


def create_jar(upper_diameter, lower_diameter, height, color_name, offset=(0, 0, 0)):
    scale = upper_diameter / lower_diameter
    model_2d = circle(d=upper_diameter)
    model_3d = color(color_name)(
        rotate((0, ROTATION, 0))(
            translate(offset)(
                linear_extrude(height, scale=scale, center=True)(model_2d)
            )
        )
    )
    return model_3d


def create_holder(cut_bottom=False):
    near_plane = translate((-160, 0, 0))(color("purple")((cube(200, center=True))))
    far_plane = translate((120, 0, 0))(color("orange")((cube(200, center=True))))
    top_plane = rotate((0, ROTATION, 0))(
        translate((0, 0, 130))(color("red")(cube(200, center=True)))
    )

    holder_2d = arc(rad=HOLDER_LENGTH, start_degrees=-18, end_degrees=18)
    holder = translate((-HOLDER_LENGTH / 2, 0, 0))(
        linear_extrude(HOLDER_HEIGHT, center=True)(holder_2d)
    )

    jar = create_jar(JAR_UPPER, JAR_LOWER, JAR_HEIGHT, "green", offset=(0, 0, 1))
    sleeve = create_jar(
        JAR_UPPER + JAR_BUFFER * 10,
        JAR_LOWER + JAR_BUFFER * 20,
        JAR_HEIGHT - 20,
        "white",
        offset=(0, 0, 5),
    )
    model = (holder - near_plane - far_plane - top_plane) + sleeve - jar
    if cut_bottom:
        groove = create_jar(
            JAR_UPPER + LID_BUFFER * 10,
            JAR_LOWER + LID_BUFFER * 10,
            JAR_HEIGHT + 10,
            "yellow",
            offset=(125, 0, 0),
        )
        model -= groove

    return model


def main():
    top_holders = []
    bot_holders = []
    for i in range(10):
        top_holders.append(rotate_point(0, 36 * i, (-150, 0, 0), create_holder(True)))
        bot_holders.append(
            rotate_point(
                0, 36 * i, (-150, 0, 0), translate((0, 0, -129))(create_holder(False))
            )
        )
    all_holders = sum(top_holders) + sum(bot_holders)
    # all_holders = create_holder(True)
    scad_render_to_file(all_holders, "spicerack.scad", file_header=f"$fn = {SEGMENTS};")


if __name__ == "__main__":
    main()
