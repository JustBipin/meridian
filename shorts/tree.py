import random

import numpy as np
from manim import *

# ============================================================
# DESIGN & CONTENT TOKENS
# ============================================================

BACKGROUND_COLOR = "#000000"

TRUNK_COLOR = "#5d4037"
BRANCH_COLOR_MID = "#795548"
TWIG_COLOR = "#a1887f"

PALETTE_A_HEX = ["#1A4314", "#2E7D32", "#4CAF50"]
PALETTE_B_HEX = ["#556B2F", "#8BC34A", "#CDDC39"]

MAX_DEPTH = 5

INITIAL_LENGTH = 1.80
LENGTH_DECAY = 0.68

INITIAL_THICKNESS = 0.10
THICKNESS_DECAY = 0.65

BRANCH_ANGLE_MEAN = 34.0
BRANCH_ANGLE_STD = 7.0

PHOTOTROPISM_STRENGTH = 0.22
GRAVITY_STRENGTH = 0.12
BEND_STRENGTH = 0.06

CAMERA_PHI = 72 * DEGREES
CAMERA_THETA = -40 * DEGREES
ZOOM_FACTOR = 1.10

_leaf_rng = np.random.RandomState(9001)
_leaf_random = random.Random(9002)


# ============================================================
# COLOR & GEOMETRY UTILITIES
# ============================================================


def blend_colors(color1_hex, color2_hex, alpha):
    c1 = np.array(color_to_rgb(color1_hex))
    c2 = np.array(color_to_rgb(color2_hex))

    blended = (1 - alpha) * c1 + alpha * c2

    return rgb_to_color(blended)


def sample_gradient(hex_colors, alpha):
    alpha = np.clip(alpha, 0.0, 1.0)

    num_segments = len(hex_colors) - 1
    scaled = alpha * num_segments

    index = int(scaled)

    if index >= num_segments:
        return hex_colors[-1]

    local_alpha = scaled - index

    return blend_colors(hex_colors[index], hex_colors[index + 1], local_alpha)


def get_harmonized_leaf_color(depth_factor):
    shift = _leaf_rng.uniform(-0.1, 0.1)

    color_a_sample = np.clip(depth_factor + shift, 0, 1)

    base_color = sample_gradient(PALETTE_A_HEX, color_a_sample)

    accent_weight = np.clip(depth_factor * 1.5 - 0.2, 0, 0.8)

    accent_color = sample_gradient(PALETTE_B_HEX, depth_factor)

    return blend_colors(base_color, accent_color, accent_weight)


# ============================================================
# SMOOTH, CURVED BEZIER LEAF
# ============================================================


class NaturalLeaf(VGroup):
    def __init__(self, length=0.18, width=0.07, color="#4CAF50", **kwargs):
        super().__init__(**kwargs)

        half_len = length * 0.5
        max_w = width * 0.5

        base = np.array([0, -half_len, 0])
        tip = np.array([0, half_len, 0])

        r_mid = (base + tip) * 0.5 + np.array([max_w, 0, 0.02])

        blade_right = CubicBezier(base, base + np.array([max_w * 0.5, 0, 0]), r_mid, tip)

        l_mid = (base + tip) * 0.5 + np.array([-max_w, 0, 0.02])

        blade_left = CubicBezier(tip, l_mid, base + np.array([-max_w * 0.5, 0, 0]), base)

        blade_shape = VMobject()

        blade_shape.set_points_as_corners(blade_right.get_points())

        blade_shape.add_points_as_corners(blade_left.get_points())

        blade_shape.close_path()

        blade_shape.set_fill(color=color, opacity=0.92)

        blade_shape.set_stroke(color=blend_colors(color, "#082106", 0.3), width=0.4)

        self.add(blade_shape)

        vein = CubicBezier(
            base,
            base + np.array([0, half_len * 0.3, -0.01]),
            tip + np.array([0, -half_len * 0.3, 0.01]),
            tip,
            color=blend_colors(color, "#082106", 0.5),
            stroke_width=0.6,
        )

        self.add(vein)


