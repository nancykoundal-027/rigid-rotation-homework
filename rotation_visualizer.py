import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# ============================================================
# ROTATION MATRICES
# ============================================================

def rotation_x(angle):
    a = np.radians(angle)
    return np.array([
        [1, 0, 0],
        [0, np.cos(a), -np.sin(a)],
        [0, np.sin(a), np.cos(a)]
    ])


def rotation_y(angle):
    a = np.radians(angle)
    return np.array([
        [np.cos(a), 0, np.sin(a)],
        [0, 1, 0],
        [-np.sin(a), 0, np.cos(a)]
    ])


def rotation_z(angle):
    a = np.radians(angle)
    return np.array([
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a), np.cos(a), 0],
        [0, 0, 1]
    ])


def get_rotation_matrix(rx, ry, rz):
    """
    Rotation sequence:
    X -> Y -> Z

    R = Rz * Ry * Rx
    """
    return rotation_z(rz) @ rotation_y(ry) @ rotation_x(rx)


# ============================================================
# RIGID BODY GEOMETRY
# ============================================================

# Dimensions of the rigid body
body_length = 1.5
body_width = 1.0
body_height = 0.7

# Eight corners of the rigid body
corners = np.array([
    [-body_length/2, -body_width/2, -body_height/2],
    [ body_length/2, -body_width/2, -body_height/2],
    [ body_length/2,  body_width/2, -body_height/2],
    [-body_length/2,  body_width/2, -body_height/2],

    [-body_length/2, -body_width/2,  body_height/2],
    [ body_length/2, -body_width/2,  body_height/2],
    [ body_length/2,  body_width/2,  body_height/2],
    [-body_length/2,  body_width/2,  body_height/2]
])

# Six faces of the cuboid
faces = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [1, 2, 6, 5],
    [0, 3, 7, 4]
]


# ============================================================
# FIGURE
# ============================================================

fig = plt.figure(figsize=(14, 8))

ax = fig.add_axes(
    [0.04, 0.10, 0.58, 0.82],
    projection="3d"
)

ax.set_title(
    "Interactive 3D Rigid Body Rotation",
    fontsize=17,
    fontweight="bold"
)


# ============================================================
# MATRIX AND INFORMATION AREA
# ============================================================

matrix_ax = fig.add_axes(
    [0.67, 0.52, 0.30, 0.30]
)

matrix_ax.axis("off")

matrix_ax.text(
    0.5,
    0.90,
    "Rotation Matrix R",
    ha="center",
    fontsize=16,
    fontweight="bold"
)

matrix_text = matrix_ax.text(
    0.5,
    0.45,
    "",
    ha="center",
    va="center",
    fontsize=14,
    family="monospace"
)


angle_ax = fig.add_axes(
    [0.67, 0.38, 0.30, 0.10]
)

angle_ax.axis("off")

angle_text = angle_ax.text(
    0.5,
    0.5,
    "",
    ha="center",
    va="center",
    fontsize=13,
    family="monospace"
)


# ============================================================
# SLIDERS
# ============================================================

slider_x_ax = fig.add_axes(
    [0.68, 0.25, 0.25, 0.035]
)

slider_y_ax = fig.add_axes(
    [0.68, 0.19, 0.25, 0.035]
)

slider_z_ax = fig.add_axes(
    [0.68, 0.13, 0.25, 0.035]
)


slider_x = Slider(
    slider_x_ax,
    "Rotation X",
    -180,
    180,
    valinit=0,
    valstep=1
)

slider_y = Slider(
    slider_y_ax,
    "Rotation Y",
    -180,
    180,
    valinit=0,
    valstep=1
)

slider_z = Slider(
    slider_z_ax,
    "Rotation Z",
    -180,
    180,
    valinit=0,
    valstep=1
)


# ============================================================
# RESET BUTTON
# ============================================================

reset_ax = fig.add_axes(
    [0.68, 0.055, 0.12, 0.045]
)

reset_button = Button(
    reset_ax,
    "Reset"
)


# ============================================================
# UPDATE FUNCTION
# ============================================================

