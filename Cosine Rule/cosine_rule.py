from manimlib import *
import numpy as np

# ============================================================
#  STYLE CONSTANTS -- cinematic cold-open for the cosine rule video
#  This is the ONE scene in the project that departs from the usual
#  white "exam paper" background -- it opens dark/3b1b-style and
#  hands off to white at the very end of beat 5.
# ============================================================
LEG_A_COLOR   = "#00B8A9"   # teal   -- one leg of the right triangle
LEG_B_COLOR   = "#7B2CBF"   # purple -- other leg
HYP_C_COLOR   = "#FF6B00"   # orange -- hypotenuse / the side opposite the marked angle
ANGLE_COLOR   = "#750A0A"   # red    -- the marked/known angle (the right angle here)
ANCIENT_INK   = "#C9A66B"   # warm gold-tan -- hand-drawn "ancient ink" strokes
CONTEXT_GRAY  = "#8A8D91"   # muted neutral -- the "several other triangles" in beat 4
QUESTION_COLOR = "#8B0303"  # dark red -- rhetorical / bridge lines
CORRECTION_COLOR = "#FFB800" # gold -- the -2ab cos(C) correction term itself
BG_DARK       = "#0B0B0D"   # near-black cinematic backdrop
LIGHT_TEXT    = "#F5F1E8"   # warm off-white -- prose/equation text on the dark backdrop

# ============================================================
#  TIMING PLAN -- matches the provided VO subtitles exactly, T=0 at
#  scene start (subtitles start at 0:01). Re-check against the audio
#  track once mixed; these are all whole/half-second estimates.
#
#   T=1.0   "As long as 2000 BCE, different civilizations..."
#   T=16.0  "So what was that idea?"
#   T=18.0  "Take a right-angled triangle...90-degree angle."
#   T=23.0  "...tells us that the square"
#   T=27.0  "of the side opposite the right angle..."
#   T=31.0  "...sum of the square of the other two sides."
#   T=33.0  "But Pythagoras Theorem only applies..."
#   T=37.0  "real world, we have plenty of triangles..."
#   T=42.0  "So is there any modified form..."
#   T=45.0  "applies to any triangle?"
#   T~48.0  narration ends; remaining time is visual settle + white handoff
# ============================================================

# The right-angled "hero" triangle -- a clean 1.8 : 2.4 : 3.0 triple
# (0.6x of 3-4-5). Verified numerically: all three squares-on-sides
# come out as true squares and 1.8^2 + 2.4^2 = 3.0^2 exactly.
V_RIGHT = np.array([-1.2, -0.9, 0.0])   # the right-angle vertex
V_A     = np.array([ 1.2, -0.9, 0.0])   # end of leg a (horizontal)
V_TOP   = np.array([-1.2,  0.9, 0.0])   # end of leg b (vertical)

# Where the right-angle vertex moves to in beat 4 -- V_A and V_TOP
# stay fixed, opening the angle to roughly 60.5 degrees.
V_RIGHT_NEW = np.array([0.3, -2.2, 0.0])


def rough_triangle_mark(vertices, position, scale):
    """A small hand-sketch-style triangle outline for the background
    'ancient survey marks' / beat-4 context triangles."""
    tri = Polygon(*[np.array(v) for v in vertices])
    tri.set_stroke(ANCIENT_INK, width=2.5, opacity=0.55)
    tri.scale(scale)
    tri.move_to(position)
    return tri


def rough_circle_mark(position, radius, opacity=0.5):
    """A rough compass-drawn circle with a small centre point, evoking
    ancient geometric construction (architecture / land measurement)."""
    circ = Circle(radius=radius)
    circ.set_stroke(ANCIENT_INK, width=2.5, opacity=opacity)
    circ.move_to(position)
    centre = Dot(np.array(position), radius=0.035)
    centre.set_color(ANCIENT_INK).set_opacity(opacity)
    return VGroup(circ, centre)


def rough_angle_mark(vertex, dir1_deg, dir2_deg, arm_length):
    """Two rays from a point with a small connecting arc -- a rough
    angle-sighting sketch, evoking star navigation. dir2_deg must be
    greater than dir1_deg."""
    vertex = np.array(vertex)
    d1, d2 = dir1_deg * DEGREES, dir2_deg * DEGREES
    arm1 = Line(vertex, vertex + arm_length * np.array([np.cos(d1), np.sin(d1), 0.0]))
    arm2 = Line(vertex, vertex + arm_length * np.array([np.cos(d2), np.sin(d2), 0.0]))
    arc = Arc(radius=arm_length * 0.4, start_angle=d1, angle=(d2 - d1), arc_center=vertex)
    mark = VGroup(arm1, arm2, arc)
    mark.set_stroke(ANCIENT_INK, width=2.5, opacity=0.55)
    return mark


def rough_square_mark(position, size, rotation_deg=0):
    """A simple rotated square outline -- basic geometric variety."""
    sq = Square(side_length=size)
    sq.rotate(rotation_deg * DEGREES)
    sq.set_stroke(ANCIENT_INK, width=2.5, opacity=0.5)
    sq.move_to(position)
    return sq


def square_on_segment(P, Q, outward_sign):
    """Returns the 4 corners of a square built outward from segment
    P->Q. outward_sign flips which perpendicular side counts as
    'outward' -- checked numerically against the actual triangle
    before use (see check_geometry.py)."""
    P, Q = np.array(P), np.array(Q)
    d = Q - P
    length = np.linalg.norm(d)
    u = d / length
    perp = np.array([-u[1], u[0], 0.0]) * outward_sign
    return [P, Q, Q + perp * length, P + perp * length]


def angle_arc_at(vertex, point1, point2, radius):
    """Small Arc marking the (non-reflex) interior angle at `vertex`
    between rays to point1 and point2. Self-corrects direction so it
    always returns the angle under 180 degrees, regardless of which
    point is passed first -- same helper as cosine_rule_statement.py."""
    vertex = np.array(vertex)
    v1 = np.array(point1) - vertex
    v2 = np.array(point2) - vertex
    a1 = np.arctan2(v1[1], v1[0])
    a2 = np.arctan2(v2[1], v2[0])
    diff = (a2 - a1) % TAU
    if diff > PI:
        a1, diff = a2, TAU - diff
    return Arc(radius=radius, start_angle=a1, angle=diff, arc_center=vertex)