# ============================================================
# NATURAL LEAF CLUSTER
# ============================================================


class TexturedLeafCluster(VGroup):
    def __init__(self, position, depth_factor=0.5, scale=0.25, **kwargs):
        super().__init__(**kwargs)

        n_leaves = _leaf_rng.randint(4, 8)

        for i in range(n_leaves):
            leaf_length = scale * _leaf_rng.uniform(1.20, 1.80)

            leaf_width = leaf_length * _leaf_rng.uniform(0.24, 0.40)

            leaf_color = get_harmonized_leaf_color(depth_factor)

            leaf = NaturalLeaf(length=leaf_length, width=leaf_width, color=leaf_color)

            azimuth = _leaf_rng.uniform(0, 2 * np.pi)

            elevation = _leaf_rng.uniform(0.25, 1.15)

            direction = np.array([
                np.cos(azimuth) * np.cos(elevation),
                np.sin(azimuth) * np.cos(elevation),
                np.sin(elevation),
            ])

            offset_distance = _leaf_rng.uniform(scale * 0.15, scale * 0.65)

            offset = direction * offset_distance

            leaf.move_to(position + offset)

            leaf.rotate(_leaf_rng.uniform(-0.35, 0.35), axis=OUT)

            leaf.rotate(_leaf_rng.uniform(-0.75, 0.75), axis=RIGHT)

            leaf.rotate(azimuth, axis=UP)

            leaf.scale(_leaf_rng.uniform(0.80, 1.15))

            self.add(leaf)

        self.move_to(position)


# ============================================================
# TAPERED SMOOTH CURVED BRANCH
# ============================================================


class TaperedSmoothBranch(VGroup):
    def __init__(self, start, mid, end, start_thick, end_thick, color, **kwargs):
        super().__init__(**kwargs)

        mid_thick = (start_thick + end_thick) * 0.5

        # Cubic Bezier control points
        cp1 = start + (mid - start) * 0.4
        cp2 = end + (mid - end) * 0.4

        n_samples = 12

        # Create tapered 3D segments
        for i in range(n_samples - 1):
            t = i / (n_samples - 1)
            t_next = (i + 1) / (n_samples - 1)

            p1 = self._eval_bezier(start, cp1, cp2, end, t)

            p2 = self._eval_bezier(start, cp1, cp2, end, t_next)

            segment_thick = start_thick + (end_thick - start_thick) * t

            next_thick = start_thick + (end_thick - start_thick) * t_next

            avg_thick = (segment_thick + next_thick) * 0.5

            seg = Line3D(start=p1, end=p2, thickness=max(0.003, avg_thick * 1.2), color=color)

            self.add(seg)

        # Smooth joints
        joint_start = Sphere(center=start, radius=max(0.003, start_thick * 0.65), color=color)

        joint_mid = Sphere(center=mid, radius=max(0.003, mid_thick * 0.65), color=color)

        joint_end = Sphere(center=end, radius=max(0.003, end_thick * 0.65), color=color)

        self.add(joint_start, joint_mid, joint_end)

    @staticmethod
    def _eval_bezier(p0, p1, p2, p3, t):
        """Evaluate cubic Bezier curve at parameter t."""

        mt = 1 - t

        return mt**3 * p0 + 3 * mt**2 * t * p1 + 3 * mt * t**2 * p2 + t**3 * p3


# ============================================================
# TREE NODE
# ============================================================


