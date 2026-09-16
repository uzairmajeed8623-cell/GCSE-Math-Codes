from manimlib import *
from types import SimpleNamespace

# ------------------------------------------------------------------
# Shared setup for the OAB sector question video (portrait, 9:16).
# The "question" scene and the "solution" scene both import this, so
# the border, question text, and diagram stay perfectly consistent
# between clips instead of drifting apart via copy-paste.
# ------------------------------------------------------------------

INK = BLACK
BODY_FONT = "Times New Roman"

SCALE = 0.5
RADIUS_VAL = 4.7
ANGLE_A = 78 * DEGREES  # direction of point A, measured from O
ANGLE_B = 22 * DEGREES  # direction of point B, measured from O
REFLEX_SWEEP = TAU - (ANGLE_A - ANGLE_B)  # the major (reflex) arc's sweep, ~304 degrees

FRAME_MARGIN = 0.35  # gap between the screen edge and the border
INNER_PAD = 0.4      # gap between the border and the content inside it


def P(x, y):
    """Map true sector coordinates (in metres) onto the scene, scaled down."""
    return np.array([x, y, 0.0]) * SCALE


def build_border():
    border = RoundedRectangle(
        width=FRAME_WIDTH - 2 * FRAME_MARGIN,
        height=FRAME_HEIGHT - 2 * FRAME_MARGIN,
        corner_radius=0.3,
        stroke_color=INK,
        stroke_width=2,
    )
    border.move_to(ORIGIN)
    return border

def build_header(border, label="Nov 2024, 3H", font_size=12, color=GREY):
    """Small paper-reference header, sat just outside the border's
    top-left corner (exam series / paper code)."""
    header = Text(label, font=BODY_FONT, font_size=font_size).set_color(color)
    header.next_to(border, UP, buff=0.12).align_to(border, LEFT).shift(RIGHT*0.3)
    return header

def content_width_for(border):
    return border.get_width() - 2 * INNER_PAD


def corner_buff():
    return FRAME_MARGIN + INNER_PAD


def build_question_text(font_size=25):
    """Returns a SimpleNamespace with the full question_text group plus
    references to the specific lines later animations need to highlight
    or move (the word 'reflex', the number '34.3')."""

    def line(text, weight=NORMAL):
        return Text(text, font=BODY_FONT, slant=ITALIC, weight=weight,
                    font_size=font_size).set_color(INK)

    q_number = Text("11", font=BODY_FONT, weight=BOLD, font_size=font_size).set_color(INK)
    stem_word = line("OAB is a")
    stem_row = VGroup(q_number, stem_word).arrange(RIGHT, buff=0.14)

    stem_block = VGroup(
        stem_row,
        line("sector of a circle"),
        line("with centre O and"),
        line("radius 4.7 m."),
    ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)

    perimeter_line1 = line("The sector has a")
    perimeter_line2 = line("perimeter of 34.3 m.")
    perimeter_block = VGroup(perimeter_line1, perimeter_line2).arrange(
        DOWN, buff=0.14, aligned_edge=LEFT
    )

    find_line1 = line("Find the size of the")
    find_line2 = line("reflex angle AOB.")
    find_block = VGroup(find_line1, find_line2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)

    round_block = VGroup(
        line("Give your answer correct"),
        line("to the nearest degree."),
    ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)

    question_text = VGroup(
        stem_block, perimeter_block, find_block, round_block
    ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)

    return SimpleNamespace(
        group=question_text,
        stem_block=stem_block,
        perimeter_block=perimeter_block,
        perimeter_line2=perimeter_line2,
        find_block=find_block,
        find_line2=find_line2,
        round_block=round_block,
    )


def build_diagram():
    """Returns a SimpleNamespace with the sector arc (major sector only,
    not a full circle), radii, dots, labels, and the diagram group.
    NOTE: the O/A/B fields here are RAW, pre-layout coordinates - only
    useful while building the diagram. Once lay_out_side_by_side() has
    scaled and moved the group, get the real on-screen positions from
    dot_O.get_center() etc. instead."""

    O = P(0, 0)
    A = P(RADIUS_VAL * np.cos(ANGLE_A), RADIUS_VAL * np.sin(ANGLE_A))
    B = P(RADIUS_VAL * np.cos(ANGLE_B), RADIUS_VAL * np.sin(ANGLE_B))

    sector_arc = Arc(arc_center=O, radius=RADIUS_VAL * SCALE, start_angle=ANGLE_A,
                      angle=REFLEX_SWEEP, stroke_color=INK, stroke_width=1.5)

    radius_OA = Line(O, A, stroke_color=INK, stroke_width=1.5)
    radius_OB = Line(O, B, stroke_color=INK, stroke_width=1.5)

    dot_O = Dot(O, radius=0.045, color=INK)
    dot_A = Dot(A, radius=0.045, color=INK)
    dot_B = Dot(B, radius=0.045, color=INK)
    sector_dots = VGroup(dot_O, dot_A, dot_B)

    label_O = Tex("O", font_size=28).set_color(INK).next_to(O, DL, buff=0.12)
    label_A = Tex("A", font_size=28).set_color(INK).next_to(A, UP, buff=0.1)
    label_B = Tex("B", font_size=28).set_color(INK).next_to(B, RIGHT, buff=0.1)
    sector_labels = VGroup(label_O, label_A, label_B)

    radius_label = Text("4.7 m", font=BODY_FONT, font_size=24).set_color(INK)
    radius_label.move_to(radius_OA.get_center()).shift(LEFT * 0.3 + UP * 0.08)

    diagram = VGroup(
        sector_arc, radius_OA, radius_OB,
        sector_dots, sector_labels, radius_label,
    )

    return SimpleNamespace(
        group=diagram,
        sector_arc=sector_arc,
        radius_OA=radius_OA,
        radius_OB=radius_OB,
        dot_O=dot_O, dot_A=dot_A, dot_B=dot_B,
        sector_dots=sector_dots,
        label_O=label_O, label_A=label_A, label_B=label_B,
        sector_labels=sector_labels,
        radius_label=radius_label,
        O=O, A=A, B=B,  # pre-layout only - see docstring above
    )


def lay_out_side_by_side(question_text_group, diagram_group, border, gap=0.3,
                          diagram_width_ratio=0.55):
    """Positions the question text (left) and diagram (right) side by
    side, both anchored to the top of the border - shared by every
    scene so the two clips line up exactly.

    diagram_width_ratio controls how the available width is split
    between the two columns (0.5 = even split). Raise it for a bigger
    diagram and narrower text column, lower it for the opposite."""
    content_width = content_width_for(border)
    available = content_width - gap
    diagram_width = available * diagram_width_ratio
    text_width = available * (1 - diagram_width_ratio)

    question_text_group.set_max_width(text_width)
    diagram_group.set_max_width(diagram_width)
    diagram_group.set_max_height(FRAME_HEIGHT * 0.46)

    question_text_group.to_corner(UL, buff=corner_buff())
    diagram_group.next_to(question_text_group, RIGHT, buff=gap, aligned_edge=UP)

    border_right_inner = border.get_right()[0] - INNER_PAD
    if diagram_group.get_right()[0] > border_right_inner:
        diagram_group.set_x(border_right_inner - diagram_group.get_width() / 2)
        diagram_group.align_to(question_text_group, UP)