class CosineRuleIntro(InteractiveScene):
    def construct(self):
        frame = self.frame

        backdrop = Rectangle(width=FRAME_WIDTH + 0.5, height=FRAME_HEIGHT + 0.5)
        backdrop.set_fill(BG_DARK, opacity=1).set_stroke(width=0)
        self.add(backdrop)

        # ============================================================
        # BEAT 1 (T=1 to T=16) -- "As long as 2000 BCE, different
        # civilizations were independently discovering a fundamental
        # geometric rule that we still use today. They needed this
        # idea to build architecture, measure land, and even navigate
        # using the stars."
        #
        # Background shapes now cover more mathematical variety
        # (triangles, compass circles, an angle-sighting mark, a
        # square) and are noticeably bigger. The angle-marks are held
        # back to a second wave so they land specifically on "navigate
        # using the stars" rather than appearing with everything else.
        # ============================================================
        date_label = Text("2000 BCE", font_size=34).set_color(ANCIENT_INK)
        date_label.to_corner(UL, buff=0.8)

        wave1 = VGroup(
            rough_triangle_mark([[-0.5, -0.35, 0], [0.5, -0.4, 0], [0.0, 0.5, 0]], [-5.7, 1.4, 0], 1.05),
            rough_triangle_mark([[-0.4, -0.3, 0], [0.45, -0.35, 0], [0.1, 0.45, 0]], [5.5, -2.1, 0], 0.95),
            rough_triangle_mark([[-0.35, -0.25, 0], [0.3, -0.3, 0], [-0.05, 0.35, 0]], [5.0, 2.5, 0], 0.75),
            rough_circle_mark([-5.2, -2.5, 0], radius=0.6),
            rough_circle_mark([6.3, 0.2, 0], radius=0.45),
            rough_square_mark([2.3, -3.2, 0], size=0.65, rotation_deg=12),
        )

        wave2 = VGroup(
            rough_angle_mark([-6.2, -0.6, 0], dir1_deg=20, dir2_deg=78, arm_length=0.9),
            rough_angle_mark([-2.0, 2.8, 0], dir1_deg=200, dir2_deg=258, arm_length=0.85),
        )

        base_line = Line([-2.8, -3.0, 0], [-0.4, -3.0, 0]).set_stroke(ANCIENT_INK, width=2, opacity=0.5)
        ticks = VGroup(*[
            Line([x, -3.0, 0], [x, -2.72, 0]).set_stroke(ANCIENT_INK, width=2, opacity=0.5)
            for x in [-2.4, -1.8, -1.2, -0.8]
        ])

        self.wait(1.0)                                             # T=1.0
        self.play(FadeIn(date_label), run_time=0.6)                # T=1.6
        self.play(LaggedStart(*[ShowCreation(m) for m in wave1], lag_ratio=0.15, run_time=6.9))   # T=8.5
        self.play(
            LaggedStart(*[ShowCreation(m) for m in wave2], lag_ratio=0.35, run_time=4.5),
            LaggedStart(ShowCreation(base_line), *[ShowCreation(t) for t in ticks], lag_ratio=0.2, run_time=3.5),
        )                                                           # T=13.0
        self.wait(1.0)                                              # T=14.0

        # The "hero" triangle, still rough/hand-drawn -- built as
        # THREE separate Line segments (not one closed Polygon) so
        # each one cleanly ReplacementTransforms into its own
        # correctly-coloured final side a moment later.
        P1 = np.array([-0.9, -0.75, 0.0])
        P2 = np.array([0.95, -0.65, 0.0])
        P3 = np.array([-0.55, 0.85, 0.0])
        rough_a = Line(P1, P2)
        rough_b = Line(P1, P3)
        rough_c = Line(P2, P3)
        rough_hero = VGroup(rough_a, rough_b, rough_c)
        rough_hero.set_stroke(ANCIENT_INK, width=3, opacity=0.85)

        self.play(ShowCreation(rough_hero), FadeOut(date_label), run_time=1.5)   # T=15.5 (~"So what was that idea?")
        self.wait(0.5)                                                            # T=16.0

        # ============================================================
        # "So what was that idea?" (T=16 to T=18) -- camera pushes in,
        # background marks clear away.
        # ============================================================
        self.play(
            frame.animate.set_height(4.0).move_to(rough_hero),
            FadeOut(wave1), FadeOut(wave2), FadeOut(ticks), FadeOut(base_line),
            run_time=2.0,
        )   # T=18.0

        # ============================================================
        # BEAT 2 (T=18 to T=23) -- "Take a right-angled triangle -- a
        # triangle with one 90-degree angle."
        # ============================================================
        leg_a = Line(V_RIGHT, V_A).set_stroke(LEG_A_COLOR, width=4)
        leg_b = Line(V_RIGHT, V_TOP).set_stroke(LEG_B_COLOR, width=4)
        hyp_c = Line(V_A, V_TOP).set_stroke(HYP_C_COLOR, width=4)

        self.play(
            ReplacementTransform(rough_a, leg_a),
            ReplacementTransform(rough_b, leg_b),
            ReplacementTransform(rough_c, hyp_c),
            frame.animate.to_default_state(),
            run_time=1.8,
        )   # T=19.8
        self.wait(0.2)   # T=20.0

        right_angle_marker = Square(side_length=0.22)
        right_angle_marker.move_to(V_RIGHT + np.array([0.11, 0.11, 0]))
        right_angle_marker.set_stroke(ANGLE_COLOR, width=2.5)
        angle_90_label = Text("90°", font_size=24).set_color(ANGLE_COLOR)
        angle_90_label.move_to(V_RIGHT + np.array([0.62, 0.55, 0]))

        self.play(ShowCreation(right_angle_marker), Write(angle_90_label), run_time=2.5)   # T=22.5
        self.wait(0.5)   # T=23.0

        # ============================================================
        # BEAT 3 (T=23 to T=33) -- "The rule we now know as Pythagoras
        # Theorem tells us that the square of the side opposite the
        # right angle is equal to the sum of the square of the other
        # two sides."
        #
        # Built in the SPOKEN order: the hypotenuse square ("the side
        # opposite the right angle") first, then the two leg squares
        # together ("the other two sides") -- reordered from a purely
        # visual-logic build to match narration. No standalone text
        # equation this time; the labelled squares carry the
        # relationship, and there's no time budget left for a second
        # reveal before "But Pythagoras..." begins.
        # ============================================================
        square_c = Polygon(*square_on_segment(V_A, V_TOP, outward_sign=-1))
        square_a = Polygon(*square_on_segment(V_RIGHT, V_A, outward_sign=-1))
        square_b = Polygon(*square_on_segment(V_RIGHT, V_TOP, outward_sign=1))
        for sq, col in [(square_a, LEG_A_COLOR), (square_b, LEG_B_COLOR), (square_c, HYP_C_COLOR)]:
            sq.set_stroke(col, width=2.5).set_fill(col, opacity=0.15)

        asq_label = Tex("a^2", font_size=40).set_color(LEG_A_COLOR).move_to(square_a.get_center())
        bsq_label = Tex("b^2", font_size=40).set_color(LEG_B_COLOR).move_to(square_b.get_center())
        csq_label = Tex("c^2", font_size=40).set_color(HYP_C_COLOR).move_to(square_c.get_center())

        self.wait(2.5)                                    # T=25.5  "...tells us that"
        self.play(ShowCreation(square_c), run_time=2.0)    # T=27.5  "the square"
        self.play(Write(csq_label), run_time=1.0)          # T=28.5  "of the side opposite the right angle"
        self.wait(0.5)                                     # T=29.0  "...is equal to"
        self.play(ShowCreation(square_a), ShowCreation(square_b), run_time=2.0)   # T=31.0  "the sum of the"
        self.play(Write(asq_label), Write(bsq_label), run_time=1.5)               # T=32.5  "square of the other two sides."
        self.wait(0.5)   # T=33.0

        # ============================================================
        # BEAT 4 (T=33 to T=42) -- "But Pythagoras' theorem only
        # applies to right-angled triangles, and in the real world, we
        # have plenty of triangles that don't have a 90-degree angle."
        # ============================================================
        self.play(
            FadeOut(square_a), FadeOut(square_b), FadeOut(square_c),
            FadeOut(asq_label), FadeOut(bsq_label), FadeOut(csq_label),
            FadeOut(right_angle_marker), FadeOut(angle_90_label),
            run_time=1.5,
        )   # T=34.5   "But Pythagoras' theorem only applies to right-angled triangles"

        new_leg_a = Line(V_RIGHT_NEW, V_A).set_stroke(LEG_A_COLOR, width=4)
        new_leg_b = Line(V_RIGHT_NEW, V_TOP).set_stroke(LEG_B_COLOR, width=4)
        self.play(
            ReplacementTransform(leg_a, new_leg_a),
            ReplacementTransform(leg_b, new_leg_b),
            run_time=2.0,
        )   # T=36.5   "and in the"
        leg_a, leg_b = new_leg_a, new_leg_b
        self.wait(0.5)   # T=37.0

        context_triangles = VGroup(
            rough_triangle_mark([[-0.4, -0.2, 0], [0.35, -0.35, 0], [0.05, 0.4, 0]], [-4.6, 2.0, 0], 0.6),
            rough_triangle_mark([[-0.3, -0.3, 0], [0.4, -0.25, 0], [0.1, 0.3, 0]], [4.4, 2.1, 0], 0.55),
            rough_triangle_mark([[-0.35, -0.25, 0], [0.3, -0.3, 0], [-0.1, 0.35, 0]], [4.5, -2.2, 0], 0.55),
        )
        for tri in context_triangles:
            tri.set_stroke(CONTEXT_GRAY, width=2, opacity=0.5)

        self.play(LaggedStart(*[FadeIn(t) for t in context_triangles], lag_ratio=0.3, run_time=3.5))
        # T=40.5   "real world, we have plenty of triangles that don't have a"
        self.wait(1.5)   # T=42.0

        # ============================================================
        # BEAT 5 (T=42 onward) -- "So is there any modified form of
        # Pythagoras' theorem that applies to any triangle?"
        # ============================================================
        self.play(FadeOut(context_triangles), run_time=1.0)   # T=43.0

        new_label_a = Tex("a", font_size=36).set_color(LEG_A_COLOR)
        new_label_a.move_to((V_RIGHT_NEW + V_A) / 2 + np.array([0.1, -0.35, 0]))
        new_label_b = Tex("b", font_size=36).set_color(LEG_B_COLOR)
        new_label_b.move_to((V_RIGHT_NEW + V_TOP) / 2 + np.array([-0.4, 0.0, 0]))
        new_label_c = Tex("c", font_size=36).set_color(HYP_C_COLOR)
        new_label_c.move_to((V_A + V_TOP) / 2 + np.array([0.35, 0.15, 0]))
        triangle_group = VGroup(leg_a, leg_b, hyp_c)

        self.play(Write(new_label_a), Write(new_label_b), Write(new_label_c), run_time=1.5)
        # T=44.5   "So is there any modified form of Pythagoras' theorem that"
        self.wait(0.5)   # T=45.0

        teaser = Tex("c^2", font_size=52).set_color(HYP_C_COLOR)
        teaser.next_to(triangle_group, RIGHT, buff=1.3)
        question = Text("?", font_size=64).set_color(LIGHT_TEXT)
        question.next_to(teaser, RIGHT, buff=0.5)

        self.play(Write(teaser), run_time=1.0)      # T=46.0
        self.play(FadeIn(question), run_time=0.6)   # T=46.6
        self.play(question.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.0)
        # T=47.6   "applies to any triangle?"
        self.wait(1.0)   # T=48.6 -- narration ends; visual settle begins

        everything = VGroup(triangle_group, new_label_a, new_label_b, new_label_c, teaser, question)
        self.play(frame.animate.set_height(6.5).move_to(everything), run_time=1.8)   # T=50.4
        self.wait(0.8)   # T=51.2

        # ============================================================
        # BEAT 6 -- "And yes, there is. It's called the cosine rule."
        #
        # The triangle is NOT faded here -- it persists continuously
        # into the rest of the scene (this used to be a separate
        # CosineRuleMotivation scene; it's merged in here specifically
        # so nothing has to be destroyed and rebuilt at the junction).
        # Only the "?" resolves into the name, and the backdrop
        # switches from the cinematic dark to the white background
        # used by the rest of the video -- the triangle and its a/b/c
        # labels carry straight through untouched.
        # ============================================================
        name_reveal = Text("The Cosine Rule", font_size=44).set_color(HYP_C_COLOR)
        name_reveal.move_to(question.get_center())

        self.play(
            ReplacementTransform(question, name_reveal),
            FadeOut(teaser),
            backdrop.animate.set_fill(WHITE, opacity=1),
            frame.animate.to_default_state(),
            run_time=1.8,
        )
        self.wait(0.3)
        self.play(name_reveal.animate.to_edge(UP, buff=0.6), run_time=1.0)
        self.wait(0.3)

        # ============================================================
        # "We already know that if the angle is 90 degrees, then
        # c^2 = a^2 + b^2. But what happens when we change this angle?
        # Clearly, length c changes. So we need some extra term that
        # tells us how much the angle changes this relationship."
        #
        # The exact same triangle continues -- now converted into a
        # ValueTracker-driven system so the angle can sweep smoothly.
        # V_RIGHT_NEW becomes the fixed angle-vertex; the two arm
        # lengths and the starting angle are computed directly from
        # its CURRENT distances to V_A and V_TOP, so the dynamic
        # system's initial render is pixel-identical to the static
        # triangle it replaces -- verified numerically before use
        # (reconstructed points matched V_A/V_TOP exactly, see
        # check_geometry.py). This is a genuinely different
        # parametrization from beat 4's deformation (there, V_A/V_TOP
        # were fixed and the vertex moved; here the vertex is fixed
        # and two constant-length arms rotate around it), since this
        # demo specifically needs sides a and b to stay fixed length
        # while only the angle between them changes.
        # ============================================================
        C_vertex = V_RIGHT_NEW
        arm1_vec = V_A - C_vertex
        arm2_vec = V_TOP - C_vertex
        LEN_ARM1 = np.linalg.norm(arm1_vec)
        LEN_ARM2 = np.linalg.norm(arm2_vec)
        dir1_0 = np.degrees(np.arctan2(arm1_vec[1], arm1_vec[0]))
        dir2_0 = np.degrees(np.arctan2(arm2_vec[1], arm2_vec[0]))
        bisector = (dir1_0 + dir2_0) / 2
        start_angle_value = dir2_0 - dir1_0   # ~60.5, matches beat 4's landing angle exactly

        angle_tracker = ValueTracker(start_angle_value)

        def far1():
            d = (bisector - angle_tracker.get_value() / 2) * DEGREES
            return C_vertex + LEN_ARM1 * np.array([np.cos(d), np.sin(d), 0.0])

        def far2():
            d = (bisector + angle_tracker.get_value() / 2) * DEGREES
            return C_vertex + LEN_ARM2 * np.array([np.cos(d), np.sin(d), 0.0])

        dyn_leg_a = always_redraw(lambda: Line(C_vertex, far1()).set_stroke(LEG_A_COLOR, width=4))
        dyn_leg_b = always_redraw(lambda: Line(C_vertex, far2()).set_stroke(LEG_B_COLOR, width=4))
        dyn_side_c = always_redraw(lambda: Line(far1(), far2()).set_stroke(HYP_C_COLOR, width=4))
        # same offsets as new_label_a/b/c above, so the swap below is exact
        dyn_label_a = always_redraw(lambda: Tex("a", font_size=36).set_color(LEG_A_COLOR).move_to(
            (C_vertex + far1()) / 2 + np.array([0.1, -0.35, 0.0])
        ))
        dyn_label_b = always_redraw(lambda: Tex("b", font_size=36).set_color(LEG_B_COLOR).move_to(
            (C_vertex + far2()) / 2 + np.array([-0.4, 0.0, 0.0])
        ))
        dyn_label_c = always_redraw(lambda: Tex("c", font_size=36).set_color(HYP_C_COLOR).move_to(
            (far1() + far2()) / 2 + np.array([0.35, 0.15, 0.0])
        ))
        angle_label = always_redraw(lambda: Tex(
            f"C = {angle_tracker.get_value():.0f}^\\circ", font_size=32
        ).set_color(ANGLE_COLOR).move_to(C_vertex + np.array([0.0, -0.55, 0.0])))

        # Instant, invisible swap -- remove() / add() by exact object
        # identity (not the triangle_group wrapper) so there's no
        # ambiguity about whether family-unpacking applies. The
        # dynamic system's current render exactly matches what's
        # already on screen, so this is a substitution, not a visible
        # transition.
        self.remove(leg_a, leg_b, hyp_c, new_label_a, new_label_b, new_label_c)
        self.add(dyn_leg_a, dyn_leg_b, dyn_side_c, dyn_label_a, dyn_label_b, dyn_label_c)

        self.play(Write(angle_label), run_time=0.8)
        self.wait(0.3)

        # "We already know that if the angle is 90 degrees..." --
        # settle the angle to exactly 90.
        self.play(angle_tracker.animate.set_value(90), run_time=1.8, rate_func=smooth)
        self.wait(0.3)

        # "...then c^2 = a^2 + b^2."
        pyth_recall = Tex(
            "c^2", "=", "a^2", "+", "b^2", font_size=44, fill_color=BLACK,
            tex_to_color_map={"c^2": HYP_C_COLOR, "a^2": LEG_A_COLOR, "b^2": LEG_B_COLOR},
        )
        pyth_recall.move_to(np.array([3.2, -0.3, 0.0]))
        self.play(Write(pyth_recall), run_time=1.5)
        self.wait(1.0)

        # "But what happens when we change this angle? Clearly, length
        # c changes." -- sweep on to 130; the recalled equation fades
        # since it's no longer true once C leaves 90, and side c
        # (already the one visibly stretching) is the whole point.
        self.play(
            angle_tracker.animate.set_value(130),
            FadeOut(pyth_recall),
            run_time=2.8, rate_func=smooth,
        )
        self.wait(0.5)

        # "So we need some extra term that tells us how much the angle
        # changes this relationship."
        bridge_text = Text("So we need some extra term...", font_size=36).set_color(QUESTION_COLOR)
        bridge_text.to_edge(DOWN, buff=0.9)
        self.play(Write(bridge_text))
        self.wait(1.5)

        # A live Arc reserved for angle C, inside the triangle,
        # updating continuously from here on -- introduced now since
        # this is where the angle starts actively changing again.
        dyn_angle_arc = always_redraw(
            lambda: angle_arc_at(C_vertex, far1(), far2(), radius=0.5).set_stroke(ANGLE_COLOR, width=2.5)
        )
        self.play(ShowCreation(dyn_angle_arc), FadeOut(bridge_text), run_time=1.2)
        self.wait(0.3)

        # ============================================================
        # "And for any triangle, that extra term is -2ab cos C."
        #
        # The full symbolic cosine rule appears for the first time in
        # this scene (it was only ever shown as plain "c^2=a^2+b^2"
        # before this point).
        # ============================================================
        full_eq = Tex(
            "c^2", "=", "a^2", "+", "b^2", "-", "2ab\\cos(C)", font_size=40, fill_color=BLACK,
            tex_to_color_map={
                "c^2": HYP_C_COLOR, "a^2": LEG_A_COLOR, "b^2": LEG_B_COLOR,
                "2ab\\cos(C)": CORRECTION_COLOR,
            },
        )
        full_eq.to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        self.play(Write(full_eq), run_time=1.8)
        self.wait(1.5)

        # ============================================================
        # "But how is the cosine term useful here? To understand this,
        # again imagine that the angle C is 90 degrees. If you plug in
        # cos 90 degrees, which is zero, the entire cosine term
        # disappears, and the equation is reduced to Pythagoras'
        # theorem."
        # ============================================================
        self.play(angle_tracker.animate.set_value(90), run_time=2.2, rate_func=smooth)
        self.wait(0.3)

        cos90_fact = Tex(
            "\\cos(90^\\circ)", "=", "0", font_size=34, fill_color=BLACK,
            tex_to_color_map={"0": ANGLE_COLOR},
        )
        cos90_fact.next_to(full_eq, DOWN, buff=0.5)
        self.play(Write(cos90_fact))
        self.wait(1.2)

        pyth_reduced = Tex(
            "c^2", "=", "a^2", "+", "b^2", font_size=40, fill_color=BLACK,
            tex_to_color_map={"c^2": HYP_C_COLOR, "a^2": LEG_A_COLOR, "b^2": LEG_B_COLOR},
        )
        pyth_reduced.move_to(full_eq)
        self.play(TransformMatchingTex(full_eq, pyth_reduced), FadeOut(cos90_fact), run_time=1.6)
        self.wait()

        pythag_box = SurroundingRectangle(pyth_reduced, buff=0.2).set_color("#0074FF")
        pythag_note = Text("Pythagoras' theorem", font_size=26).set_color("#0074FF")
        pythag_note.next_to(pythag_box, DOWN, buff=0.25)
        self.play(ShowCreation(pythag_box), Write(pythag_note))
        self.wait(1.5)

        # ============================================================
        # "But what happens when the angle becomes greater than 90
        # degrees? The cosine of an angle greater than 90 degrees is
        # negative. So, because we're subtracting a negative value,
        # the term 2ab cos C effectively gets added to a^2+b^2. This
        # makes sense, because as the angle gets larger, the side c
        # also becomes longer."
        # ============================================================
        self.play(FadeOut(pythag_box), FadeOut(pythag_note))

        full_eq2 = Tex(
            "c^2", "=", "a^2", "+", "b^2", "-", "2ab\\cos(C)", font_size=40, fill_color=BLACK,
            tex_to_color_map={
                "c^2": HYP_C_COLOR, "a^2": LEG_A_COLOR, "b^2": LEG_B_COLOR,
                "2ab\\cos(C)": CORRECTION_COLOR,
            },
        )
        full_eq2.move_to(pyth_reduced)
        self.play(TransformMatchingTex(pyth_reduced, full_eq2))
        self.wait(0.5)

        self.play(angle_tracker.animate.set_value(130), run_time=2.8, rate_func=smooth)
        self.wait()

        cos_gt90 = Tex(
            "\\cos(130^\\circ)", "\\approx", "-0.64", font_size=32, fill_color=BLACK,
            tex_to_color_map={"-0.64": ANGLE_COLOR},
        )
        cos_gt90.next_to(full_eq2, DOWN, buff=0.5)
        self.play(Write(cos_gt90))
        self.wait()

        full_eq2.save_state()
        flying_copy = cos_gt90["-0.64"].copy()
        target_064 = Tex("(0.64)", font_size=40).set_color(ANGLE_COLOR).move_to(full_eq2["\\cos(C)"])

        term_box_gt = SurroundingRectangle(VGroup(full_eq2["-"],full_eq2["2ab\\cos(C)"]), buff=0.1).set_color(CORRECTION_COLOR)
        minus_to_plus =Tex("+", font_size=40).set_color(ANGLE_COLOR).move_to(full_eq2["-"])
        added_note = Text("effectively added → c longer", font_size=26).set_color(CORRECTION_COLOR)
        added_note.next_to(cos_gt90, DOWN, buff=0.3)
        self.play(ShowCreation(term_box_gt), Write(added_note), ReplacementTransform(full_eq2["-"], minus_to_plus),
                  Transform(flying_copy, target_064),FadeOut(full_eq2["\\cos(C)"]))
        self.wait()

        c_flash1 = SurroundingRectangle(dyn_label_c, buff=0.15).set_color(HYP_C_COLOR)
        self.play(ShowCreation(c_flash1))
        self.wait()
        self.play(FadeOut(term_box_gt), FadeOut(c_flash1))
        self.wait(0.5)

        # ============================================================
        # "The opposite is also true. If we reduce the angle to less
        # than 90 degrees, the cosine becomes positive. So the cosine
        # term is subtracted from a^2+b^2, making c shorter than it
        # was at 90 degrees."
        # ============================================================
        # This speeds up the animation so it finishes completely halfway through
        def first_half(t):
            return smooth(min(t * 2, 1))

        # This keeps the animation at 0% until halfway, then finishes it
        def second_half(t):
            return smooth(max((t - 0.5) * 2, 0))

        # Now apply them directly to the animations
        self.play(
            # 1. Angle animates normally for the full 2.8 seconds
            angle_tracker.animate.set_value(50),
            
            # 2. These fades use "first_half", so they finish by 1.4s
            FadeOut(cos_gt90, rate_func=first_half),
            FadeOut(added_note, rate_func=first_half),
            FadeOut(flying_copy, rate_func=first_half),
            FadeOut(minus_to_plus, rate_func=first_half),
            
            # 3. Restore uses "second_half", so it waits 1.4s before starting
            Restore(full_eq2, rate_func=second_half),
            
            run_time=2.8
        )
        self.wait()

        cos_lt90 = Tex(
            "\\cos(50^\\circ)", "\\approx", "+0.64", font_size=32, fill_color=BLACK,
            tex_to_color_map={"+0.64": LEG_A_COLOR},
        )
        cos_lt90.next_to(full_eq2, DOWN, buff=0.5)
        self.play(Write(cos_lt90))
        self.wait()

        flying_copy2 = cos_gt90["0.64"].copy()
        target_064_2 = Tex("(0.64)", font_size=40).set_color(ANGLE_COLOR).move_to(full_eq2["\\cos(C)"])

        term_box_lt = SurroundingRectangle(full_eq2["2ab\\cos(C)"], buff=0.1).set_color(CORRECTION_COLOR)
        cosine_angle_soln2 = Tex("(0.64)", font_size = 40).set_color(ANGLE_COLOR).move_to(full_eq2["\\cos(C)"])
        subtracted_note = Text("subtracted → c shorter", font_size=26).set_color(CORRECTION_COLOR)
        subtracted_note.next_to(cos_lt90, DOWN, buff=0.3)
        self.play(ShowCreation(term_box_lt), Write(subtracted_note), Transform(flying_copy2, target_064_2),FadeOut(full_eq2["\\cos(C)"]))
        self.wait()

        c_flash2 = SurroundingRectangle(dyn_label_c, buff=0.15).set_color(HYP_C_COLOR)
        self.play(ShowCreation(c_flash2))
        self.wait(2)

        # ------------------------------------------------------------
        # End of scene.
        # ------------------------------------------------------------
        for m in (dyn_leg_a, dyn_leg_b, dyn_side_c, dyn_label_a, dyn_label_b, dyn_label_c,
                  angle_label, dyn_angle_arc):
            m.clear_updaters()

        self.play(
            FadeOut(dyn_leg_a), FadeOut(dyn_leg_b), FadeOut(dyn_side_c),
            FadeOut(dyn_label_a), FadeOut(dyn_label_b), FadeOut(dyn_label_c),
            FadeOut(angle_label), FadeOut(dyn_angle_arc),
            FadeOut(VGroup(*full_eq2[:-1])), FadeOut(cos_lt90), FadeOut(subtracted_note), FadeOut(c_flash2),
            FadeOut(name_reveal), FadeOut(term_box_lt), FadeOut(cosine_angle_soln2),
            FadeOut(flying_copy2),FadeOut(term_box_lt),
            run_time=1.5,
        )
        self.wait()


