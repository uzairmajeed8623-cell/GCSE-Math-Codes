from manimlib import *

# ------------------------------------------------------------------
# Part 1 of the OBCD solving video (landscape, 16:9).
#
# Picks up the same question card built in obcd_question.py, then
# walks through the opening beats of the script:
#   1. question recap / build
#   2. highlight OBCD, then DCE
#   3. copy B's and E's coordinates out next to their points
#   4. highlight D permanently
#   5. highlight OD and DE (the two lines that meet at D)
#   6. fade that highlight
#   7. generic "simultaneous equations" reminder illustration (grey)
#   8. re-highlight DE, introduce y = mx + c
#   9. gradient formula y2-y1 / x2-x1
#  10. highlight DE and OB together (parallel-lines observation)
#
# Worked answer (comment only, never shown on screen): D = (7, 3.5).
# ------------------------------------------------------------------


def line_intersection(p1, p2, q1, q2):
    """Exact intersection of line p1-p2 with line q1-q2 (2D, z ignored)."""
    p1, p2, q1, q2 = [np.array(pt[:2]) for pt in (p1, p2, q1, q2)]
    d1 = p2 - p1
    d2 = q2 - q1
    denom = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((q1[0] - p1[0]) * d2[1] - (q1[1] - p1[1]) * d2[0]) / denom
    point = p1 + t * d1
    return np.array([point[0], point[1], 0.0])