def update(val=None):

    rx = slider_x.val
    ry = slider_y.val
    rz = slider_z.val

    # Calculate rotation matrix
    R = get_rotation_matrix(rx, ry, rz)

    # Rotate rigid body corners
    rotated_corners = (R @ corners.T).T

    # Rotate body coordinate axes
    axis_length = 2.0

    body_x = R @ np.array([axis_length, 0, 0])
    body_y = R @ np.array([0, axis_length, 0])
    body_z = R @ np.array([0, 0, axis_length])

    # Clear 3D view
    ax.clear()

    # ========================================================
    # AXIS SETTINGS
    # ========================================================

    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.7, 2.7)
    ax.set_zlim(-2.7, 2.7)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_box_aspect([1, 1, 1])

    ax.view_init(
        elev=25,
        azim=35
    )

    ax.set_title(
        "Interactive 3D Rigid Body Rotation",
        fontsize=16,
        fontweight="bold"
    )

    # ========================================================
    # FIXED REFERENCE FRAME
    # ========================================================

    ax.quiver(
        0, 0, 0,
        2.0, 0, 0,
        color="red",
        linewidth=3,
        arrow_length_ratio=0.12
    )

    ax.quiver(
        0, 0, 0,
        0, 2.0, 0,
        color="green",
        linewidth=3,
        arrow_length_ratio=0.12
    )

    ax.quiver(
        0, 0, 0,
        0, 0, 2.0,
        color="blue",
        linewidth=3,
        arrow_length_ratio=0.12
    )

    ax.text(
        2.1, 0, 0,
        "X₀",
        color="red",
        fontsize=13,
        fontweight="bold"
    )

    ax.text(
        0, 2.1, 0,
        "Y₀",
        color="green",
        fontsize=13,
        fontweight="bold"
    )

    ax.text(
        0, 0, 2.1,
        "Z₀",
        color="blue",
        fontsize=13,
        fontweight="bold"
    )

    # ========================================================
    # ROTATING RIGID BODY
    # ========================================================

    rotated_faces = [
        [rotated_corners[index] for index in face]
        for face in faces
    ]

    body = Poly3DCollection(
        rotated_faces,
        alpha=0.35,
        edgecolor="black",
        linewidth=1.5
    )

    ax.add_collection3d(body)

    # ========================================================
    # RIGID BODY EDGES
    # ========================================================

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    for start, end in edges:

        p1 = rotated_corners[start]
        p2 = rotated_corners[end]

        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            [p1[2], p2[2]],
            color="black",
            linewidth=2
        )

    # Rigid body label
    center = R @ np.array([0, 0, body_height/2 + 0.2])

    ax.text(
        center[0],
        center[1],
        center[2],
        "RIGID BODY",
        fontsize=11,
        fontweight="bold"
    )

    # ========================================================
    # BODY COORDINATE FRAME
    # ========================================================

    # X axis of body
    ax.quiver(
        0, 0, 0,
        body_x[0],
        body_x[1],
        body_x[2],
        color="darkred",
        linewidth=4,
        arrow_length_ratio=0.10
    )

    # Y axis of body
    ax.quiver(
        0, 0, 0,
        body_y[0],
        body_y[1],
        body_y[2],
        color="darkgreen",
        linewidth=4,
        arrow_length_ratio=0.10
    )

    # Z axis of body
    ax.quiver(
        0, 0, 0,
        body_z[0],
        body_z[1],
        body_z[2],
        color="darkblue",
        linewidth=4,
        arrow_length_ratio=0.10
    )

    # Body labels
    ax.text(
        body_x[0],
        body_x[1],
        body_x[2],
        "X",
        color="darkred",
        fontsize=13,
        fontweight="bold"
    )

    ax.text(
        body_y[0],
        body_y[1],
        body_y[2],
        "Y",
        color="darkgreen",
        fontsize=13,
        fontweight="bold"
    )

    ax.text(
        body_z[0],
        body_z[1],
        body_z[2],
        "Z",
        color="darkblue",
        fontsize=13,
        fontweight="bold"
    )

    # ========================================================
    # ROTATION MATRIX
    # ========================================================

    matrix_text.set_text(
        "R = Rz · Ry · Rx\n\n"
        f"[ {R[0,0]:8.4f}  {R[0,1]:8.4f}  {R[0,2]:8.4f} ]\n"
        f"[ {R[1,0]:8.4f}  {R[1,1]:8.4f}  {R[1,2]:8.4f} ]\n"
        f"[ {R[2,0]:8.4f}  {R[2,1]:8.4f}  {R[2,2]:8.4f} ]"
    )

    # ========================================================
    # ANGLE READOUT
    # ========================================================

    angle_text.set_text(
        f"θx = {rx:.0f}°     "
        f"θy = {ry:.0f}°     "
        f"θz = {rz:.0f}°"
    )

    fig.canvas.draw_idle()


# ============================================================
# RESET
# ============================================================

def reset(event):

    slider_x.reset()
    slider_y.reset()
    slider_z.reset()


# ============================================================
# CONNECT SLIDERS
# ============================================================

slider_x.on_changed(update)
slider_y.on_changed(update)
slider_z.on_changed(update)

reset_button.on_clicked(reset)


# ============================================================
# START
# ============================================================

update()

plt.show()