# ============================================================
#  STYLE CONSTANTS -- standard white "exam paper" background,
#  continuing the established palette. Colours here track ROLE
#  (known side / target side / given angle), matching the SAS/SSS
#  worked-example convention: whichever side you choose to solve for
#  becomes "a" and is coloured orange, regardless of which letter it
#  would have had elsewhere.
# ============================================================
KNOWN1_COLOR   = "#00B8A9"   # teal   -- first known side (8cm / b)
KNOWN2_COLOR   = "#7B2CBF"   # purple -- second known side (11cm / c)
TARGET_COLOR   = "#FF6B00"   # orange -- the side being solved for (a)
ANGLE_COLOR    = "#750A0A"   # red    -- the given angle (72deg / A)
CORRECTION_COLOR = "#FFB800" # gold   -- the -2bc cos A term
ANSWER_COLOR   = "#0074FF"   # blue   -- final boxed answer
SAS_EMPHASIS   = "#1E56C7"   # bright blue -- this example is SAS
SSS_DEEMPHASIS = "#B0B0B0"   # light grey  -- SSS, not this example
QUESTION_COLOR = "#8B0303"   # dark red -- rhetorical bridge lines
NEUTRAL_SIDE   = "#555555"   # dark grey -- unlabelled generic side

# Real SAS triangle, built directly from the example's own numbers
# (8cm, 11cm, 72 degrees) at a fixed scale -- verified numerically
# before use: the resulting third side works out to ~11.43 scene
# units-in-cm, matching the law-of-cosines answer of 11.4286 almost
# exactly, so the diagram is genuinely consistent with the arithmetic.
SCALE = 0.28
V_A = np.array([-0.3, 1.4, 0.0])     # the 72-degree vertex (angle A)
DIR_TO_C = 250                        # degrees, side b's direction
DIR_TO_B = DIR_TO_C + 72              # degrees, side c's direction
V_C = V_A + 8 * SCALE * np.array([np.cos(np.radians(DIR_TO_C)), np.sin(np.radians(DIR_TO_C)), 0.0])
V_B = V_A + 11 * SCALE * np.array([np.cos(np.radians(DIR_TO_B)), np.sin(np.radians(DIR_TO_B)), 0.0])