class ObcdRectangleSolutionPart1(InteractiveScene):
    samples = 16

    def construct(self):
        self.set_background_color(WHITE)

        ink = BLACK
        margin_color = GREY_B
        body_font = "Times New Roman"

        # Palette - bright/saturated so it pops against white (the
        # cream-background set from earlier videos reads as muted here)
        teal_obcd = "#00B8A9"       # rectangle OBCD identity (vivid teal)
        terracotta_de = "#E63946"   # line DE identity (vivid red, stays consistent)
        blue_od = "#0074FF"         # line OD identity (vivid blue)
        amber_d = "#FF6B00"         # point D - permanent highlight (vivid orange)
        green_ob = "#00C853"        # line OB identity (vivid green)
        grey_illustration = "#AAAAAA"
        m_color = "#7B2CBF"         # vivid purple
        c_color = "#FFB800"         # vivid gold

        # ============================================================
        # 1. QUESTION CARD (same visual language as obcd_question.py,
        #    but the rectangle is built from 4 separate Line objects
        #    instead of one Polygon, so each side can be highlighted
        #    independently later on).
        # ============================================================
        left_ticks = VGroup(*[
            Line(np.array([-7.05, y, 0]), np.array([-6.8, y, 0]),
                 stroke_color=margin_color, stroke_width=1.5)
            for y in np.linspace(3.7, -3.7, 24)
        ])
        right_margin_line = Line(
            np.array([6.3, 3.75, 0]), np.array([6.3, -3.75, 0]),
            stroke_color=margin_color, stroke_width=1.5
        )
        right_margin_tick = Line(
            np.array([6.15, 3.8, 0]), np.array([6.45, 3.8, 0]),
            stroke_color=margin_color, stroke_width=1.5
        )
        margin_marks = VGroup(left_ticks, right_margin_line, right_margin_tick)
        self.add(margin_marks)

        q_number = Text("16", font=body_font, weight=BOLD, font_size=34).set_color(ink)
        line1_body = Text("OBCD is a rectangle.", font=body_font,
                           slant=ITALIC, font_size=34).set_color(ink)
        line1 = VGroup(q_number, line1_body).arrange(RIGHT, buff=0.18)
        line2 = Text("DCE is a straight line.", font=body_font,
                      slant=ITALIC, font_size=34).set_color(ink)
        line2.next_to(line1_body, DOWN, buff=0.2, aligned_edge=LEFT)
        header = VGroup(line1, line2)
        header.to_corner(UL, buff=1.0)

        b_prefix = Text("B has coordinates ", font=body_font,
                         slant=ITALIC, font_size=34).set_color(ink)
        b_coords_only = Text("(2, \u22124)", font=body_font,
                              slant=ITALIC, font_size=34).set_color(ink)
        b_coord_text = VGroup(b_prefix, b_coords_only).arrange(RIGHT, buff=0.06)

        e_prefix = Text("E has coordinates ", font=body_font,
                         slant=ITALIC, font_size=34).set_color(ink)
        e_coords_only = Text("(12, \u22126.5)", font=body_font,
                              slant=ITALIC, font_size=34).set_color(ink)
        e_coord_text = VGroup(e_prefix, e_coords_only).arrange(RIGHT, buff=0.06)

        coords_block = VGroup(b_coord_text, e_coord_text).arrange(
            DOWN, buff=0.22, aligned_edge=LEFT
        )

        work_out_text = Text("Work out the coordinates of D.", font=body_font,
                              slant=ITALIC, font_size=34).set_color(ink)
        show_working_text = Text("You must show all your working.", font=body_font,
                                  slant=ITALIC, font_size=34).set_color(ink)
        instruction_block = VGroup(work_out_text, show_working_text).arrange(
            DOWN, buff=0.22, aligned_edge=LEFT
        )

        footer = VGroup(coords_block, instruction_block).arrange(
            DOWN, buff=0.55, aligned_edge=LEFT
        )
        footer.to_corner(DL, buff=1.0)

        # ---- Diagram: axes + rectangle sides + DCE line ----
        SCALE = 0.5

        def P(x, y):
            return np.array([x, y, 0.0]) * SCALE

        O = P(0, 0)
        B = P(2, -4)
        C = P(9, -0.5)
        D = P(7, 3.5)
        E = P(12, -6.5)

        x_axis = Line(P(-1.4, 0), P(10.3, 0), stroke_color=ink, stroke_width=2.5)
        x_axis.add_tip(length=0.22, width=0.13)
        y_axis = Line(P(0, -1.3), P(0, 4.6), stroke_color=ink, stroke_width=2.5)
        y_axis.add_tip(length=0.22, width=0.13)
        axes = VGroup(x_axis, y_axis)

        x_label = Tex("x", font_size=32).set_color(ink)
        x_label.next_to(x_axis.get_end(), RIGHT, buff=0.12).shift(DOWN * 0.06)
        y_label = Tex("y", font_size=32).set_color(ink)
        y_label.next_to(y_axis.get_end(), UP, buff=0.08).shift(RIGHT * 0.08)

        # Rectangle sides as separate Lines (each independently highlightable)
        line_OB = Line(O, B, stroke_color=ink, stroke_width=3)
        line_BC = Line(B, C, stroke_color=ink, stroke_width=3)
        line_CD = Line(C, D, stroke_color=ink, stroke_width=3)
        line_DO = Line(D, O, stroke_color=ink, stroke_width=3)
        rectangle_sides = VGroup(line_OB, line_BC, line_CD, line_DO)

        extension_line = Line(C, E, stroke_color=ink, stroke_width=3)
        de_line_group = VGroup(line_CD, extension_line)

        dot_O = Dot(O, radius=0.045, color=ink).set_z_index(1)
        dot_B = Dot(B, radius=0.045, color=ink).set_z_index(1)
        dot_C = Dot(C, radius=0.045, color=ink)
        dot_D = Dot(D, radius=0.045, color=ink).set_z_index(1)
        dot_E = Dot(E, radius=0.045, color=ink).set_z_index(1)
        rect_dots = VGroup(dot_O, dot_B, dot_C, dot_D).set_color("#0BE4AD")

        label_O = Tex("O", font_size=32).set_color(ink).next_to(O, DL, buff=0.12)
        label_B = Tex("B", font_size=32).set_color(ink).next_to(B, DOWN, buff=0.12)
        label_C = Tex("C", font_size=32).set_color(ink).next_to(C, RIGHT, buff=0.12)
        label_D = Tex("D", font_size=32).set_color(ink).next_to(D, UP, buff=0.12)
        label_E = Tex("E", font_size=32).set_color(ink).next_to(E, DR, buff=0.1)
        rect_labels = VGroup(label_O, label_B, label_C, label_D)

        diagram = VGroup(
            axes, x_label, y_label,
            rectangle_sides, extension_line,
            rect_dots, dot_E,
            rect_labels, label_E,
        )
        diagram.move_to(np.array([2.8, 0.0, 0.0]))

        # ---- Beat 1: "This question appeared in Edexcel Higher Maths
        # Paper 3, November 2024, and many students were unable to
        # arrive at the correct solution." (show the question build) ----
        self.play(Write(header))
        self.play(ShowCreation(axes), FadeIn(x_label), FadeIn(y_label))
        self.play(ShowCreation(rectangle_sides), FadeIn(rect_dots))
        self.play(LaggedStart(*[Write(l) for l in rect_labels], lag_ratio=0.2))
        self.play(ShowCreation(extension_line), FadeIn(dot_E), Write(label_E))
        self.play(Write(footer))
        self.wait()

        # ============================================================
        # Beat 2: "We are told that OBCD is a rectangle and that D, C
        # and E lie on the same straight line."
        # -> highlight OBCD, unhighlight, highlight DCE, unhighlight
        # ============================================================
        self.play(rectangle_sides.animate.set_color(teal_obcd))
        self.wait()
        self.play(rectangle_sides.animate.set_color(ink))
        self.wait()

        self.play(de_line_group.animate.set_color(terracotta_de))
        self.wait()
        self.play(de_line_group.animate.set_color(ink))
        self.wait()

        # ============================================================
        # Beat 3: "The coordinates of B are (2, -4), and the
        # coordinates of E are (12, -6.5)."
        # -> fly a copy of each coordinate label out to its point
        # ============================================================
        b_coord_callout = b_coords_only.copy().scale(0.72)
        b_coord_callout.next_to(label_B, DOWN, buff=0.15)
        self.play(TransformFromCopy(b_coords_only, b_coord_callout))
        self.wait()

        e_coord_callout = e_coords_only.copy().scale(0.72)
        e_coord_callout.next_to(label_E, DOWN, buff=0.15)
        self.play(TransformFromCopy(e_coords_only, e_coord_callout))
        self.wait()

        # ============================================================
        # Beat 4: "We are asked to work out the coordinates of point
        # D." -> highlight point D, keep it highlighted (no fade back)
        # ============================================================
        self.play(
            dot_D.animate.set_color(amber_d).scale(2.0),
            label_D.animate.set_color(amber_d),
        )
        self.wait()

        # "So, how can we do that?" - narration only
        self.wait()

        # ============================================================
        # Beat 5: "Notice that point D lies at the intersection of two
        # straight lines: OD and DE." -> highlight both OD and DE
        # ============================================================
        self.play(
            line_DO.animate.set_color(blue_od),
            de_line_group.animate.set_color(terracotta_de),
        )
        self.wait()

        # "If we can find the equations of these two lines, then we
        # can use simultaneous equations to find the point where they
        # intersect." -> fade the OD / DE highlight back to black
        self.play(
            line_DO.animate.set_color(ink),
            de_line_group.animate.set_color(ink),
        )
        self.wait()

        # "And that point of intersection is exactly the coordinates
        # of D." - narration only
        self.wait()

        # ============================================================
        # Beat 6: "Remember, whenever we have two straight lines and
        # we want to find the point where they meet, simultaneous
        # equations are usually the method to use."
        # -> The question wording (header/footer) has done its job by
        # now, so it fades out to make room for the working-out area.
        # The OBCD diagram itself is NOT touched - it stays on screen,
        # unchanged, for the rest of the video.
        # ============================================================
        header_footer_group = VGroup(header, footer)
        self.play(FadeOut(header_footer_group))

        gap_left_x = -FRAME_X_RADIUS + 0.4
        gap_right_x = diagram.get_left()[0] - 0.5
        gap_top_y = FRAME_Y_RADIUS - 0.6
        gap_bottom_y = -FRAME_Y_RADIUS + 0.6
        gap_width = gap_right_x - gap_left_x
        gap_height = gap_top_y - gap_bottom_y
        gap_center = np.array([
            (gap_left_x + gap_right_x) / 2, (gap_top_y + gap_bottom_y) / 2, 0.0
        ])

        mini_x_axis = Line(LEFT * 2, RIGHT * 2, stroke_color=grey_illustration, stroke_width=2)
        mini_x_axis.add_tip(length=0.18, width=0.11)
        mini_y_axis = Line(DOWN * 1.5, UP * 1.5, stroke_color=grey_illustration, stroke_width=2)
        mini_y_axis.add_tip(length=0.18, width=0.11)
        mini_axes = VGroup(mini_x_axis, mini_y_axis)

        l1_start, l1_end = np.array([-1.5, -1.0, 0]), np.array([1.5, 1.2, 0])
        l2_start, l2_end = np.array([-1.5, 1.5, 0]), np.array([1.5, -0.3, 0])
        mini_line1 = Line(l1_start, l1_end, stroke_color=grey_illustration, stroke_width=2.5).set_color("#2F79DA")
        mini_line2 = Line(l2_start, l2_end, stroke_color=grey_illustration, stroke_width=2.5).set_color("#2F79DA")

        mini_intersection = line_intersection(l1_start, l1_end, l2_start, l2_end)
        mini_dot = Dot(mini_intersection, radius=0.06).set_color("#2F79DA").set_z_index(1)

        mini_label1 = Text("Line 1", font=body_font, font_size=26,
                            color=grey_illustration).next_to(mini_line1.get_end(), UR, buff=0.1)
        mini_label2 = Text("Line 2", font=body_font, font_size=26,
                            color=grey_illustration).next_to(mini_line2.get_end(), DR, buff=0.1)

        sim_eq_text = Text("Simultaneous Equations", font=body_font,
                            slant=ITALIC, font_size=30, color=grey_illustration)
        sim_eq_text.next_to(mini_axes, DOWN, buff=0.6)

        illustration = VGroup(
            mini_axes, mini_line1, mini_line2, mini_dot,
            mini_label1, mini_label2, sim_eq_text,
        )
        illustration.set_max_width(gap_width)
        illustration.set_max_height(gap_height)
        illustration.move_to(gap_center)

        self.play(ShowCreation(mini_axes))
        self.play(ShowCreation(mini_line1), ShowCreation(mini_line2))
        self.play(FadeIn(mini_dot), Write(mini_label1), Write(mini_label2))
        self.play(Write(sim_eq_text))
        self.wait(2)

        self.play(FadeOut(illustration))

        # ============================================================
        # Beat 7: "Let's begin by finding the equation of the line
        # DE." -> re-highlight line DE (it was never hidden, so no
        # need to bring anything back)
        # ============================================================
        self.play(de_line_group.animate.set_color(terracotta_de))
        self.wait()

        # "Display the general equation y = mx + c. Label m as the
        # gradient and c as the y-intercept." -> built in the same
        # left-hand gap the illustration just used.
        y_part = Tex("y", font_size=44).set_color(ink)
        eq_part = Tex("=", font_size=44).set_color(ink)
        m_part = Tex("m", font_size=44).set_color(m_color)
        x_part = Tex("x", font_size=44).set_color(ink)
        plus_part = Tex("+", font_size=44).set_color(ink)
        c_part = Tex("c", font_size=44).set_color(c_color)
        general_eq = VGroup(y_part, eq_part, m_part, x_part, plus_part, c_part)
        general_eq.arrange(RIGHT, buff=0.1)

        gradient_label = Text("gradient", font=body_font, slant=ITALIC,
                               font_size=26).set_color(m_color)
        gradient_label.next_to(m_part, UP, buff=0.7)
        gradient_arrow = Arrow(gradient_label.get_bottom(), m_part.get_top(),
                                buff=0.08, thickness=2.0, color=m_color)

        intercept_label = Text("y-intercept", font=body_font, slant=ITALIC,
                                font_size=26).set_color(c_color)
        intercept_label.next_to(c_part, DOWN, buff=0.7)
        intercept_arrow = Arrow(intercept_label.get_top(), c_part.get_bottom(),
                                 buff=0.08, thickness=2.0, color=c_color)

        # ============================================================
        # Beat 8: "Let's start by finding the gradient first."
        # -> gradient formula (y2-y1)/(x2-x1), placed below the
        # y = mx + c block.
        # ============================================================
        grad_num = Tex(R"y_2 - y_1", font_size=36).set_color(ink)
        grad_den = Tex(R"x_2 - x_1", font_size=36).set_color(ink)
        grad_bar_width = max(grad_num.get_width(), grad_den.get_width()) + 0.2
        grad_bar = Line(LEFT * grad_bar_width / 2, RIGHT * grad_bar_width / 2,
                         stroke_color=ink, stroke_width=2)
        grad_num.next_to(grad_bar, UP, buff=0.1)
        grad_den.next_to(grad_bar, DOWN, buff=0.1)
        grad_fraction = VGroup(grad_num, grad_bar, grad_den)

        m_label2 = Tex("m", font_size=36).set_color(m_color)
        equals2 = Tex("=", font_size=36).set_color(ink)
        gradient_formula = VGroup(m_label2, equals2, grad_fraction).arrange(RIGHT, buff=0.25)
        gradient_formula.next_to(
            VGroup(gradient_label, general_eq, intercept_label, intercept_arrow),
            DOWN, buff=0.7, aligned_edge=LEFT
        )

        # Fit the whole work-notes block into the same gap the
        # illustration occupied a moment ago, then reveal it there.
        work_notes = VGroup(
            general_eq, gradient_label, gradient_arrow,
            intercept_label, intercept_arrow, gradient_formula,
        )
        work_notes.set_max_width(gap_width)
        work_notes.set_max_height(gap_height)
        work_notes.move_to(gap_center)

        self.play(Write(general_eq))
        self.wait()
        self.play(Write(gradient_label), ShowCreation(gradient_arrow))
        self.wait()
        self.play(Write(intercept_label), ShowCreation(intercept_arrow))
        self.wait()

        self.play(Write(gradient_formula))
        self.wait(2)

        # "Normally, to calculate a gradient, we need the coordinates
        # of two points ... but for line DE we only know one point, E.
        # So how can we find its gradient without a second point?" -
        # narration only.
        self.wait(3)

        # ============================================================
        # Beat 9: "Here's the clever observation. Notice that DE is
        # parallel to OB." -> highlight DE and OB together
        # ============================================================
        self.play(
            de_line_group.animate.set_color(terracotta_de),  # already this colour; reasserts it
            line_OB.animate.set_color(green_ob),
        )
        self.wait(2)

        # ============================================================
        # Beat 10: "And parallel lines always have the same gradient.
        # So instead of finding the gradient of DE, we can find the
        # gradient of OB instead." - narration only.
        # ============================================================
        self.wait(2)

        # ============================================================
        # Beat 11: "The point O is the origin, so its coordinates are
        # (0, 0)." -> write (0,0) at O; relabel O(x1,y1), B(x2,y2)
        # ============================================================
        o_coord_callout = Text("(0, 0)", font=body_font, slant=ITALIC,
                                font_size=25).set_color(ink)
        o_coord_callout.next_to(dot_O, UL, buff=0.12)

        new_label_O = Tex(R"O(x_1, y_1)", font_size=30).set_color(ink)
        new_label_O.next_to(dot_O, DL, buff=0.12)
        new_label_B = Tex(R"B(x_2, y_2)", font_size=30).set_color(ink)
        new_label_B.next_to(dot_B, DOWN, buff=0.12)

        # Tracks every NEW work-area mobject from here on, so it can
        # all be cleared in one go later without disturbing the
        # diagram (label_O/label_B are diagram labels, so they are
        # deliberately left out of this tracking group).
        solving_de_extras = VGroup(o_coord_callout)

        self.play(
            Write(o_coord_callout),
            label_O.animate.become(new_label_O),
            label_B.animate.become(new_label_B),
        )
        self.wait()

        # ============================================================
        # Beat 12: "Using the gradient formula: (-4-0)/(2-0) = -4/2
        # = -2. So the gradient of OB is -2."
        # ============================================================
        m_ob_label = Tex(R"m(OB)", font_size=36).set_color(green_ob)
        m_ob_label.move_to(m_label2.get_center()).shift(LEFT * 0.3)  # slight left-shift to avoid overlap with '='
        self.play(m_label2.animate.become(m_ob_label))
        self.wait()

        sub_num_val1 = Tex("-4", font_size=36).set_color(ink)
        sub_num_minus = Tex("-", font_size=36).set_color(ink)
        sub_num_val2 = Tex("0", font_size=36).set_color(ink)
        sub_num = VGroup(sub_num_val1, sub_num_minus, sub_num_val2).arrange(RIGHT, buff=0.1)
        sub_num.next_to(grad_bar, UP, buff=0.1)

        sub_den_val1 = Tex("2", font_size=36).set_color(ink)
        sub_den_minus = Tex("-", font_size=36).set_color(ink)
        sub_den_val2 = Tex("0", font_size=36).set_color(ink)
        sub_den = VGroup(sub_den_val1, sub_den_minus, sub_den_val2).arrange(RIGHT, buff=0.1)
        sub_den.next_to(grad_bar, DOWN, buff=0.1)

        self.play(
            # Fly coordinate numbers into target positions
            TransformFromCopy(b_coord_callout[4:], sub_num_val1),  # -4 replaces y_2
            TransformFromCopy(o_coord_callout[4],  sub_num_val2),  # 0 replaces y_1
            TransformFromCopy(b_coord_callout[1],  sub_den_val1),  # 2 replaces x_2
            TransformFromCopy(o_coord_callout[1],  sub_den_val2),  # 0 replaces x_1

            # Fade out variable letters in-place as numbers arrive
            FadeOut(grad_num[0:2]),  # y_2
            FadeOut(grad_num[3:5]),  # y_1
            FadeOut(grad_den[0:2]),  # x_2
            FadeOut(grad_den[3:5]),  # x_1

            # Morph original minus signs into new minus signs
            ReplacementTransform(grad_num[2], sub_num_minus),
            ReplacementTransform(grad_den[2], sub_den_minus),
        )

        self.wait()
        solving_de_extras.add(sub_num, sub_den)

        substituted_fraction = VGroup(sub_num, grad_bar, sub_den)

        # 1. Create the target simplified fraction elements centered at the same location
        simplified_num = Tex("-4", font_size=36).set_color(ink)
        simplified_den = Tex("2", font_size=36).set_color(ink)

        # Calculate a shorter bar width for the simplified numbers
        simp_bar_width = max(simplified_num.get_width(), simplified_den.get_width()) + 0.2
        simp_bar = Line(
            LEFT * simp_bar_width / 2, 
            RIGHT * simp_bar_width / 2, 
            stroke_color=ink, 
            stroke_width=2
        ).move_to(grad_bar.get_left()).shift(RIGHT*0.3)  # Keep the exact same center position

        simplified_num.next_to(simp_bar, UP, buff=0.1)
        simplified_den.next_to(simp_bar, DOWN, buff=0.1)

        # 2. Animate the in-place transformation
        self.play(
            # Move -4 and 2 into their centered positions
            ReplacementTransform(sub_num_val1, simplified_num),
            ReplacementTransform(sub_den_val1, simplified_den),
            
            # Fade out the "- 0" terms
            FadeOut(sub_num_minus),
            FadeOut(sub_num_val2),
            FadeOut(sub_den_minus),
            FadeOut(sub_den_val2),
            
            # Shrink the fraction bar in-place
            ReplacementTransform(grad_bar, simp_bar),
        )
        self.wait()

        # Group the updated in-place fraction
        simplified_frac = VGroup(simplified_num, simp_bar, simplified_den)

        # 3. Write "= -2" to the right of the newly simplified fraction
        equals_b = Tex("=", font_size=36).set_color(ink)
        equals_b.next_to(simplified_frac, RIGHT, buff=0.3)

        final_value = Tex("-2", font_size=36).set_color(ink)
        final_value.next_to(equals_b, RIGHT, buff=0.3)

        self.play(Write(equals_b), Write(final_value))
        self.wait()

        solving_de_extras.add(simplified_frac, equals_b, final_value)

        # ============================================================
        # Beat 13: "Since OB and DE are parallel, the gradient of DE
        # is also -2." -> write "= m(DE)" in DE's colour
        # ============================================================
        equals_c = Tex("=", font_size=36).set_color(ink)
        equals_c.next_to(final_value, RIGHT, buff=0.3)
        m_de_label = Tex(R"m(DE)", font_size=36).set_color(terracotta_de)
        m_de_label.next_to(equals_c, RIGHT, buff=0.3)

        self.play(Write(equals_c), Write(m_de_label))
        self.wait(2)
        solving_de_extras.add(equals_c, m_de_label)

        # ============================================================
        # Beat 14: "Now we already know one point on the line DE,
        # namely E(12, -6.5). So we can substitute these values into
        # the equation of the line. -6.5 = -2(12) + c"
        # ============================================================
        self.play(
            FadeOut(gradient_label), FadeOut(gradient_arrow),
            FadeOut(intercept_label), FadeOut(intercept_arrow),
        )
        self.wait()

        # Throwaway copies purely to compute the new layout - never
        # added to the scene themselves.
        layout_calc = VGroup(
            Tex("-6.5", font_size=44), eq_part.copy(), Tex("-2", font_size=44),
            Tex("(", font_size=44), Tex("12", font_size=44), Tex(")", font_size=44),
            plus_part.copy(), c_part.copy(),
        ).arrange(RIGHT, buff=0.08)
        layout_calc.move_to(general_eq.get_center())

        neg6_5 = Tex("-6.5", font_size=44).set_color(ink).move_to(layout_calc[0])
        neg2_in_eq = Tex("-2", font_size=44).set_color(ink).move_to(layout_calc[2])
        open_paren = Tex("(", font_size=44).set_color(ink).move_to(layout_calc[3])
        twelve = Tex("12", font_size=44).set_color(ink).move_to(layout_calc[4])
        close_paren = Tex(")", font_size=44).set_color(ink).move_to(layout_calc[5])

        self.play(
            FadeOut(y_part), TransformFromCopy(e_coord_callout, neg6_5),
            FadeOut(m_part), TransformFromCopy(final_value, neg2_in_eq),
            FadeIn(open_paren),
            FadeOut(x_part), TransformFromCopy(e_coord_callout, twelve),
            FadeIn(close_paren),
            eq_part.animate.move_to(layout_calc[1]),
            plus_part.animate.move_to(layout_calc[6]),
            c_part.animate.move_to(layout_calc[7]),
        )
        self.wait(2)
        solving_de_extras.add(neg6_5, neg2_in_eq, open_paren, twelve, close_paren)

        # ============================================================
        # Beat 15: "Multiplying -2 with 12 gives -24." Also fade in a
        # general y = mx + c template, in DE's colour, above the
        # equation now being solved for c.
        # ============================================================
        layout_calc2 = VGroup(
            neg6_5.copy(), eq_part.copy(), Tex("-24", font_size=44),
            plus_part.copy(), c_part.copy(),
        ).arrange(RIGHT, buff=0.12)
        layout_calc2.move_to(VGroup(neg6_5, eq_part, plus_part, c_part).get_center())

        neg24 = Tex("-24", font_size=44).set_color(ink).move_to(layout_calc2[2])
        de_general_eq = Tex(R"y = mx + c", font_size=40).set_color(terracotta_de)
        solving_de_extras.add(neg24)
        # The line still currently being worked on (only the pieces
                # that are actually visible right now).
        current_working_line = VGroup(neg6_5, eq_part, neg24, plus_part, c_part)
        de_general_eq.next_to(current_working_line, UP, buff=0.7, aligned_edge=LEFT).shift(UP)
        self.play(
            FadeOut(VGroup(neg2_in_eq, open_paren, twelve, close_paren)),
            Write(neg24),
            eq_part.animate.move_to(layout_calc2[1]),
            plus_part.animate.move_to(layout_calc2[3]),
            c_part.animate.move_to(layout_calc2[4]),FadeIn(de_general_eq)
        )
        self.wait()

        # ============================================================
        # Beat 16: "Now add 24 to both sides, and we get: c = 17.5"
        # ============================================================

        # 1. Create and position "+24" below LHS and RHS
        plus24_lhs = Tex("+24", font_size=36).set_color(ink).next_to(neg6_5, DOWN, buff=0.25)
        plus24_rhs = Tex("+24", font_size=36).set_color(ink).next_to(neg24, DOWN, buff=0.25)

        # Write +24 underneath both sides
        self.play(
            Write(plus24_lhs),
            Write(plus24_rhs)
        )
        self.wait(1)

        # 2. Prepare the final target positions for "17.5 = c"
        val_17_5 = Tex("17.5", font_size=44).set_color(ink)

        # Group template to determine where 17.5, =, and c should end up
        target_line = VGroup(
            val_17_5,
            eq_part.copy(),
            c_part.copy()
        ).arrange(RIGHT, buff=0.12).move_to(current_working_line)

        # 3. Animate the in-place calculation and shift
        self.play(
            # Combine -6.5 and bottom +24 into 17.5 at target position
            ReplacementTransform(VGroup(neg6_5, plus24_lhs), target_line[0]),
            
            # Fade out -24, +, and bottom +24 on the RHS
            FadeOut(VGroup(neg24, plus_part, plus24_rhs)),
            # Slide = and c into their new positions)
            eq_part.animate.move_to(target_line[1]),
                    c_part.animate.move_to(target_line[2]))
  
        self.wait(2)

        # Update current working line tracking
        current_working_line = VGroup(val_17_5, eq_part, c_part)
        solving_de_extras.add(val_17_5, plus24_lhs, plus24_rhs)
                # ============================================================
        # Beat 17: "Putting everything together, the equation of the
        # line DE is: y = -2x + 17.5" -> substitute m and c into the
        # template equation, then clear everything else off screen
        # except the diagram and this result.
        # ============================================================

        self.wait()
                # 1. Create the final equation with the terracotta color and align it to the general equation
        final_de_eq = Tex(R"y = -2x + 17.5", font_size=40).set_color(terracotta_de)
        final_de_eq.move_to(de_general_eq, aligned_edge=LEFT)


        self.play(
            # Fly copy of 17.5 into "c" position (recolors to terracotta_de automatically)
            TransformFromCopy(val_17_5, final_de_eq[6:]),
            
            # Fly copy of -2 into "m" position (replace `m_solved_val` with your variable name for -2)
            TransformFromCopy(final_value, final_de_eq[2:4]),
            
            # Fade out original "m" and "c" variables
            FadeOut(de_general_eq[2]),  # m
            FadeOut(de_general_eq[5]),  # c
            
            # Smoothly adjust "y =", "x", and "+" into the newly aligned positions
            ReplacementTransform(de_general_eq[0:2], final_de_eq[0:2]), # y =
            ReplacementTransform(de_general_eq[3], final_de_eq[4]),     # x
            ReplacementTransform(de_general_eq[4], final_de_eq[5]),     # +
        )
        self.wait(2)

        # 1. Define the targets for single-letter labels
        reset_label_O = Tex("O", font_size=32).set_color(ink).next_to(dot_O, DL, buff=0.12)
        reset_label_B = Tex("B", font_size=32).set_color(ink).next_to(dot_B, DOWN, buff=0.12)

        
        self.play(FadeOut(target_line), FadeOut(m_label2), FadeOut(m_de_label), FadeOut(final_value),
                  FadeOut(equals_b),FadeOut(simplified_frac),FadeOut(equals2), FadeOut(c_part), FadeOut(eq_part),
                  FadeOut(equals_c), label_O.animate.become(reset_label_O),
                      label_B.animate.become(reset_label_B))
        # ============================================================
        # Beat 18: "Now let's find the equation of the line OD."
        # -> highlight OD
        # ============================================================
        self.wait()
        self.play(line_DO.animate.set_color(blue_od))
        self.wait(2)

        # ============================================================
        # Beat 19: "Notice that OD is perpendicular to OB. This is
        # because OBCD is a rectangle, and every pair of adjacent
        # sides in a rectangle are perpendicular." -> draw the small
        # right-angle box at all four corners of the rectangle.
        # ============================================================
        def right_angle_marker(vertex, p1, p2, size=0.13):
            u1 = (p1 - vertex) / np.linalg.norm(p1 - vertex)
            u2 = (p2 - vertex) / np.linalg.norm(p2 - vertex)
            corner1 = vertex + size * u1
            corner2 = vertex + size * u1 + size * u2
            corner3 = vertex + size * u2
            marker = VMobject(stroke_color=ink, stroke_width=2.5)
            marker.set_points_as_corners([corner1, corner2, corner3])
            return marker

        # Read the vertices' ACTUAL current positions off the lines
        # themselves (the diagram was moved via diagram.move_to()
        # after O/B/C/D were first defined, so those original
        # variables no longer match where the rectangle really is).
        O_now = line_OB.get_start()
        B_now = line_OB.get_end()
        C_now = line_BC.get_end()
        D_now = line_CD.get_end()

        angle_O = right_angle_marker(O_now, B_now, D_now)
        angle_B = right_angle_marker(B_now, O_now, C_now)
        angle_C = right_angle_marker(C_now, B_now, D_now)
        angle_D = right_angle_marker(D_now, C_now, O_now)
        right_angle_markers = VGroup(angle_O, angle_B, angle_C, angle_D)

        self.play(LaggedStart(*[ShowCreation(m) for m in right_angle_markers], lag_ratio=0.3))
        self.wait(2)

        # ============================================================
        # Colours/geometry reused from here on
        # ============================================================
        answer_color = "#FF3EA5"  # vivid magenta, used for final-answer callouts

        # ============================================================
        # Beat 20: "We already know that the gradient of OB is -2."
        # -> write m(OB) = -2 below DE's equation. A placeholder
        # reserves OD's eventual equation slot directly under DE's,
        # so none of the working below ever encroaches on it.
        # ============================================================
        od_eq_placeholder = Tex(R"y = \frac{1}{2}x", font_size=40)
        od_eq_placeholder.next_to(final_de_eq, DOWN, buff=0.5, aligned_edge=LEFT)
        # (never added to the scene - purely a layout reference)

        m_ob_eq2_label = Tex(R"m(OB)", font_size=36).set_color(green_ob)
        m_ob_eq2_sign = Tex("=", font_size=36).set_color(ink)
        m_ob_eq2_val = Tex("-2", font_size=36).set_color(ink)
        m_ob_eq2 = VGroup(m_ob_eq2_label, m_ob_eq2_sign, m_ob_eq2_val).arrange(RIGHT, buff=0.15)
        m_ob_eq2.next_to(od_eq_placeholder, DOWN, buff=0.6, aligned_edge=LEFT)

        self.play(Write(m_ob_eq2))
        self.wait()

        # ============================================================
        # Beat 21: "For two perpendicular lines, their gradients are
        # negative reciprocals of one another." -> m(OD) = -1/m(OB)
        # Positioned with extra headroom below, since m(OB) = -2 is
        # about to grow into a fraction plus a "x(-1)" annotation
        # line before this row is reached.
        # ============================================================
        m_od_label = Tex(R"m(OD)", font_size=36).set_color(blue_od)
        m_od_sign = Tex("=", font_size=36).set_color(ink)
        recip_num = Tex("-1", font_size=32).set_color(ink)
        recip_den = Tex(R"m(OB)", font_size=32).set_color(green_ob)
        recip_bar_w = max(recip_num.get_width(), recip_den.get_width()) + 0.15
        recip_bar = Line(LEFT * recip_bar_w / 2, RIGHT * recip_bar_w / 2,
                          stroke_color=ink, stroke_width=2)
        recip_num.next_to(recip_bar, UP, buff=0.06)
        recip_den.next_to(recip_bar, DOWN, buff=0.06)
        recip_frac = VGroup(recip_num, recip_bar, recip_den)
        m_od_line = VGroup(m_od_label, m_od_sign, recip_frac).arrange(RIGHT, buff=0.2)
        m_od_line.next_to(m_ob_eq2, DOWN, buff=1.5, aligned_edge=LEFT)

        self.play(
            Write(m_od_label), Write(m_od_sign), Write(recip_num), ShowCreation(recip_bar),
            TransformFromCopy(m_ob_eq2_label, recip_den),
        )
        self.wait(2)

        # ============================================================
        # Beat 22: "So first, take the reciprocal of -2, which is
        # -1/2." -> m(OB) = -2  becomes  1/m(OB) = -1/2
        # ============================================================
        step2_num = Tex("1", font_size=36).set_color(ink)
        step2_den = Tex(R"m(OB)", font_size=32).set_color(green_ob)
        step2_bar_w = max(step2_num.get_width(), step2_den.get_width()) + 0.15
        step2_bar = Line(LEFT * step2_bar_w / 2, RIGHT * step2_bar_w / 2,
                          stroke_color=ink, stroke_width=2)
        step2_num.next_to(step2_bar, UP, buff=0.06)
        step2_den.next_to(step2_bar, DOWN, buff=0.06)
        step2_lhs_frac = VGroup(step2_num, step2_bar, step2_den)

        step2_rnum = Tex("-1", font_size=36).set_color(ink)
        step2_rden = Tex("2", font_size=36).set_color(ink)
        step2_rbar_w = max(step2_rnum.get_width(), step2_rden.get_width()) + 0.15
        step2_rbar = Line(LEFT * step2_rbar_w / 2, RIGHT * step2_rbar_w / 2,
                           stroke_color=ink, stroke_width=2)
        step2_rnum.next_to(step2_rbar, UP, buff=0.06)
        step2_rden.next_to(step2_rbar, DOWN, buff=0.06)
        step2_rhs_frac = VGroup(step2_rnum, step2_rbar, step2_rden)

        step2_group = VGroup(step2_lhs_frac, m_ob_eq2_sign, step2_rhs_frac)
        step2_group.arrange(RIGHT, buff=0.2)
        step2_group.move_to(m_ob_eq2, aligned_edge=LEFT)

        self.play(
            FadeOut(m_ob_eq2_label),
            TransformFromCopy(m_ob_eq2_label, step2_den),
            Write(step2_num), ShowCreation(step2_bar),
            m_ob_eq2_sign.animate.move_to(step2_group[1]),
            ReplacementTransform(m_ob_eq2_val, step2_rhs_frac),
        )
        self.wait(2)

        # ============================================================
        # Beat 23: "Then multiply the result with a negative one."
        # -> write x(-1) under both sides
        # ============================================================
        times_neg1_lhs = Tex(R"\times(-1)", font_size=26).set_color(ink)
        times_neg1_lhs.next_to(step2_lhs_frac, DOWN, buff=0.22)
        times_neg1_rhs = Tex(R"\times(-1)", font_size=26).set_color(ink)
        times_neg1_rhs.next_to(step2_rhs_frac, DOWN, buff=0.22)

        self.play(Write(times_neg1_lhs), Write(times_neg1_rhs))
        self.wait()

        # ============================================================
        # Beat 24: "This gives us a gradient of 1/2 for the line OD."
        # -> Apply sign changes in-place: -1/m(OB) = 1/2 = m(OD)
        # ============================================================

        # 1. LHS: Create the leading minus sign for the left side
        final_neg = Tex("-", font_size=36).set_color(ink)

        # Position the minus sign to the left of the original LHS fraction
        lhs_target = VGroup(final_neg, step2_lhs_frac.copy()).arrange(RIGHT, buff=0.08)
        lhs_target.move_to(step2_lhs_frac, aligned_edge=RIGHT)  # Keep aligned with '='
        final_neg.move_to(lhs_target[0])

        # 2. RHS: Create target numerator (changing "-1" into "1")
        final_rnum = Tex("1", font_size=36).set_color(ink).move_to(step2_rnum)

        # 3. Animate the in-place sign changes
        self.play(
            # LHS: Fly \times(-1) up to become the minus sign, slide original fraction slightly right
            ReplacementTransform(times_neg1_lhs, final_neg),
            step2_lhs_frac.animate.move_to(lhs_target[1]),

            # RHS: Change "-1" to "1" in-place and fade out the bottom multiplier
            ReplacementTransform(step2_rnum, final_rnum),
            FadeOut(times_neg1_rhs),
        )
        self.wait()

        # Update references for the RHS fraction
        final_rhs_frac = VGroup(final_rnum, step2_rbar, step2_rden)

        # 4. Append "= m(OD)" to the right side
        m_od_result_sign = Tex("=", font_size=36).set_color(ink)
        m_od_result_sign.next_to(final_rhs_frac, RIGHT, buff=0.25)

        m_od_result_label = Tex(R"m(OD)", font_size=36).set_color(blue_od)
        m_od_result_label.next_to(m_od_result_sign, RIGHT, buff=0.25)

        self.play(
            Write(m_od_result_sign), 
            TransformFromCopy(m_od_label, m_od_result_label)
        )
        self.wait(2)

        # ============================================================
        # "Now what about the y-intercept? Since the line OD passes
        # through the origin, its y-intercept is simply 0."
        # -> highlight the origin, then write c = 0
        # ============================================================
        self.play(dot_O.animate.scale(1.8), rate_func=there_and_back, run_time=1.2)
        self.wait(0.3)

        # 1. Group the current working line for precise alignment
        od_line = VGroup(final_neg, step2_lhs_frac, m_ob_eq2_sign, final_rhs_frac, m_od_result_sign, 
            m_od_result_label)

        # 2. Position od_c_eq relative to the full equation line
        od_c_eq = Tex("c = 0", font_size=36).set_color(ink)
        od_c_eq.next_to(od_line, DOWN, buff=0.6, aligned_edge=LEFT)

        self.play(Write(od_c_eq))
        self.wait(2)

        # ============================================================
        # "So the equation of OD becomes: y = 1/2 x" -> written into
        # the pre-reserved slot directly below DE's equation, in OD's
        # colour, then every calculation below is cleared away.
        # ============================================================
        od_final_eq = Tex(R"y = \frac{1}{2}x", font_size=40).set_color(blue_od)
        od_final_eq.move_to(od_eq_placeholder)

        self.play(Write(od_final_eq))
        self.wait()

        calc_cleanup_group = VGroup(
            m_ob_eq2_sign, step2_den, step2_num, step2_bar,
            m_od_label, m_od_sign, recip_num, recip_bar, recip_den,
            final_rhs_frac, m_od_result_sign, m_od_result_label,
            od_c_eq, final_neg
        )
        self.play(FadeOut(calc_cleanup_group))
        self.wait()

        # ============================================================
        # "Now we have both equations... Notice that at point D, both
        # equations have the same y values and also the same x
        # values." -> grey dashed projection lines from D to each axis
        # ============================================================
        O_now = line_OB.get_start()
        D_now = line_CD.get_end()
        y_axis_x = y_axis.get_center()[0]
        x_axis_y = x_axis.get_center()[1]

        y_foot = np.array([y_axis_x, D_now[1], 0.0])
        x_foot = np.array([D_now[0], x_axis_y, 0.0])

        horiz_to_D = DashedLine(y_foot, D_now, stroke_color=grey_illustration,
                                 stroke_width=2, dash_length=0.08)
        y_at_D_label = Tex("y", font_size=28).set_color(ink)
        y_at_D_label.next_to(y_foot, LEFT, buff=0.15)

        vert_to_D = DashedLine(x_foot, D_now, stroke_color=grey_illustration,
                                stroke_width=2, dash_length=0.08)
        x_at_D_label = Tex("x", font_size=28).set_color(ink)
        x_at_D_label.next_to(x_foot, DOWN, buff=0.15)

        self.play(ShowCreation(horiz_to_D), Write(y_at_D_label))
        self.wait()
        self.play(ShowCreation(vert_to_D), Write(x_at_D_label))
        self.wait(2)

        # ============================================================
        # "So we can make the y's of both equations equal to one
        # another." -> copies of the two equations' "y" fly down to
        # the (now-cleared) working area and form y = y
        # ============================================================
        y_left = Tex("y", font_size=36).set_color(terracotta_de)
        equals_yy = Tex("=", font_size=36).set_color(ink)
        y_right = Tex("y", font_size=36).set_color(blue_od)
        yy_line = VGroup(y_left, equals_yy, y_right).arrange(RIGHT, buff=0.2)
        yy_line.next_to(od_final_eq, DOWN, buff=1.0, aligned_edge=LEFT)

        self.play(
            TransformFromCopy(final_de_eq[0], y_left),
            Write(equals_yy),
            TransformFromCopy(od_final_eq[0], y_right),
        )
        self.wait(2)

        # ============================================================
        # "Now we can substitute for y..." -> y's turn into each
        # equation's right-hand side: -2x + 17.5 = 1/2 x
        # ============================================================
        de_rhs_copy = final_de_eq[2:].copy().set_color(terracotta_de)
        od_rhs_copy = od_final_eq[2:].copy().set_color(blue_od)
        sub_eq_group = VGroup(de_rhs_copy, equals_yy, od_rhs_copy)
        sub_eq_group.arrange(RIGHT, buff=0.25)
        sub_eq_group.move_to(yy_line, aligned_edge=LEFT)

        self.play(
            ReplacementTransform(y_left, de_rhs_copy),
            equals_yy.animate.move_to(sub_eq_group[1]),
            ReplacementTransform(y_right, od_rhs_copy),
        )
        self.wait(2)

       # ============================================================
        # "To get rid of the denominator, multiply both sides by 2."
        # -> Transform ONLY the numbers: -2 -> -4, 17.5 -> 35, 1/2 cancels out
        # ============================================================
        times2_lhs = Tex(R"\times 2", font_size=26).set_color(ink)
        times2_lhs.next_to(de_rhs_copy, DOWN, buff=0.25)
        times2_rhs = Tex(R"\times 2", font_size=26).set_color(ink)
        times2_rhs.next_to(od_rhs_copy, DOWN, buff=0.25)

        self.play(Write(times2_lhs), Write(times2_rhs))
        self.wait()

        # 1. Create target numerals with font_size=40 and matching terracotta_de color
        num_neg4 = Tex("4", font_size=40).set_color(terracotta_de)
        num_35   = Tex("35", font_size=40).set_color(terracotta_de)

        # Align new numbers directly over the old ones
        num_neg4.move_to(de_rhs_copy[1], aligned_edge=LEFT)
        num_35.move_to(de_rhs_copy[5:7], aligned_edge=LEFT)

        # 2. Animate ONLY the numeral transformations (x and + stay untouched)
        self.play(
            # LHS: -2 morphs into -4, 17.5 morphs into 35
            ReplacementTransform(de_rhs_copy[1], num_neg4),
            ReplacementTransform(de_rhs_copy[4:8], num_35),
            FadeOut(times2_lhs),

            # RHS: 1/2 and multiplier fade out; x stays blue_od and moves next to '='
            FadeOut(od_rhs_copy[:-1]),  # Fade out the fraction (1/2)
            FadeOut(times2_rhs),
            od_rhs_copy[1].animate.next_to(equals_yy, 0.75*RIGHT, buff=0.15),
        )
        self.wait(2)
        # ============================================================
        # "Add 4x to both sides." -> -4x + 35 = x  becomes  35 = 5x
        # ============================================================
        plus4x_lhs = Tex(R"+4x", font_size=26).set_color(ink)
        plus4x_lhs.next_to(num_neg4, DOWN, buff=0.25)

        plus4x_rhs = Tex(R"+4x", font_size=26).set_color(ink)
        plus4x_rhs.next_to(od_rhs_copy[-1], DOWN, buff=0.25)

        self.play(Write(plus4x_lhs), Write(plus4x_rhs))
        self.wait()

        # 1. Create the digit '5' for the RHS in blue_od
        num_5 = Tex("5", font_size=40).set_color(blue_od)

        # 2. Build target layout for "35 = 5x" to calculate smooth final positions
        rhs_target_group = VGroup(num_5, od_rhs_copy[-1].copy()).arrange(RIGHT, buff=0.08)
        full_target_group = VGroup(num_35.copy(), equals_yy.copy(), rhs_target_group).arrange(RIGHT, buff=0.25)

        # Align the whole new equation flush-left with where the previous line started
        full_target_group.move_to(de_rhs_copy[0], aligned_edge=LEFT)

        # Extract individual target positions
        target_35_pos = full_target_group[0].get_center()
        target_eq_pos = full_target_group[1].get_center()
        target_5_pos  = full_target_group[2][0].get_center()
        target_x_pos  = full_target_group[2][1].get_center()

        # 3. Animate term-by-term changes
        self.play(
            # LHS: Fade out -4x, +, and the bottom +4x
            FadeOut(de_rhs_copy[0]),    # "-"
            FadeOut(num_neg4),          # "4"
            FadeOut(de_rhs_copy[2]),    # "x"
            FadeOut(de_rhs_copy[3]),    # "+"
            FadeOut(plus4x_lhs),

            # LHS: Slide 35 (terracotta_de) into its new position
            num_35.animate.move_to(target_35_pos),

            # Equals sign slides into position
            equals_yy.animate.move_to(target_eq_pos),

            # RHS: Morph bottom +4x into '5' (blue_od) and slide existing 'x' (blue_od) next to it
            ReplacementTransform(plus4x_rhs, num_5.move_to(target_5_pos)),
            od_rhs_copy[-1].animate.move_to(target_x_pos), run_time=2
        )
        self.wait(2)

        # ============================================================
        # "Finally, divide both sides by 5." -> 35 = 5x  becomes
        # x = 7, highlighted with a surrounding rectangle
        # =============================================================

        # Note: Using \divisionsymbol prevents LaTeX from rendering \div as divergence (\nabla \cdot)
        div5_lhs = Tex(R"\divisionsymbol 5", font_size=26).set_color(ink)
        div5_lhs.next_to(num_35, DOWN, buff=0.25)

        div5_rhs = Tex(R"\divisionsymbol 5", font_size=26).set_color(ink)
        div5_rhs.next_to(VGroup(num_5, od_rhs_copy[-1]), DOWN, buff=0.25)

        self.play(Write(div5_lhs), Write(div5_rhs))
        self.wait()

        # 1. Target layout for "7 = x"
        num_7 = Tex("7", font_size=40).set_color(terracotta_de)

        target_7_eq_x = VGroup(
            num_7.copy(),
            equals_yy.copy(),
            od_rhs_copy[-1].copy()
        ).arrange(RIGHT, buff=0.25)

        # Keep aligned flush-left with the current equation position
        current_eq_group = VGroup(num_35, equals_yy, num_5, od_rhs_copy[-1])
        target_7_eq_x.move_to(current_eq_group, aligned_edge=LEFT)

        # 2. Animate division to get "7 = x"
        self.play(
            # LHS: "35" becomes "7" (terracotta_de)
            ReplacementTransform(num_35, num_7.move_to(target_7_eq_x[0])),
            FadeOut(div5_lhs),

            # Equals sign moves to position
            equals_yy.animate.move_to(target_7_eq_x[1]),

            # RHS: "5" fades out, "x" (blue_od) moves to position
            FadeOut(num_5),
            FadeOut(div5_rhs),
            od_rhs_copy[-1].animate.move_to(target_7_eq_x[2]),
        )
        self.wait()

        # 3. Build target layout for "x = 7" and animate the flip
        target_x_eq_7 = VGroup(
            od_rhs_copy[-1].copy(),
            equals_yy.copy(),
            num_7.copy()
        ).arrange(RIGHT, buff=0.25)
        target_x_eq_7.move_to(target_7_eq_x, aligned_edge=LEFT)

        self.play(
            od_rhs_copy[-1].animate.move_to(target_x_eq_7[0]),
            equals_yy.animate.move_to(target_x_eq_7[1]),
            num_7.animate.move_to(target_x_eq_7[2]),
        )
        self.wait()

        # 4. Highlight "x = 7" with a surrounding box
        x_equals_7_group = VGroup(od_rhs_copy[-1], equals_yy, num_7)
        x7_box = SurroundingRectangle(x_equals_7_group, color=ink, buff=0.15)
        self.play(ShowCreation(x7_box), x_equals_7_group.animate.set_color(amber_d))
        self.wait(2)
        # ============================================================
        # "Now substitute this value back into either equation. The
        # equation y = 1/2 x is the simpler one." -> box it
        # ============================================================
        od_eq_box = SurroundingRectangle(od_final_eq, color=ink, buff=0.15)
        self.play(ShowCreation(od_eq_box))
        self.wait(2)

        # ============================================================
        # "So: y = 1/2 x 7 = 3.5" -> substitute x=7 into y = 1/2 x
        # ============================================================
        y_lhs = Tex("y", font_size=40).set_color(blue_od)
        y_eq_sign = Tex("=", font_size=40).set_color(ink)
        y_frac = Tex(R"\frac{1}{2}", font_size=40).set_color(blue_od)

        sub_y_open = Tex("(", font_size=40).set_color(ink)
        sub_y_seven = Tex("7", font_size=40).set_color(terracotta_de)
        sub_y_close = Tex(")", font_size=40).set_color(ink)

        # 2. Arrange the initial substitution line: y = 1/2 ( 7 )
        sub_y_group = VGroup(
            y_lhs, y_eq_sign, y_frac,
            sub_y_open, sub_y_seven, sub_y_close
        ).arrange(RIGHT, buff=0.1)

        sub_y_group.next_to(x7_box, DOWN, buff=0.6, aligned_edge=LEFT)

        # 3. Animate substituting 7 into the equation using num_7 from earlier
        self.play(
            Write(VGroup(y_lhs, y_eq_sign, y_frac)),
            FadeIn(sub_y_open), 
        )
        self.play( TransformFromCopy(num_7, sub_y_seven),
                    FadeIn(sub_y_close))
        self.wait()

        # 4. Target result for RHS calculation
        y_val_35 = Tex("3.5", font_size=40).set_color(blue_od)
        y_val_35.next_to(y_eq_sign, RIGHT, buff=0.25)
        y_coord = VGroup(y_val_35, y_eq_sign, y_lhs)
        x3_5_box = SurroundingRectangle(y_coord, color=ink, buff=0.15)

        # 5. Transform ONLY the RHS fraction and parentheses (y = remains completely untouched)
        self.play(
            ReplacementTransform(
                VGroup(y_frac, sub_y_open, sub_y_seven, sub_y_close),
                y_val_35),
                ShowCreation(x3_5_box),
                y_coord.animate.set_color(amber_d),
        )
        self.wait(2)

        # ============================================================
        # "Therefore, the coordinates of point D are (7, 3.5)" -> fly
        # the 7 and 3.5 to D; update the axis-crossing labels too.
        # ============================================================

        # 1. Single Tex object with sub-mobjects preserves natural TeX baseline & comma placement
        d_coord_group = Tex("(", "7", ",", "3.5", ")", font_size=32).set_color(ink)

        d_coord_group.next_to(dot_D, RIGHT, buff=0.2)

        # 2. Animate elements into coordinate form
        self.play(
            FadeIn(d_coord_group[0]),                                # "("
            TransformFromCopy(num_7, d_coord_group[1]),              # "7" (from num_7)
            FadeIn(d_coord_group[2]),                                # ","
            TransformFromCopy(y_val_35, d_coord_group[3:6]),           # "3.5" (from y_val_35)
            FadeIn(d_coord_group[6]),                                # ")"
            
            # Update axis labels on dot_D
            ReplacementTransform(x_at_D_label, Tex("7", font_size=28).set_color(ink).move_to(x_at_D_label)),
            ReplacementTransform(y_at_D_label, Tex("3.5", font_size=28).set_color(ink).move_to(y_at_D_label)),
            run_time = 1.5)
        self.wait(3)