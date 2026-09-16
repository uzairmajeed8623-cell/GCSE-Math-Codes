import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manimlib import *
from sector_common import (
    INK, BODY_FONT, ANGLE_A, ANGLE_B, REFLEX_SWEEP,
    build_border, build_question_text, build_diagram, lay_out_side_by_side,
    content_width_for, build_header
)

# ------------------------------------------------------------------
# Portrait solution walkthrough for the OAB sector question, covering
# the script from "First of all, we need to clarify which angle..."
# through to the sector-area fraction at the end.
# ------------------------------------------------------------------

HIGHLIGHT_COLOR = "#EF4444"
REFLEX_COLOR = "#3B82F6"
OUTSIDE_COLOR = "#F97316"
PERIMETER_COLOR = "#22C55E"
ARC_TEAL_COLOR = "#06B6D4"
AREA_COLOR = "#A855F7"


class SectorSolutionPortrait(InteractiveScene):
    samples = 16

    def construct(self):
        self.set_background_color(WHITE)

        border = build_border()
        header = build_header(border)
        qt = build_question_text()
        dg = build_diagram()
        lay_out_side_by_side(qt.group, dg.group, border)
        self.add(border, header, qt.group, dg.group)

        O = dg.dot_O.get_center()
        A = dg.dot_A.get_center()
        B = dg.dot_B.get_center()
        r = dg.sector_arc.get_width() / 2

        reflex_mid_angle = ANGLE_A + REFLEX_SWEEP / 2
        minor_mid_angle = (ANGLE_A + ANGLE_B) / 2

        indicator_r = r * 0.22
        reflex_arc = Arc(arc_center=O, radius=indicator_r, start_angle=ANGLE_A,
                          angle=REFLEX_SWEEP, color=REFLEX_COLOR, stroke_width=3)
        outside_arc = Arc(arc_center=O, radius=indicator_r, start_angle=ANGLE_B,
                           angle=(ANGLE_A - ANGLE_B), color="#F53142", stroke_width=3)

        self.play(ShowCreation(reflex_arc))
        self.play(ShowCreation(outside_arc))
        self.wait()

        reflex_word = qt.find_line2[0:6]
        highlight_box = SurroundingRectangle(reflex_word, color=HIGHLIGHT_COLOR,
                                              buff=0.04, stroke_width=2)
        self.play(ShowCreation(highlight_box))
        self.wait()

        demo_center = np.array([0.0, -1.8, 0.0])
        ray_len = 1.15
        angle_tracker = ValueTracker(180)

        ray1 = Line(demo_center, demo_center + ray_len * LEFT,
                    stroke_color=INK, stroke_width=3)

        def get_ray2():
            theta = angle_tracker.get_value() - 180
            direction = np.array([np.cos(theta * DEGREES), np.sin(theta * DEGREES), 0.0])
            return Line(demo_center, demo_center + ray_len * direction,
                        stroke_color=INK, stroke_width=3)

        def get_demo_arc():
            theta = angle_tracker.get_value()
            return Arc(arc_center=demo_center, radius=0.5, start_angle=180 * DEGREES,
                       angle=theta * DEGREES, color=REFLEX_COLOR, stroke_width=3)

        def get_angle_label():
            val = angle_tracker.get_value()
            label = Text(f"{val:.0f}\u00b0", font=BODY_FONT, font_size=26).set_color(REFLEX_COLOR)
            label.move_to(demo_center + UP * 1.55)
            return label

        ray2 = always_redraw(get_ray2)
        demo_arc = always_redraw(get_demo_arc)
        angle_label = always_redraw(get_angle_label)
        demo_vertex = Dot(demo_center, radius=0.04).set_color(INK)

        self.play(FadeIn(ray1), FadeIn(ray2), FadeIn(demo_vertex),
                   FadeIn(demo_arc), FadeIn(angle_label), run_time=1.5)
        self.play(angle_tracker.animate.set_value(300), run_time=2.5, rate_func=linear)
        self.wait()

        self.play(FadeOut(outside_arc))
        self.wait()

        ray2.clear_updaters()
        demo_arc.clear_updaters()
        angle_label.clear_updaters()
        self.play(FadeOut(VGroup(ray1, ray2, demo_arc, angle_label, demo_vertex, highlight_box)))
        self.wait()

        num_343 = qt.perimeter_line2[12:17]
        perimeter_box = SurroundingRectangle(num_343, color=PERIMETER_COLOR,
                                              buff=0.08, stroke_width=2)
        self.play(ShowCreation(perimeter_box))
        self.wait()

        arc_length_arc = Arc(arc_center=O, radius=r * 1.08, start_angle=ANGLE_A,
                              angle=REFLEX_SWEEP, color=ARC_TEAL_COLOR, stroke_width=3)
        arc_length_arc.add_tip(length=0.13, width=0.09)
        arc_length_arc.shift(O - arc_length_arc.get_arc_center())

        perim_OA = Line(O, A, color=PERIMETER_COLOR, stroke_width=2)
        perim_OB = Line(O, B, color=PERIMETER_COLOR, stroke_width=2)
        perim_arc = Arc(arc_center=O, radius=r, start_angle=ANGLE_A,
                         angle=REFLEX_SWEEP, color=PERIMETER_COLOR, stroke_width=2)

        perimeter_label = Text("34.3", font=BODY_FONT, font_size=16).set_color(PERIMETER_COLOR)
        perimeter_label.move_to(
            O + (r * 0.55) * np.array([np.cos(minor_mid_angle), np.sin(minor_mid_angle), 0.0])
        )

        self.play(
            ShowCreation(arc_length_arc),
            rate_func=linear
        )
        self.wait()
        self.play(ShowCreation(perim_arc), ShowCreation(perim_OA), ShowCreation(perim_OB),
                    Write(perimeter_label), run_time=2)
        self.wait()

        eq_343 = Text("34.3", font=BODY_FONT, font_size=30).set_color(PERIMETER_COLOR)
        minus1 = Text("-", font=BODY_FONT, font_size=30).set_color(INK)
        eq_47a = Text("4.7", font=BODY_FONT, font_size=30).set_color(INK)
        minus2 = Text("-", font=BODY_FONT, font_size=30).set_color(INK)
        eq_47b = Text("4.7", font=BODY_FONT, font_size=30).set_color(INK)
        equals1 = Text("=", font=BODY_FONT, font_size=30).set_color(INK)

        equation_row1 = VGroup(eq_343, minus1, eq_47a, minus2, eq_47b, equals1).arrange(
            RIGHT, buff=0.12
        )
        equation_row1.move_to(np.array([-0.4, -1.6, 0.0]))

        self.play(ReplacementTransform(perimeter_label, eq_343))
        self.wait(0.3)
        self.play(
            TransformFromCopy(dg.radius_label, eq_47a),
            TransformFromCopy(dg.radius_label, eq_47b),
            Write(minus1), Write(minus2), Write(equals1),
        )
        self.wait()

        self.play(FadeOut(perim_OA), FadeOut(perim_OB), FadeOut(arc_length_arc))
        self.wait()

        eq_249 = Text("24.9 m", font=BODY_FONT, font_size=30).set_color(PERIMETER_COLOR)
        eq_249.next_to(equals1, RIGHT, buff=0.14)

        arc_value_label = Text("24.9 m", font=BODY_FONT, font_size=20).set_color(PERIMETER_COLOR)
        arc_value_label.move_to(
            O + (r * 1.18) * np.array([np.cos(reflex_mid_angle), np.sin(reflex_mid_angle), 0.0])
        )
        arc_value_label.shift(DOWN * 0.12)

        self.play(Write(eq_249), Write(arc_value_label))
        self.wait()

        equation_group = VGroup(equation_row1, eq_249)
        self.play(FadeOut(equation_group))
        self.wait()

        missing_arc = Arc(arc_center=O, radius=r, start_angle=ANGLE_B,
                           angle=(ANGLE_A - ANGLE_B), color=INK, stroke_width=1.5)
        self.play(perim_arc.animate.set_color(INK), ShowCreation(missing_arc))
        small_circle = Circle(radius=r * 0.34, stroke_color=INK, stroke_width=1.5)
        small_circle.move_to(O)
        self.wait()

        FRACTION_FONT = 22

        area_num = Text("sector area", font=BODY_FONT, font_size=FRACTION_FONT).set_color(AREA_COLOR)
        area_bar = Line(LEFT * 0.5, RIGHT * 0.5, stroke_color=INK, stroke_width=2)
        area_den = Text("\u03c0r\u00b2", font=BODY_FONT, font_size=FRACTION_FONT).set_color(INK)
        area_fraction = VGroup(area_num, area_bar, area_den).arrange(DOWN, buff=0.06)

        equals_left = Text("=", font=BODY_FONT, font_size=22).set_color(INK)

        angle_num = Text("angle AOB", font=BODY_FONT, font_size=FRACTION_FONT).set_color(REFLEX_COLOR)
        angle_bar = Line(LEFT * 0.45, RIGHT * 0.45, stroke_color=INK, stroke_width=2)
        angle_den = Text("360\u00b0", font=BODY_FONT, font_size=FRACTION_FONT).set_color(INK)
        angle_fraction = VGroup(angle_num, angle_bar, angle_den).arrange(DOWN, buff=0.06)

        equals_right = Text("=", font=BODY_FONT, font_size=22).set_color(INK)

        arc_num = Text("arc length", font=BODY_FONT, font_size=FRACTION_FONT).set_color(PERIMETER_COLOR)
        arc_bar = Line(LEFT * 0.5, RIGHT * 0.5, stroke_color=INK, stroke_width=2)
        arc_den = Text("2\u03c0r", font=BODY_FONT, font_size=FRACTION_FONT).set_color(INK)
        arc_fraction = VGroup(arc_num, arc_bar, arc_den).arrange(DOWN, buff=0.06)

        full_equation = VGroup(
            area_fraction, equals_left, angle_fraction, equals_right, arc_fraction
        ).arrange(RIGHT, buff=0.16)
        full_equation.set_max_width(content_width_for(border))
        full_equation.move_to(np.array([0.0, -1.9, 0.0]))

        self.play(ShowCreation(small_circle), Write(angle_fraction))
        self.wait()
        self.play(Write(equals_right), Write(arc_fraction))
        self.wait()
        self.play(Write(equals_left), Write(area_fraction))
        self.wait(2)

        NEW_FRACTION_FONT = FRACTION_FONT

        angle_fraction_v2 = VGroup(
            Text("angle AOB", font=BODY_FONT, font_size=NEW_FRACTION_FONT).set_color(REFLEX_COLOR),
            Line(LEFT * 0.55, RIGHT * 0.55, stroke_color=INK, stroke_width=2),
            Text("360\u00b0", font=BODY_FONT, font_size=NEW_FRACTION_FONT).set_color(INK),
        ).arrange(DOWN, buff=0.08)

        equals_right_v2 = Text("=", font=BODY_FONT, font_size=28).set_color(INK)

        value_249 = Text("24.9 m", font=BODY_FONT, font_size=NEW_FRACTION_FONT).set_color(PERIMETER_COLOR)
        right_bar_v2 = Line(LEFT * 0.6, RIGHT * 0.6, stroke_color=INK, stroke_width=2)
        right_den_v2 = Text("2\u03c0r", font=BODY_FONT, font_size=NEW_FRACTION_FONT).set_color(INK)
        right_fraction_v2 = VGroup(value_249, right_bar_v2, right_den_v2).arrange(DOWN, buff=0.08)

        remaining_eq_v2 = VGroup(angle_fraction_v2, equals_right_v2, right_fraction_v2).arrange(
            RIGHT, buff=0.22
        )
        remaining_eq_v2.set_max_width(content_width_for(border))
        remaining_eq_v2.move_to(np.array([0.0, -1.9, 0.0]))

        self.play(
            FadeOut(area_fraction), FadeOut(equals_left),
            Transform(angle_fraction, angle_fraction_v2),
            Transform(equals_right, equals_right_v2),
            ReplacementTransform(arc_num, value_249),
            Transform(arc_bar, right_bar_v2),
            Transform(arc_den, right_den_v2),
        )
        self.wait()

        den_with_r_value = Text("2\u03c0(4.7)", font=BODY_FONT,
                                 font_size=NEW_FRACTION_FONT).set_color(INK)
        den_with_r_value.move_to(arc_den.get_center())
        self.play(Transform(arc_den, den_with_r_value))
        self.wait()

        den_evaluated = Text("29.53 m", font=BODY_FONT,
                              font_size=NEW_FRACTION_FONT).set_color(INK)
        den_evaluated.move_to(arc_den.get_center())
        self.play(Transform(arc_den, den_evaluated))
        self.wait()

        right_fraction_group = VGroup(value_249, arc_bar, arc_den)
        value_08432 = Text("0.8432", font=BODY_FONT, font_size=NEW_FRACTION_FONT).set_color(INK)
        value_08432.move_to(right_fraction_group.get_center())
        self.play(ReplacementTransform(right_fraction_group, value_08432))
        self.wait()

        # ==================================================================
        # STEP 12 - "multiply both sides by 360 to get angle AOB on its
        # own" - "360 x" appears to the left, centred on the dividing bar;
        # "x 360" appears to the right of 0.8432.
        #
        # Adding these two terms widens the row past its STEP-9 fit, and
        # since angle_fraction / equals_right / value_08432 are already
        # sitting at the edges of the content width, that overflow lands
        # squarely on the border. Fix: give the multiplier terms their
        # own smaller font (they're an annotation, not core equation), then
        # measure the combined row width and — only if it still doesn't
        # fit — shrink the existing fraction and the multiplier terms by
        # the SAME factor together. A single shared scale keeps font size
        # and the gap to the central "=" shrinking in proportion, and
        # guarantees the row fits rather than relying on guessed values.
        # ==================================================================
        MULT_FONT = NEW_FRACTION_FONT - 6
        MULT_BUFF = 0.1

        mult_left = Text("360 \u00d7", font=BODY_FONT, font_size=MULT_FONT).set_color(INK)
        mult_right = Text("\u00d7 360", font=BODY_FONT, font_size=MULT_FONT).set_color(INK)

        existing_eq = VGroup(angle_fraction, equals_right, value_08432)
        safe_width = content_width_for(border) * 0.92  # small margin, not flush to the border
        projected_width = (
            mult_left.get_width() + MULT_BUFF
            + existing_eq.get_width() + MULT_BUFF
            + mult_right.get_width()
        )
        mult_scale = min(1.0, safe_width / projected_width)

        if mult_scale < 1.0:
            existing_center = existing_eq.get_center()
            self.play(existing_eq.animate.scale(mult_scale).move_to(existing_center))
            mult_left.scale(mult_scale)
            mult_right.scale(mult_scale)
            self.wait(0.2)

        mult_left.next_to(angle_fraction, LEFT, buff=MULT_BUFF)
        mult_left.set_y(angle_bar.get_y())
        mult_right.next_to(value_08432, RIGHT, buff=MULT_BUFF)

        self.play(Write(mult_left), Write(mult_right))
        self.wait()

        value_30355 = Text("303.55\u00b0", font=BODY_FONT,
                            font_size=round(NEW_FRACTION_FONT * mult_scale)).set_color(INK)
        value_30355.move_to(VGroup(value_08432, mult_right).get_center())

        self.play(
            FadeOut(mult_left), FadeOut(angle_bar), FadeOut(angle_den),
            angle_num.animate.set_y(equals_right.get_y()),
            ReplacementTransform(VGroup(value_08432, mult_right), value_30355),
        )
        self.wait()

        value_304 = Text("304\u00b0", font=BODY_FONT,
                          font_size=round((NEW_FRACTION_FONT + 6) * mult_scale)).set_color(REFLEX_COLOR)
        value_304.move_to(value_30355.get_center())
        self.play(Transform(value_30355, value_304))
        self.wait(2)