GENERIC_SHIFT = np.array([-4.2, 0.0, 0.0])   # where the SAS card sits before the transition


def label_at(text, position, color, font_size=34):
    return Tex(text, font_size=font_size, fill_color=color).move_to(np.array(position))


class CosineRuleExampleSAS(InteractiveScene):
    def construct(self):
        # grid = NumberPlane(
        #     axis_config={"stroke_color": GREY, "stroke_opacity": 0.3},
        #     background_line_style={"stroke_color": GREY, "stroke_width": 2, "stroke_opacity": 0.3},
        # )
        # self.add(grid)
        
        backdrop = Rectangle(width=FRAME_WIDTH + 0.5, height=FRAME_HEIGHT + 0.5)
        backdrop.set_fill(WHITE, opacity=1).set_stroke(width=0)
        self.add(backdrop)

        # ============================================================
        # "Alright, we have the cosine rule, but when to apply it to
        # our questions. There are two cases, first when two sides and
        # the angle between them are given, in other word SAS, or
        # second when all three sides are provided, SSS."
        # ============================================================
        GA, GB, GC = V_A + GENERIC_SHIFT, V_B + GENERIC_SHIFT, V_C + GENERIC_SHIFT

        sas_side_b = Line(GA, GC).set_stroke(KNOWN1_COLOR, width=4)
        sas_side_c = Line(GA, GB).set_stroke(KNOWN2_COLOR, width=4)
        sas_side_a = Line(GB, GC).set_stroke(NEUTRAL_SIDE, width=3)
        sas_arc = Arc(radius=0.4, start_angle=DIR_TO_C * DEGREES, angle=72 * DEGREES, arc_center=GA)
        sas_arc.set_stroke(ANGLE_COLOR, width=2.5)

        label_x = label_at("x", (GA + GC) / 2 + np.array([-0.35, 0.12, 0]), KNOWN1_COLOR)
        label_y = label_at("y", (GA + GB) / 2 + np.array([0.35, 0.12, 0]), KNOWN2_COLOR)
        label_theta = label_at("\\theta", GA + np.array([0.16, -0.57, 0]), ANGLE_COLOR, font_size=30)

        sas_heading = Text("SAS", font_size=40).set_color(BLACK)
        sas_heading.move_to(np.array([-3.95, 2.3, 0.0]))

        S1, S2, S3 = np.array([2.9, 1.3, 0.0]), np.array([5.3, -0.5, 0.0]), np.array([2.2, -0.8, 0.0])
        sss_side_1 = Line(S1, S2).set_stroke(KNOWN1_COLOR, width=4)
        sss_side_2 = Line(S2, S3).set_stroke(KNOWN2_COLOR, width=4)
        sss_side_3 = Line(S3, S1).set_stroke(TARGET_COLOR, width=4)
        label_p = label_at("p", (S1 + S2) / 2 + np.array([0.35, 0.05, 0]), KNOWN1_COLOR)
        label_q = label_at("q", (S2 + S3) / 2 + np.array([0.0, -0.35, 0]), KNOWN2_COLOR)
        label_r = label_at("r", (S3 + S1) / 2 + np.array([-0.35, 0.0, 0]), TARGET_COLOR)

        sss_heading = Text("SSS", font_size=40).set_color(BLACK)
        sss_heading.move_to(np.array([3.47, 2.3, 0.0]))

        sss_group = VGroup(sss_side_1, sss_side_2, sss_side_3, label_p, label_q, label_r)

        self.play(Write(sas_heading), ShowCreation(VGroup(sas_side_b, sas_side_c, sas_side_a)))
        self.play(ShowCreation(sas_arc), Write(label_x), Write(label_y), Write(label_theta))
        self.wait(0.5)
        self.play(Write(sss_heading), ShowCreation(VGroup(sss_side_1, sss_side_2, sss_side_3)))
        self.play(Write(label_p), Write(label_q), Write(label_r))
        self.wait(1.5)

        # ============================================================
        # "Let's start with an example. There is a triangle in which
        # one side is 8cm and the other is 11cm. The angle between
        # them is 72 degrees. And we are required to find the length
        # of the third side."
        #
        # SSS triangle is removed but its heading stays. Both headings
        # move to the top and recolour (SAS emphasised, SSS greyed
        # out), while the SAS triangle simultaneously shifts back to
        # centre and its arbitrary labels become the example's real
        # numbers.
        # ============================================================
        self.play(FadeOut(sss_group), run_time=0.8)

        real_label_8 = label_at("8", (V_A + V_C) / 2 + np.array([-0.35, 0.12, 0]), KNOWN1_COLOR)
        real_label_11 = label_at("11", (V_A + V_B) / 2 + np.array([0.35, 0.12, 0]), KNOWN2_COLOR)
        real_label_72 = label_at("72^\\circ", V_A + np.array([0.28, -0.57, 0]), ANGLE_COLOR, font_size=28)

        target_side = DashedLine(V_B, V_C, dash_length=0.12).set_stroke(TARGET_COLOR, width=4)
        target_q = Text("?", font_size=32).set_color(TARGET_COLOR)
        target_q.move_to((V_B + V_C) / 2 + np.array([0.0, -0.4, 0.0]))

        self.play(
            sas_heading.animate.move_to([-2.2, 3.3, 0]).set_color(SAS_EMPHASIS),
            sss_heading.animate.move_to([2.2, 3.3, 0]).set_color(SSS_DEEMPHASIS),
            sas_side_b.animate.shift(-GENERIC_SHIFT),
            sas_side_c.animate.shift(-GENERIC_SHIFT),
            sas_arc.animate.shift(-GENERIC_SHIFT),
            ReplacementTransform(label_x, real_label_8),
            ReplacementTransform(label_y, real_label_11),
            ReplacementTransform(label_theta, real_label_72),
            sas_side_a.animate.replace(target_side).set_opacity(0),
            FadeIn(target_side),
            FadeIn(target_q),
            run_time=2.2,
        )
        self.wait(1.5)
        self.remove(sas_side_a)   # remove the faded-out copy of the dashed line, leaving only the visible one
        # ============================================================
        # "Now in the formula sheet, the cosine rule is given as
        # a^2 = b^2 + c^2 - 2bc cos A."
        # ============================================================
        # We split the string into granular pieces so we can animate 
        # the variables (b, c, A) independently from the exponents/operators.
        sheet_eq = Tex(
            "a^2", "=", "b", "^2", "+", "c", "^2", "-", "2", "b", "c", "\\cos ", "A",
            font_size=42, fill_color=BLACK, tex_to_color_map={
             "a^2": TARGET_COLOR, "b": KNOWN1_COLOR, "^2" : BLACK, "c": KNOWN2_COLOR, "+" : BLACK, "-" : BLACK,
             "\\cos": CORRECTION_COLOR, "A": CORRECTION_COLOR,
             },
        )
            
        sheet_eq.move_to(np.array([0.5, -1.9, 0.0]))
        sheet_border = SurroundingRectangle(sheet_eq, buff=0.35).set_color(BLACK).set_stroke(width=1.5)
        sheet_label = Text("formula sheet", font_size=20).set_color(GREY)
        sheet_label.next_to(sheet_border, UP, buff=0.1).align_to(sheet_border, LEFT)

        self.play(ShowCreation(sheet_border), Write(sheet_label))
        self.play(Write(sheet_eq))
        self.wait(1.5)

        # ============================================================
        # "But wait, earlier we wrote the cosine rule using (c) on the
        # left-hand side. So why is it (a) here? Well, the letters
        # themselves don't really matter. What matters is how we label
        # the triangle."
        # ============================================================
        bridge1 = Text("Why (a), not (c)?", font_size=32).set_color(QUESTION_COLOR)
        bridge1.next_to(sheet_border, DOWN, buff=0.6)
        self.play(Write(bridge1))
        self.play(bridge1.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.2)
        self.wait(0.5)

        bridge2 = Text("It's about how YOU label the triangle", font_size=28).set_color(QUESTION_COLOR)
        bridge2.move_to(bridge1)
        self.play(ReplacementTransform(bridge1, bridge2))
        self.wait(1.5)
        self.play(FadeOut(bridge2))

        # ============================================================
        # "We choose the side we want to find and call it (a). The
        # angle opposite to it will then be (A). And the other two
        # sides become (b) and (c)."
        #
        # The diagram gets relabelled to match -- the target side's
        # "?" becomes "a", the 72-degree angle is confirmed as "A",
        # and the two known sides pick up "b" and "c" alongside their
        # numbers.
        # ============================================================
        label_a_diagram = label_at("a", (V_B + V_C) / 2 + np.array([0.0, -0.35, 0.0]), TARGET_COLOR)
        label_A_diagram = label_at("A", V_A + np.array([0.15, 0.2, 0.0]), ANGLE_COLOR, font_size=30)
        label_b_diagram = label_at("b", (V_A + V_C) / 2 + np.array([-0.35, -0.32, 0.0]), KNOWN1_COLOR, font_size=28)
        label_c_diagram = label_at("c", (V_A + V_B) / 2 + np.array([0.45, -0.15, 0.0]), KNOWN2_COLOR, font_size=28)

        self.play(ReplacementTransform(target_q, label_a_diagram))
        self.wait(0.3)
        self.play(FadeIn(label_A_diagram))
        self.wait(0.3)
        self.play(FadeIn(label_b_diagram), FadeIn(label_c_diagram))
        self.wait(1.5)

        # ============================================================
        # "Now we can simply substitute the values. Since b=8 and
        # c=11, we get: 8 squared + 11 squared - two times eight times
        # 11 times cos 72."
        # ============================================================
        # ============================================================
        # NEW FLYING SUBSTITUTION ANIMATION
        # ============================================================
        self.play(FadeOut(sheet_border), FadeOut(sheet_label))

        # 1. Define the substituted target structurally
        # Separating \cos completely from parentheses to avoid LaTeX compilation errors
        substituted_eq = Tex(
            "a^2", "=", "8", "^2", "+", "11", "^2", "-", 
            "2(", "8", ")(", "11", ")", "\\cos", "(", "72^\\circ", ")",
            font_size=38, fill_color=BLACK)

        # 2. Re-apply colors using exact indices so we don't break the string order
        # Indices: [2]=first 8, [5]=first 11, [9]=second 8, [11]=s")",econd 11, [13]=\cos, [15]=72
        substituted_eq[0].set_color(TARGET_COLOR)
        substituted_eq[3].set_color(KNOWN1_COLOR)
        substituted_eq[6:8].set_color(KNOWN2_COLOR)
        
        # Color the correction part
        substituted_eq[12].set_color(KNOWN1_COLOR)        # Inside parens: 8
        substituted_eq[15:17].set_color(KNOWN2_COLOR)       # Inside parens: 11
        substituted_eq[18:21].set_color(CORRECTION_COLOR)   # \cos
        substituted_eq[22:25].set_color(ANGLE_COLOR)   # 72^\circ

        substituted_eq.move_to(sheet_eq)

        # 3. Make copies of the diagram labels to act as the "flying objects"
        copy_8_1 = real_label_8.copy()
        copy_8_2 = real_label_8.copy()
        copy_11_1 = real_label_11.copy()
        copy_11_2 = real_label_11.copy()
        copy_72 = real_label_72.copy()

        #4. Animate the complex structural replacement
        self.play(
            # Base equation structure shifting into new places
            ReplacementTransform(sheet_eq[0], substituted_eq[0]),
            ReplacementTransform(sheet_eq[1], substituted_eq[1]),
            ReplacementTransform(sheet_eq[2], substituted_eq[2]),
            ReplacementTransform(sheet_eq[4], substituted_eq[4]),  # First ^2
            ReplacementTransform(sheet_eq[5], substituted_eq[5]),
            ReplacementTransform(sheet_eq[7], substituted_eq[8]),  # Second ^2
            ReplacementTransform(sheet_eq[8], substituted_eq[9]),

            
            # The structure of the 2bc cos A term (parens fading in)
            ReplacementTransform(sheet_eq[9], substituted_eq[10:12]),   # "2" -> "2("
            ReplacementTransform(sheet_eq[12:15], substituted_eq[18:21]), # "\cos" -> "\cos"
            FadeIn(substituted_eq[13:15], shift=UP*0.2),               # ")("
            FadeIn(substituted_eq[17], shift=UP*0.2),               # ")"
            FadeIn(substituted_eq[21], shift=UP*0.2),               # "("
            FadeIn(substituted_eq[25], shift=UP*0.2),               # "("
            
            # The old variables (b, c, b, c, A) visually drop down and fade away
            FadeOut(sheet_eq[3], shift=DOWN*0.5),
            FadeOut(sheet_eq[6], shift=DOWN*0.5),
            FadeOut(sheet_eq[10], shift=DOWN*0.5),
            FadeOut(sheet_eq[11], shift=DOWN*0.5),
            FadeOut(sheet_eq[15], shift=DOWN*0.5),
        
            
            # The diagram copies FLY into the empty spaces left behind!
            # Since the destination slots are mapped to CORRECTION_COLOR, 
            # they will smoothly morph to gold as they land.
            ReplacementTransform(copy_8_1, substituted_eq[3]),
            ReplacementTransform(copy_8_2, substituted_eq[12]),
            ReplacementTransform(copy_11_1, substituted_eq[6:8]),
            ReplacementTransform(copy_11_2, substituted_eq[15:17]),
            ReplacementTransform(copy_72, substituted_eq[22:25]),
            
            run_time=2.5
        )
        self.wait(1.5)
        
        # Ensure the final object is properly registered to the scene graph
        self.add(substituted_eq)
        self.wait(1.5)
        # ============================================================
        # "Calculating each part gives us 64, 121, and the cosine term
        # gives us 54.39."
        # ============================================================
        calculated_eq = Tex(
            "a^2", "=", "64", "+", "121", "-", "54.39", font_size=38, fill_color=BLACK,
            tex_to_color_map={
                "a^2": TARGET_COLOR, "64": KNOWN1_COLOR, "121": KNOWN2_COLOR, "54.39": CORRECTION_COLOR,
            },
        )
        calculated_eq.move_to(substituted_eq)
        self.play(ReplacementTransform(substituted_eq[0], calculated_eq[0]), 
                  ReplacementTransform(substituted_eq[1], calculated_eq[1]), 
                  ReplacementTransform(substituted_eq[2], calculated_eq[2]), 
                  ReplacementTransform(substituted_eq[3:5], calculated_eq[3:5]), 
                  ReplacementTransform(substituted_eq[5], calculated_eq[5]), 
                  ReplacementTransform(substituted_eq[6:9], calculated_eq[6:9]), 
                  ReplacementTransform(substituted_eq[9], calculated_eq[9]), 
                  ReplacementTransform(substituted_eq[10:26], calculated_eq[10:16]), 
                  run_time=1.8)
        self.wait(1.5)

        # ============================================================
        # "Which on further resolving gives us 130.61."
        # ============================================================
        resolved_eq = Tex(
            "a^2", "= ", "130.61", font_size=38, fill_color=BLACK,
            tex_to_color_map={"a^2": TARGET_COLOR},
        )
        resolved_eq.move_to(calculated_eq)
        self.play(ReplacementTransform(calculated_eq[0], resolved_eq[0]),
                  ReplacementTransform(calculated_eq[1], resolved_eq[1]),
                  ReplacementTransform(calculated_eq[2], resolved_eq[2]),
            ReplacementTransform(calculated_eq[3:16], resolved_eq[3:9]), 
                  run_time=1.4)
        self.wait(1.5)

        # ============================================================
        # "And since we want to find a, we take the square root of
        # both sides. So, a = root of 130.61, approximately 11.42."
        #
        # A genuinely new step (not a further simplification of the
        # same statement) -- built as a fresh equation with its own
        # "=" rather than transforming resolved_eq in place. The "√"
        # appearing is itself the visual cue for "square root both
        # sides", so no separate annotation is needed.
        # ============================================================
        final_eq = Tex(
            "a", "=", "\\sqrt{130.61}", "\\approx", "11.42", font_size=40, fill_color=BLACK,
            tex_to_color_map={"a": TARGET_COLOR, "11.42": TARGET_COLOR},
        )
        final_eq.next_to(resolved_eq, DOWN, buff=0.5)
        self.play(Write(final_eq), run_time=1.6)
        self.wait(1.5)

        # ============================================================
        # "Therefore, the length of the third side is approximately
        # 11.42 centimetres."
        #
        # The answer returns to the diagram rather than continuing to
        # stack further down the page.
        # ============================================================
        answer_box = SurroundingRectangle(final_eq["11.42"], buff=0.12).set_color(ANSWER_COLOR)
        answer_text = final_eq["11.42"].scale(0.8).copy()

        self.play(ShowCreation(answer_box))
        self.play(answer_text.animate.next_to(label_a_diagram, RIGHT, buff = 0.4))
        self.wait(2)
        self.play(FadeOut(answer_box), FadeOut(answer_text), FadeOut(final_eq), FadeOut(resolved_eq), FadeOut(calculated_eq), 
                  FadeOut(substituted_eq), FadeOut(real_label_8), FadeOut(real_label_11), FadeOut(real_label_72), 
                  FadeOut(label_A_diagram), FadeOut(label_b_diagram), FadeOut(label_c_diagram),FadeOut(sas_side_b),
                  FadeOut(sas_side_c), FadeOut(sas_arc), FadeOut(target_side), FadeOut(label_a_diagram))