class TreeNode:
    def __init__(self, p_start, orientation, length, thickness, depth, prev_phi, start_time, duration):
        self.p_start = p_start
        self.orientation = orientation
        self.length = length

        self.start_thickness = thickness

        self.end_thickness = thickness * THICKNESS_DECAY

        self.depth = depth
        self.prev_phi = prev_phi

        self.start_time = start_time
        self.duration = duration

        up = orientation[:, 2]

        growth_factor = depth / MAX_DEPTH

        tropism = np.array([0.0, 0.0, PHOTOTROPISM_STRENGTH * growth_factor - GRAVITY_STRENGTH * (1.0 - growth_factor)])

        self.growth_dir = up + tropism

        self.growth_dir /= np.linalg.norm(self.growth_dir)

        self.p_end = p_start + self.growth_dir * length

        # Random direction perpendicular to growth direction
        rand_dir = np.random.randn(3)

        rand_dir -= rand_dir.dot(self.growth_dir) * self.growth_dir

        rand_norm = np.linalg.norm(rand_dir)

        if rand_norm > 1e-6:
            rand_dir /= rand_norm

        bend_mag = np.random.uniform(0.2, 0.6) * BEND_STRENGTH * length

        self.p_mid = p_start + self.growth_dir * (length * 0.5) + rand_dir * bend_mag

        # Branch color by depth
        t_color = depth / MAX_DEPTH

        if t_color < 0.5:
            self.color = blend_colors(TRUNK_COLOR, BRANCH_COLOR_MID, t_color * 2.0)

        else:
            self.color = blend_colors(BRANCH_COLOR_MID, TWIG_COLOR, (t_color - 0.5) * 2.0)

        self.branch_mob = TaperedSmoothBranch(
            start=p_start,
            mid=self.p_mid,
            end=self.p_end,
            start_thick=max(0.003, self.start_thickness),
            end_thick=max(0.002, self.end_thickness),
            color=self.color,
        )

        self.child1 = None
        self.child2 = None
        self.apical = None
        self.foliage = None

        self.build_children()

    def build_children(self):

        # ----------------------------------------------------
        # TERMINAL / LEAF NODE
        # ----------------------------------------------------

        if self.depth >= MAX_DEPTH:
            leaf_time = self.start_time + self.duration

            leaf_scale = _leaf_rng.uniform(0.20, 0.30)

            depth_factor = self.depth / MAX_DEPTH

            clusters = [TexturedLeafCluster(position=self.p_end, depth_factor=depth_factor, scale=leaf_scale)]

            if _leaf_rng.uniform(0.0, 1.0) < 0.60:
                offset = _leaf_rng.uniform(-0.12, 0.12, size=3)

                clusters.append(
                    TexturedLeafCluster(
                        position=self.p_end + offset, depth_factor=depth_factor * 0.95, scale=leaf_scale * 0.80
                    )
                )

            foliage_group = VGroup(*clusters)

            self.foliage = (foliage_group, leaf_time)

            return

        # ----------------------------------------------------
        # CHILD BRANCH PARAMETERS
        # ----------------------------------------------------

        growth_factor = self.depth / MAX_DEPTH

        rotation_step = np.radians(np.random.uniform(60, 120))

        base_phi = self.prev_phi + rotation_step

        child_thick = self.end_thickness

        child_len = self.length * LENGTH_DECAY

        child_duration = self.duration * 0.80

        spread_angle = BRANCH_ANGLE_MEAN + (1.0 - growth_factor) * 10.0

        angle = np.radians(np.random.normal(spread_angle, BRANCH_ANGLE_STD))

        # ----------------------------------------------------
        # FIRST LATERAL BRANCH
        # ----------------------------------------------------

        t_sub1 = np.random.uniform(0.50, 0.60)

        p_branch1 = self.p_start + self.growth_dir * (self.length * t_sub1)

        start_time_c1 = self.start_time + self.duration * t_sub1

        rx1 = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])

        rz1 = np.array([[np.cos(base_phi), -np.sin(base_phi), 0], [np.sin(base_phi), np.cos(base_phi), 0], [0, 0, 1]])

        self.child1 = TreeNode(
            p_start=p_branch1,
            orientation=self.orientation @ rz1 @ rx1,
            length=(child_len * np.random.uniform(0.85, 0.98)),
            thickness=child_thick,
            depth=self.depth + 1,
            prev_phi=base_phi,
            start_time=start_time_c1,
            duration=child_duration,
        )

        # ----------------------------------------------------
        # SECOND LATERAL BRANCH
        # ----------------------------------------------------

        t_sub2 = np.random.uniform(0.85, 0.95)

        p_branch2 = self.p_start + self.growth_dir * (self.length * t_sub2)

        start_time_c2 = self.start_time + self.duration * t_sub2

        phi2 = base_phi + np.radians(np.random.uniform(160, 200))

        rz2 = np.array([[np.cos(phi2), -np.sin(phi2), 0], [np.sin(phi2), np.cos(phi2), 0], [0, 0, 1]])

        self.child2 = TreeNode(
            p_start=p_branch2,
            orientation=self.orientation @ rz2 @ rx1,
            length=(child_len * np.random.uniform(0.85, 0.98)),
            thickness=child_thick,
            depth=self.depth + 1,
            prev_phi=phi2,
            start_time=start_time_c2,
            duration=child_duration,
        )

        # ----------------------------------------------------
        # APICAL BRANCH
        # ----------------------------------------------------

        start_time_ap = self.start_time + self.duration

        self.apical = TreeNode(
            p_start=self.p_end,
            orientation=self.orientation,
            length=child_len * 1.02,
            thickness=child_thick * 1.02,
            depth=self.depth + 1,
            prev_phi=base_phi,
            start_time=start_time_ap,
            duration=child_duration,
        )

    def collect_by_depth(self, depth_dict):

        if self.depth not in depth_dict:
            depth_dict[self.depth] = {"branches": [], "foliage": []}

        depth_dict[self.depth]["branches"].append(self.branch_mob)

        if self.foliage:
            depth_dict[self.depth]["foliage"].append(self.foliage[0])

        if self.child1:
            self.child1.collect_by_depth(depth_dict)

        if self.child2:
            self.child2.collect_by_depth(depth_dict)

        if self.apical:
            self.apical.collect_by_depth(depth_dict)


