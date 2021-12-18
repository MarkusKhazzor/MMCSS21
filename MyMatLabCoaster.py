import numpy as np
from Modules.CurveUtilities import *
from Modules.TrackReader import *
from matplotlib import cm  # easy color mapping
import matplotlib as mpl
import matplotlib.pyplot as plt
# IMPORTANT SETTING PC DEPENDENT
# npl.use('Qt5Agg') # might be needed if matplot lib does not generate a separate window

from matplotlib.animation import FuncAnimation

data_storage = {
    # general bezier curve function data created with the sample pillar points and their solved handles
    "curves": [],
    "curves_first_derivatives": [],
    "curves_second_derivatives": [],
    "curves_third_derivatives": [],

    # calculated data of points on all the curves according to their splitting intervals
    "points_on_curves": [],
    "points_on_curves_first_derivatives": [],
    "points_on_curves_second_derivatives": [],
    "points_on_curves_third_derivatives": [],

    "points_on_curves_curvatures": [],
    "points_on_curves_curvature_norms": [],
    "points_on_curves_torsions": [],
    "points_on_curves_torsions_norms": [],

    "points_on_curves_binormals": [],
    "points_on_curves_tangents": [],
    "points_on_curves_normals": []
}

# Start reading the input rollercoaster pillar points
sample_points = extract_rollercoaster_pillar_points()

# Calculate bezier curve handles
p0s, p1s, p2s, p3s = calculate_rollercoaster_samples_and_handles(sample_points)

# PREPARE CURVE TO BE DRAWN
# get all curves & their different form-functions!
for i, sample in enumerate(p0s):
    data_storage["curves"].append(receive_bezier_curve(sample, p1s[i], p2s[i], p3s[i]))
    data_storage["curves_first_derivatives"].append(receive_curve_first_derivative(sample, p1s[i], p2s[i], p3s[i]))
    data_storage["curves_second_derivatives"].append(receive_curve_second_derivative(sample, p1s[i], p2s[i], p3s[i]))
    data_storage["curves_third_derivatives"].append(receive_curve_third_derivative(sample, p1s[i], p2s[i], p3s[i]))

# calculate points on curves for chosen curve separation amount and calculate their specific data
n_curves = len(data_storage["curves"])
curve_separation_amount = 10

for t in np.linspace(start=0, stop=n_curves, num=n_curves * curve_separation_amount):

    t_as_integer_and_fractional = math.modf(t % n_curves)
    curve_index = int(t_as_integer_and_fractional[1])
    curve_t = t_as_integer_and_fractional[0]

    data_storage["points_on_curves"].append(data_storage["curves"][curve_index](curve_t))

    data_storage["points_on_curves_first_derivatives"].append(data_storage["curves_first_derivatives"][curve_index](curve_t))

    data_storage["points_on_curves_second_derivatives"].append(data_storage["curves_second_derivatives"][curve_index](curve_t))

    data_storage["points_on_curves_third_derivatives"].append(data_storage["curves_third_derivatives"][curve_index](curve_t))

    curvature = curvature_at_t(data_storage["curves_first_derivatives"][curve_index], data_storage["curves_second_derivatives"][curve_index])(curve_t)
    data_storage["points_on_curves_curvatures"].append(curvature)
    data_storage["points_on_curves_curvature_norms"].append(np.linalg.norm(curvature))

    torsion = torsion_at_t(data_storage["curves_first_derivatives"][curve_index], data_storage["curves_second_derivatives"][curve_index], data_storage["curves_third_derivatives"][curve_index])(curve_t)
    data_storage["points_on_curves_torsions"].append(torsion)
    data_storage["points_on_curves_torsions_norms"].append(np.linalg.norm(torsion))

    data_storage["points_on_curves_binormals"].append(binormal_vector_at_t(data_storage["curves_first_derivatives"][curve_index], data_storage["curves_second_derivatives"][curve_index])(curve_t))

    data_storage["points_on_curves_tangents"].append(tangent_at_t(data_storage["curves_first_derivatives"][curve_index])(curve_t))

    data_storage["points_on_curves_normals"].append(normal_vector_at_t(data_storage["curves_first_derivatives"][curve_index], data_storage["curves_second_derivatives"][curve_index])(curve_t))


# SET UP 3D ROLLERCOASTER TRACK
# potential tweak settings:  figsize=(20, 20), dpi=80
fig = plt.figure()
#  additional settings:
#  works for my pc to zoom in at start: https://stackoverflow.com/questions/12439588/how-to-maximize-a-plt-show-window-using-python
wm = plt.get_current_fig_manager()
wm.window.state('zoomed')

ax = fig.add_subplot(2,2,3, projection='3d')  # the first 2 parameters stay the same!
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
ax.set_xlim3d(-7, 7)
ax.set_ylim3d(-7, 7)
ax.set_zlim3d(-7, 7)

# plot all bezier curves as a continues track
points = np.array(data_storage["points_on_curves"])
ax.plot(points[:, 0], points[:, 1], points[:, 2], c='r')


# PLOT ADDITIONAL ROLLERCOASTER INFORMATION
# first derivative # speed
x1 = fig.add_subplot(3, 3, 1)
x1.set_xlabel('segmented_points')
x1.set_ylabel('first derivative')
# automatically takes 0-n as x values # amount
x1.plot(data_storage["points_on_curves_first_derivatives"])
# optional marker
x1_marker = x1.plot([0], [0], '|', ms=450)

# second derivative # acceleration - Beschleunigung
x2 = fig.add_subplot(3,3,2)
x2.set_xlabel('segmented_points')
x2.set_ylabel('second derivative')
x2.plot(data_storage["points_on_curves_second_derivatives"])
# optional marker
x2_marker = x2.plot([0], [0], '|', ms=450)

# third derivatives # jerk - Ruck
x3 = fig.add_subplot(3,3,3)
x3.set_xlabel('segmented_points')
x3.set_ylabel('third derivative')
x3.plot(data_storage["points_on_curves_third_derivatives"])
# optional marker
x3_marker = x3.plot([0], [0], '|', ms=450)

# torsion - Torsion
x4 = fig.add_subplot(3,3,6)
x4.set_xlabel('segmented_points')
x4.set_ylabel('torsion')
x4.plot(data_storage["points_on_curves_torsions_norms"])  # TODO Moritz/ Google DIFFERENCE BETWEEN NORM AND NOT NORM?!
# optional marker
x4_marker = x4.plot([0], [0], '|', ms=450)

# curvature - Krümmung
x5 = fig.add_subplot(3,3,9)
x5.set_xlabel('segmented_points')
x5.set_ylabel('curvature')
x5.plot(data_storage["points_on_curves_curvature_norms"]) # TODO Moritz/ Google DIFFERENCE BETWEEN NORM AND NOT NORM?!
# optional marker
x5_marker = x5.plot([0], [0], '|', ms=450)


# CALCULATE CURVATURE COLOR MAP
norm = mpl.colors.Normalize(vmin=min(data_storage["points_on_curves_curvature_norms"]), vmax=max(data_storage["points_on_curves_curvature_norms"]), clip=True)
color_mapper = cm.ScalarMappable(norm=norm, cmap=cm.cmaps_listed['plasma'])
# plot a colorbar legend for the curvature
plt.colorbar(mappable=color_mapper, ax=ax, label="point on curvature norm")


# ANIMATION
# draw a point on the curve
point = []

# draw Frenet-Dreibein
quiver_tangent = []
quiver_binormal_vector = []
quiver_normal_vector = []

# animation loop
def update(frame_number):
    global point  # needed since we dont work in a class!
    global quiver_tangent
    global quiver_binormal_vector
    global quiver_normal_vector

    # calc current point index position
    current_index = (frame_number % len(points))  # * 10 # 10 is speed

    # update point
    curve_point = points[current_index]
    # update markers
    x1_marker[0].set_data(current_index, 0)
    x2_marker[0].set_data(current_index, 0)
    x3_marker[0].set_data(current_index, 0)
    x4_marker[0].set_data(current_index, 0)
    x5_marker[0].set_data(current_index, 0)

    # delete last point &  Frenet-Dreibein
    if point:
        point.remove()

    if quiver_tangent:
        quiver_tangent.remove()

    if quiver_binormal_vector:
        quiver_binormal_vector.remove()

    if quiver_normal_vector:
        quiver_normal_vector.remove()

    # show new point with new curvature color and save last point to be able to delete
    point_color_curvature_dependent = color_mapper.to_rgba(data_storage["points_on_curves_curvature_norms"][current_index])  # get color
    point = ax.scatter(curve_point[0], curve_point[1], curve_point[2], s=40, c=np.array([point_color_curvature_dependent]), marker='o')

    # show "frenetsches dreibein"
    tangent = data_storage["points_on_curves_tangents"][current_index]
    quiver_tangent = ax.quiver(curve_point[0], curve_point[1], curve_point[2], tangent[0], tangent[1], tangent[2], color="g")

    binormal_vector = data_storage["points_on_curves_binormals"][current_index]
    quiver_binormal_vector = ax.quiver(curve_point[0], curve_point[1], curve_point[2], binormal_vector[0], binormal_vector[1], binormal_vector[2], color="y")

    normal_vector = data_storage["points_on_curves_normals"][current_index]
    quiver_normal_vector = ax.quiver(curve_point[0], curve_point[1], curve_point[2], normal_vector[0], normal_vector[1], normal_vector[2], color="r")


# execute animationLoop
animation = FuncAnimation(fig, update, interval=10) # , blit=True - saves performance

# render everything
plt.show()