# ============================================================
# SCENE
# ============================================================


class ThreeDLSystemTree(ThreeDScene):
    def construct(self):

        # ----------------------------------------------------
        # CAMERA
        # ----------------------------------------------------

        self.camera.background_color = BACKGROUND_COLOR

        self.set_camera_orientation(phi=CAMERA_PHI, theta=CAMERA_THETA, zoom=ZOOM_FACTOR)

        self.begin_ambient_camera_rotation(rate=0.45)

        # ----------------------------------------------------
        # PLATFORM
        # ----------------------------------------------------

        platform = Circle(radius=3.4, color="#222222", fill_color="#111111", fill_opacity=0.90)

        platform.move_to([0, 0, -2.0])

        self.add(platform)

        # ----------------------------------------------------
        # DETERMINISTIC RANDOM SEEDS
        # ----------------------------------------------------

        np.random.seed(6012)
        random.seed(6012)

        # ----------------------------------------------------
        # ROOT
        # ----------------------------------------------------

        root_node = TreeNode(
            p_start=np.array([0.0, 0.0, -2.0]),
            orientation=np.eye(3),
            length=INITIAL_LENGTH,
            thickness=INITIAL_THICKNESS,
            depth=0,
            prev_phi=0.0,
            start_time=0.0,
            duration=1.4,
        )

        # ----------------------------------------------------
        # COLLECT TREE BY GENERATION
        # ----------------------------------------------------

        depth_dict = {}

        root_node.collect_by_depth(depth_dict)

        # ----------------------------------------------------
        # GROW GENERATION BY GENERATION
        # ----------------------------------------------------

        for d in sorted(depth_dict.keys()):
            branches = depth_dict[d]["branches"]
            foliage = depth_dict[d]["foliage"]

            # Branch growth
            if branches:
                self.play(
                    LaggedStart(*[Create(branch) for branch in branches], lag_ratio=0.10, run_time=1.0, rate_func=smooth)
                )

            # Leaf growth
            if foliage:
                self.play(LaggedStart(*[GrowFromCenter(f) for f in foliage], lag_ratio=0.03, run_time=1.4, rate_func=smooth))

        # ----------------------------------------------------
        # HOLD
        # ----------------------------------------------------

        self.wait(3.0)

        self.stop_ambient_camera_rotation()

        self.wait(0.5)
