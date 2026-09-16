from manimlib import *
import numpy as np

# ============================================================
#  STYLE CONSTANTS  (matched to average_frequency.py / qsequence.py)
# ============================================================
TABLE_COLOR = "#462802"     # table border / divider colour
CUM_COLOR = "#750A0A"       # cumulative-frequency accent colour
CELL_FILL = "#2B0101"       # dark "dice" fill used for numbering cells
QUESTION_COLOR = "#8B0303"  # colour for "Median?" / rhetorical questions
GROUP_COLORS0 = {
    0: "#2E7670",   # 0 pets  -> teal
    1: "#C77203",   # 1 pet   -> orange
    2: "#750A0A",   # 2 pets  -> dark red
    3: "#3674B5",   # 3 pets  -> blue
}

GROUP_COLORS = {
    0: "#C8AAAA",   # 0 pets  
    1: "#D5451B",   # 1 pet   
    2: "#FF9644",   # 2 pets  
    3: "#4B9EF7",   # 3 pets  
}


# ============================================================
#  HELPERS
# ============================================================
def create_pets_table(numbers, freqs, cum_freqs):
    """
    Builds the "Number of Pets / Frequency" table (2 visible columns),
    plus the pieces needed for the 3rd "Cumulative Frequency" column.
    The 3rd-column pieces are built now (per the brief) but are NOT
    positioned or added to the scene until they're actually needed.
    """
    # ---- Header (2 visible columns) ----
    h1 = Text("No. of Pets", font_size=34).set_color(BLACK)
    h2 = Text("Frequency", font_size=34).set_color(BLACK)
    header = VGroup(h1, h2).arrange(RIGHT, buff=0.8)

    # ---- Data rows ----
    rows = VGroup()
    cum_texts = VGroup()
    for n, f, c in zip(numbers, freqs, cum_freqs):
        num = Text(str(n), font_size=34).set_color(BLACK)
        frq = Text(str(f), font_size=34).set_color(BLACK)
        row = VGroup(num, frq).arrange(RIGHT, buff=2.2)
        rows.add(row)

        cum = Text(str(c), font_size=34).set_color(CUM_COLOR)
        cum_texts.add(cum)

    rows.arrange(DOWN, buff=0.55)

    table_content = VGroup(header, rows)
    table_content.arrange(DOWN, buff=0.6,)

    # ---- Border / divider for the visible 2-column table ----
    border = SurroundingRectangle(table_content, buff=0.2).set_color(TABLE_COLOR)

    col0_right = header[0].get_right()[0]
    col1_left = header[1].get_left()[0]
    x_div = (col0_right + col1_left) / 2
    v_line = Line(
        np.array([x_div, border.get_top()[1], 0]),
        np.array([x_div, border.get_bottom()[1], 0]),
    ).set_color(TABLE_COLOR)

    h_lines = VGroup()
    for row in rows:
        line = Line(border.get_left(), border.get_right())
        line.move_to(row.get_top() + UP * 0.28)
        line.set_color(TABLE_COLOR)
        h_lines.add(line)

    # ---- Centre the whole visible table as one rigid group ----
    VGroup(header, rows, border, v_line, h_lines).move_to(ORIGIN)

    # ---- 3rd column pieces (built now, positioned/revealed later) ----
    h3_line1 = Text("Cumulative", font_size=28).set_color(BLACK)
    h3_line2 = Text("Frequency", font_size=28).set_color(BLACK)
    h3_label = VGroup(h3_line1, h3_line2).arrange(DOWN, buff=0.05)
    h3_q = Text("?", font_size=32).set_color(CUM_COLOR)
    h3_full = VGroup(h3_label, h3_q).arrange(RIGHT, buff=0.2)

    return {
        "header": header,
        "rows": rows,
        "border": border,
        "v_line": v_line,
        "h_lines": h_lines,
        "h3_label": h3_label,
        "h3_q": h3_q,
        "h3_full": h3_full,
        "cum_texts": cum_texts,
    }


def build_third_column_frame(table_dict):
    """
    Computes the border / divider / row-lines for the FULL 3-column
    table. Call this only once the table has been moved to its final
    position and the 3rd-column pieces have been placed next to it,
    since the frame depends on their on-screen positions.
    """
    everything = VGroup(
        table_dict["header"], table_dict["rows"],
        table_dict["h3_full"], table_dict["cum_texts"],
    )
    border_full = SurroundingRectangle(everything, buff=0.17).set_color(TABLE_COLOR)

    col2_right = table_dict["header"][1].get_right()[0]
    col3_left = table_dict["h3_full"].get_left()[0]
    x_div2 = (col2_right + col3_left) / 2
    v_line2 = Line(
        np.array([x_div2, border_full.get_top()[1], 0]),
        np.array([x_div2, border_full.get_bottom()[1], 0]),
    ).set_color(TABLE_COLOR)

    h_lines_full = VGroup()
    for row in table_dict["rows"]:
        line = Line(border_full.get_left(), border_full.get_right())
        line.move_to(row.get_top() + UP * 0.28).shift(RIGHT * 1.1)  # shift right to avoid overlapping the v_line2
        line.set_color(TABLE_COLOR)
        h_lines_full.add(line)

    return border_full, v_line2, h_lines_full


def create_numbered_list_table(data_values, cell_width=0.85, cell_height=0.6):
    """
    Builds the interleaved 6-column x 10-row grid used to demonstrate
    cumulative frequency by "counting through the list":
      - even display-rows (0,2,4,6,8)  -> item numbering, 1..29,
        dark-filled cells, numbers coloured by which pet-group they
        belong to (matches GROUP_COLORS)
      - odd display-rows  (1,3,5,7,9)  -> the data values themselves,
        plain outlined cells, black text
    Only 29 of the 30 available slots are used (29 students), so the
    very last cell pair is left empty.
    """
    n_items = len(data_values)
    n_cols = 6
    n_blocks = 5  # 5 (numbering row, data row) pairs = 10 rows total

    cell_rects = VGroup()
    numbering_texts = VGroup()
    data_cells_texts = VGroup()

    for block in range(n_blocks):
        for col in range(n_cols):
            idx = block * n_cols + col          # 0-indexed position in the list
            row_numbering = 2 * block
            row_data = 2 * block + 1

            x = col * cell_width
            y_numbering = -row_numbering * cell_height
            y_data = -row_data * cell_height

            num_rect = Rectangle(width=cell_width, height=cell_height)
            num_rect.set_fill(CELL_FILL, opacity=1)
            num_rect.set_stroke(CELL_FILL, width=1)
            num_rect.move_to(np.array([x, y_numbering, 0]))
            cell_rects.add(num_rect)

            data_rect = Rectangle(width=cell_width, height=cell_height)
            data_rect.set_stroke(BLACK, width=1)
            data_rect.move_to(np.array([x, y_data, 0]))
            cell_rects.add(data_rect)

            if idx < n_items:
                item_number = idx + 1
                value = data_values[idx]

                num_text = Text(str(item_number), font_size=24).set_color(GROUP_COLORS[value])
                num_text.move_to(num_rect.get_center())
                numbering_texts.add(num_text)

                val_text = Text(str(value), font_size=28).set_color(BLACK)
                val_text.move_to(data_rect.get_center())
                data_cells_texts.add(val_text)

    group = VGroup(cell_rects, numbering_texts, data_cells_texts)
    group.center()

    return {
        "group": group,
        "cell_rects": cell_rects,
        "numbering_texts": numbering_texts,
        "data_cells_texts": data_cells_texts,
    }

 # Define the bubbly path function
def bubbly_path(start, end, alpha):
    if alpha == 0:
        return start
    if alpha == 1:
        return end
        
    # Elastic easing formula for a bouncy overshoot
    omega = 0.5 * TAU  # Controls the number of wobbles
    decay = 1        # Controls how fast the wobbling stops
    
    # Bouncy multiplier
    bubbly_alpha = 1 - np.exp(-decay * alpha) * np.sin(omega * alpha)
    
    # Interpolate coordinates using the modified alpha
    return start * (1 - bubbly_alpha) + end * bubbly_alpha


# ============================================================
#  SCENE
# ============================================================
class MedianCumulativeFrequency(InteractiveScene):
    def construct(self):
        grid = NumberPlane(
            axis_config={"stroke_color": GREY, "stroke_opacity": 0.3},
            background_line_style={"stroke_color": GREY, "stroke_width": 2, "stroke_opacity": 0.3},
        )
        self.add(grid)

        # ------------------------------------------------------
        # "A survey was conducted ... results from 29 students are
        #  summarised in this frequency table."
        # ------------------------------------------------------
        numbers = [0, 1, 2, 3]
        freqs = [11, 12, 5, 1]
        cum_freqs = [11, 23, 28, 29]

        table_dict = create_pets_table(numbers, freqs, cum_freqs)

        self.play(Write(table_dict["header"]))
        self.play(LaggedStart(*[Write(row) for row in table_dict["rows"]], lag_ratio=0.35, run_time=1.6))
        self.play(
            ShowCreation(table_dict["border"]),
            ShowCreation(table_dict["v_line"]),
            ShowCreation(table_dict["h_lines"]),
        )
        self.wait()

        # "The frequency of 11 tells us that 11 students do not own any pets."
        hl0 = SurroundingRectangle(table_dict["rows"][0]).set_color(GROUP_COLORS0[0])
        self.play(ShowCreation(hl0))
        self.wait()
        self.play(FadeOut(hl0))

        # "Similarly, 12 students own one pet each, 5 students own two
        #  pets each, and finally, only one student owns three pets."
        for i in (1, 2, 3):
            hl = SurroundingRectangle(table_dict["rows"][i]).set_color(GROUP_COLORS0[i])
            self.play(ShowCreation(hl))
            self.wait(0.4)
            self.play(FadeOut(hl))
        self.wait()

        # ------------------------------------------------------
        # "Now we are asked to find the median number of pets owned
        #  by these students. So, how do we do that?"
        # ------------------------------------------------------
        median_q = VGroup(
            Text("Median", font_size=44),
            Text("?", font_size=50),
        ).set_color(QUESTION_COLOR).arrange(RIGHT, buff=0.15)
        median_q.next_to(table_dict["border"], LEFT, buff=1.0)

        self.play(Write(median_q))
        self.play(median_q.animate.shift(UP * 0.2), rate_func=there_and_back, run_time=1.2)
        self.wait()
        self.play(FadeOut(median_q))

        # ------------------------------------------------------
        # "To find the median, we first need to calculate something
        #  called the cumulative frequency."
        #  -> move table left, reveal the 3rd column with "Cumulative
        #     Frequency?" then drop the "?"
        # ------------------------------------------------------
        full_table = VGroup(
            table_dict["header"], table_dict["rows"],
            table_dict["border"], table_dict["v_line"], table_dict["h_lines"],
        )
        self.play(full_table.animate.to_edge(2.5*RIGHT, buff=1.0))

        table_dict["h3_full"].next_to(table_dict["header"], RIGHT, buff=0.4).shift(DOWN*0.1)
        for cum, row in zip(table_dict["cum_texts"], table_dict["rows"]):
            cum.next_to(row, RIGHT, buff=2.2)

        border_full, v_line2, h_lines_full = build_third_column_frame(table_dict)

        self.play(
            FadeOut(table_dict["border"]),  FadeOut(table_dict["h_lines"]),
            FadeIn(table_dict["h3_full"]),
            ShowCreation(border_full), ShowCreation(v_line2), ShowCreation(h_lines_full),
        )
        self.wait()

        # drop the "?" -- the header label itself stays permanently
        self.play(FadeOut(table_dict["h3_q"]))
        self.wait()

        # ------------------------------------------------------
        # "But what exactly is cumulative frequency? To understand the
        #  idea, let's imagine that instead of having the information
        #  organised in a table, we wrote the data out as a complete
        #  list."
        # ------------------------------------------------------
        data_values = [0] * 11 + [1] * 12 + [2] * 5 + [3] * 1  # 29 values

        data_texts = VGroup(*[
            Text(str(v), font_size=28).set_color(BLACK) for v in data_values
        ])
        data_texts.arrange_in_grid(n_rows=5, n_cols=6, h_buff = 0.68, v_buff=0.9)
        data_texts.to_edge(LEFT, buff=1.3)

        zeros = data_texts[0:11]
        ones = data_texts[11:23]
        twos = data_texts[23:28]
        threes = data_texts[28:29]

        # "The first 11 students own 0 pets, so we would write eleven zeros."
        self.play(LaggedStart(*[FadeIn(t) for t in zeros], lag_ratio=0.08))
        self.wait()

        # "After that come the 12 students who own 1 pet each, so we
        #  would write twelve ones."
        self.play(LaggedStart(*[FadeIn(t) for t in ones], lag_ratio=0.08))
        self.wait()

        # "Next, we would write five twos, because five students own
        #  2 pets."
        self.play(LaggedStart(*[FadeIn(t) for t in twos], lag_ratio=0.08))
        self.wait()

        # "And finally, we would write a single 3, representing the
        #  one student who owns 3 pets."
        self.play(FadeIn(threes[0]))
        self.wait()

        # ------------------------------------------------------
        # "Now notice what happens if we start counting our way
        #  through the list."
        #  -> reveal the numbered 6x10 grid: numbering cells and the
        #     matching data cells appear together.
        # ------------------------------------------------------
        list_table = create_numbered_list_table(data_values)
        list_table["group"].move_to(data_texts.get_center())

        self.play(
            ReplacementTransform(data_texts, list_table["data_cells_texts"], path_func=bubbly_path),
            FadeIn(list_table["cell_rects"]),
            FadeIn(list_table["numbering_texts"]),
        )
        self.wait()

        # "The first 11 values are zeros. This means that up to this
        #  point, we have counted 11 students."
        box_11 = VGroup(
            SurroundingRectangle(list_table["data_cells_texts"][0:6]).set_color(GROUP_COLORS0[0]),
            SurroundingRectangle(list_table["data_cells_texts"][6:11]).set_color(GROUP_COLORS0[0]))
        box_11_n = SurroundingRectangle(list_table["numbering_texts"][10]).set_color(GROUP_COLORS[3])
        self.play(LaggedStart(ShowCreation(box_11), ShowCreation(box_11_n), lag_ratio=0.4))
        self.wait()
        self.play(TransformFromCopy(list_table["numbering_texts"][10], table_dict["cum_texts"][0]))
        self.wait()
        self.play(FadeOut(box_11), FadeOut(box_11_n))

        #"When we include the students who own 1 pet, the total rises
         #to 23 students."
        box_23 = VGroup(
            SurroundingRectangle(list_table["data_cells_texts"][0:6]),
            SurroundingRectangle(list_table["data_cells_texts"][6:12]),
            SurroundingRectangle(list_table["data_cells_texts"][12:18]),
            SurroundingRectangle(list_table["data_cells_texts"][18:23])).set_color(GROUP_COLORS0[1])
        box_23_n = SurroundingRectangle(list_table["numbering_texts"][22]).set_color(GROUP_COLORS[2])
        self.play(LaggedStart(ShowCreation(box_23), ShowCreation(box_23_n), lag_ratio=0.4))
        self.wait()
        self.play(TransformFromCopy(list_table["numbering_texts"][22], table_dict["cum_texts"][1]))
        self.wait()
        self.play(FadeOut(box_23), FadeOut(box_23_n))

        # "Including the students who own 2 pets takes the total to
        #  28 students."
        box_28 = VGroup(
            SurroundingRectangle(list_table["data_cells_texts"][0:6]),
            SurroundingRectangle(list_table["data_cells_texts"][6:12]),
            SurroundingRectangle(list_table["data_cells_texts"][12:18]),
            SurroundingRectangle(list_table["data_cells_texts"][18:24]),
            SurroundingRectangle(list_table["data_cells_texts"][24:28])
            ).set_color(GROUP_COLORS0[2])
        box_28_n = SurroundingRectangle(list_table["numbering_texts"][27]).set_color(GROUP_COLORS[1])
        self.play(LaggedStart(ShowCreation(box_28), ShowCreation(box_28_n), lag_ratio=0.4))
        self.wait()
        self.play(TransformFromCopy(list_table["numbering_texts"][27], table_dict["cum_texts"][2]))
        self.wait()
        self.play(FadeOut(box_28), FadeOut(box_28_n))

        # "And finally, including the last student gives a total of
        #  29 students."
        box_29 = VGroup(
            SurroundingRectangle(list_table["data_cells_texts"][0:6]),
            SurroundingRectangle(list_table["data_cells_texts"][6:12]),
            SurroundingRectangle(list_table["data_cells_texts"][12:18]),
            SurroundingRectangle(list_table["data_cells_texts"][18:24]),
            SurroundingRectangle(list_table["data_cells_texts"][24:29]),
            ).set_color(GROUP_COLORS0[3])
        box_29_n = SurroundingRectangle(list_table["numbering_texts"][28]).set_color(GROUP_COLORS[0])
        self.play(LaggedStart(ShowCreation(box_29), ShowCreation(box_29_n), lag_ratio=0.4))
        self.wait()
        self.play(TransformFromCopy(list_table["numbering_texts"][28], table_dict["cum_texts"][3]))
        self.wait()
        self.play(FadeOut(box_29), FadeOut(box_29_n))

        # "These running totals are called cumulative frequencies."
        rects = [SurroundingRectangle(c).set_color("#978F66") for c in table_dict["cum_texts"]]
        
        # 2. Play the creation animation using the saved variable
        self.play(LaggedStart(*[ShowCreation(r) for r in rects], lag_ratio=0.25, run_time=2.5))
        self.wait(1)
        self.play(FadeOut(VGroup(*rects)))
        self.wait(2)

       # ============================================================
        #  FINDING THE MEDIAN FROM THE CUMULATIVE FREQUENCIES
        # ============================================================
        # "Having calculated the cumulative frequencies, how can we use
        #  them to find the median? Remember, the median is the value
        #  that sits exactly in the middle of the data. Since there are
        #  29 students altogether, we need to find the position of the
        #  middle value. Because 29 is an odd number, we can find the
        #  middle position by adding 1 to the total number of values
        #  and dividing by 2."
        #  -> write "Odd:" below the table, then the (n+1)/2 formula
        # ------------------------------------------------------------
        odd_label = Text("Odd:", font_size=36).set_color(BLACK)
        position_formula = Tex(r"\frac{n+1}{2}", font_size=44).set_color(BLACK)
        odd_group = VGroup(odd_label, position_formula).arrange(RIGHT, buff=0.35)
        odd_group.next_to(border_full, DOWN, buff=0.5)
 
        self.play(Write(odd_label))
        self.wait()
        self.play(Write(position_formula))
        self.wait(2)
 
        # "So, 29 plus 1 gives us 30."
        n_sub = Tex(r"\frac{29+1}{2}", font_size=44).set_color(BLACK).move_to(position_formula)
        self.play(Transform(position_formula, n_sub))
        self.wait()
 
        thirty_over_2 = Tex(r"\frac{30}{2}", font_size=44).set_color(BLACK).move_to(position_formula)
        self.play(Transform(position_formula, thirty_over_2))
        self.wait()
 
        # "And 30 divided by 2 is 15."
        equals_15 = VGroup(
            Text("=", font_size=44).set_color(BLACK),
            Text("15", font_size=44).set_color(CUM_COLOR),
        ).arrange(RIGHT, buff=0.2)
        equals_15.next_to(position_formula, RIGHT, buff=0.3)
        self.play(Write(equals_15))
        self.wait()
 
        # "This tells us that the median is the 15th value in the list."
        self.wait()
 
        # "And looking at the list, the 15th value is 1, which is our
        #  median."
        highlight_15 = SurroundingRectangle(
            VGroup(list_table["numbering_texts"][14], list_table["data_cells_texts"][14]),
            buff=0.08,
        ).set_color("#DD9E59")
        self.play(ShowCreation(highlight_15))
        self.wait(2)
 
        # ------------------------------------------------------------
        # "Now, instead of writing out all 29 values and counting our
        #  way to the 15th position, we can use the cumulative
        #  frequency column to locate it much more quickly."
        #  -> drop the list grid, bring the table (with its working)
        #     to the centre, highlight the cumulative-frequency column
        # ------------------------------------------------------------
        self.play(FadeOut(highlight_15), FadeOut(list_table["group"]))
        self.wait()
        table_dict["h3_full"][1].set_opacity(0)  # hide the "?" in the header
        table_and_calc = VGroup(
            table_dict["header"], table_dict["rows"], table_dict["cum_texts"],
            table_dict["h3_full"], border_full, table_dict["v_line"], v_line2, h_lines_full,
            odd_label, position_formula, equals_15,
        )
        self.play(table_and_calc.animate.move_to(ORIGIN).shift(DOWN*0.2))
        self.play(VGroup(odd_label, position_formula, equals_15).animate.shift(LEFT*0.5))
        self.wait(2)
 
        cum_col_highlight = SurroundingRectangle(
            VGroup(table_dict["h3_full"], table_dict["cum_texts"]), buff=0.1
        ).set_color("#452829")
        self.play(ShowCreation(cum_col_highlight))
        self.wait(2)
 
        # "Notice that the cumulative frequency reaches 11 at the value
        #  0. This means the first 11 positions in the list are
        #  occupied by zeros."
        row0_highlight = VGroup(SurroundingRectangle(table_dict["rows"][0][0], buff=0.12),
                               SurroundingRectangle(table_dict["cum_texts"][0], buff=0.12)).set_color(GROUP_COLORS0[0])
        range_label_0 = Text("1 —— 11", font_size=35).set_color(GROUP_COLORS0[0])
        range_label_0.next_to(row0_highlight, RIGHT, buff=1)
 
        self.play(FadeOut(cum_col_highlight), ShowCreation(row0_highlight))
        self.wait()
        self.play(FadeIn(range_label_0))
        self.wait(2)
 
        # "The next cumulative frequency is 23 at the value 1. This
        #  tells us that positions 12 all the way up to 23 are occupied
        #  by ones."
        row1_highlight =  VGroup(SurroundingRectangle(table_dict["rows"][1][0], buff=0.12),
                               SurroundingRectangle(table_dict["cum_texts"][1], buff=0.12)).set_color(GROUP_COLORS0[1])
        range_label_1 = Text("12 —— 23", font_size=35).set_color(GROUP_COLORS0[1])
        range_label_1.next_to(row1_highlight, RIGHT, buff=1)
 
        self.play(
            FadeOut(row0_highlight), FadeOut(range_label_0),
            ShowCreation(row1_highlight),
        )
        self.wait(2)
        self.play(FadeIn(range_label_1))
        self.wait()
 
        # "Since the 15th position lies between 12 and 23, the 15th
        #  value must be 1."
        pos_15_marker = equals_15[1].copy()
        pos_15_marker.next_to(range_label_1, DOWN, buff=0.3)
        self.play(TransformFromCopy(equals_15[1], pos_15_marker))
        self.wait()
 
        between_box = SurroundingRectangle(
            VGroup(range_label_1, pos_15_marker), buff=0.15
        ).set_color("#B77466")
        self.play(ShowCreation(between_box))
        self.wait(2)
 
        # ------------------------------------------------------------
        # "Therefore, the median number of pets owned is 1."
        # ------------------------------------------------------------
        self.play(
            FadeOut(between_box), FadeOut(pos_15_marker),
            FadeOut(range_label_1), FadeOut(row1_highlight),
        )
 
        median_label = Text("Median = ", font_size=40).set_color(BLACK)
        median_value = table_dict["rows"][1][0].copy()
        median_conclusion = VGroup(median_label, median_value).arrange(RIGHT, buff=0.2)
        median_conclusion.next_to(table_and_calc, UP, buff=0.6)
 
        self.play(Write(median_label), TransformFromCopy(table_dict["rows"][1][0], median_value))
        self.wait()
 
        final_box = SurroundingRectangle(median_conclusion, buff=0.2).set_color("#116CD3")
        self.play(ShowCreation(final_box))
        self.wait(2)



class MedianSiblingsExample(InteractiveScene):
    """
    "Now let's try a question." A class of 31 students, siblings
    frequency table. This example builds the cumulative frequency by
    running addition directly on the table (no expanded-list device --
    that concept was already taught in MedianCumulativeFrequency), then
    finds the median using the same (n+1)/2 procedure.
 
    Reuses create_pets_table() and build_third_column_frame() exactly
    as already defined in this file -- create_pets_table() hardcodes
    its first-column header as "No. of Pets", so this scene swaps that
    label in place (via .become()) and rebuilds the border/divider/
    row-lines that depend on its width, rather than editing the
    function itself.
    """
 
    def construct(self):
        grid = NumberPlane(
            axis_config={"stroke_color": GREY, "stroke_opacity": 0.3},
            background_line_style={"stroke_color": GREY, "stroke_width": 2, "stroke_opacity": 0.3},
        )
        self.add(grid)
 
        # ------------------------------------------------------
        # "A class of 31 students was asked how many siblings they
        #  have. The results are organised in this frequency table."
        # ------------------------------------------------------
        numbers = [0, 1, 2, 3, 4]
        freqs = [4, 9, 11, 5, 2]
        cum_freqs = [4, 13, 24, 29, 31]
 
        table_dict = create_pets_table(numbers, freqs, cum_freqs)
 
        # create_pets_table() hardcodes its first column header as
        # "No. of Pets"; since that function can't be touched, swap
        # the label here and rebuild the border/divider/row-lines that
        # depend on its width, so nothing overlaps the new (wider) text.
        table_dict["header"][0].become(Text("No. of Siblings", font_size=34).set_color(BLACK))
        table_dict["header"].arrange(RIGHT, buff=0.8)
 
        table_content = VGroup(table_dict["header"], table_dict["rows"])
        table_content.arrange(DOWN, buff=0.6)
 
        table_dict["border"].become(
            SurroundingRectangle(table_content, buff=0.2).set_color(TABLE_COLOR)
        )
 
        col0_right = table_dict["header"][0].get_right()[0]
        col1_left = table_dict["header"][1].get_left()[0]
        x_div = (col0_right + col1_left) / 2
        table_dict["v_line"].become(
            Line(
                np.array([x_div, table_dict["border"].get_top()[1], 0]),
                np.array([x_div, table_dict["border"].get_bottom()[1], 0]),
            ).set_color(TABLE_COLOR)
        )
 
        for row, h_line in zip(table_dict["rows"], table_dict["h_lines"]):
            h_line.become(
                Line(table_dict["border"].get_left(), table_dict["border"].get_right())
                .move_to(row.get_top() + UP * 0.28)
                .set_color(TABLE_COLOR)
            )
 
        VGroup(
            table_dict["header"], table_dict["rows"],
            table_dict["border"], table_dict["v_line"], table_dict["h_lines"],
        ).move_to(ORIGIN)
 
        self.play(Write(table_dict["header"]))
        self.play(LaggedStart(*[Write(row) for row in table_dict["rows"]], lag_ratio=0.3, run_time=1.6))
        self.play(
            ShowCreation(table_dict["border"]),
            ShowCreation(table_dict["v_line"]),
            ShowCreation(table_dict["h_lines"]),
        )
        self.wait()
 
        # ------------------------------------------------------
        # "We are asked to find the median number of siblings. So, how
        #  do we do that? Just like before, our first step is to
        #  calculate the cumulative frequency."
        #  -> reveal the 3rd column ("Cumulative Frequency?" then drop
        #     the "?"), same device as the pets example.
        # ------------------------------------------------------
        table_dict["h3_full"].next_to(table_dict["header"], RIGHT, buff=0.4)
        for cum, row in zip(table_dict["cum_texts"], table_dict["rows"]):
            cum.next_to(row, RIGHT, buff=1.8)

        border_full, v_line2, h_lines_full = build_third_column_frame(table_dict)

        self.play(
            FadeOut(table_dict["border"]), FadeOut(table_dict["h_lines"]),
            FadeIn(table_dict["h3_full"][0]),
            ShowCreation(border_full), ShowCreation(v_line2), ShowCreation(h_lines_full),
        )
        self.wait()
        self.play(FadeOut(table_dict["h3_q"]))
        self.wait()

        # re-centre the whole 3-column table now that it has grown
        full_3col_table = VGroup(
            table_dict["header"], table_dict["rows"], 
            table_dict["h3_full"][0], table_dict["v_line"], v_line2,
            border_full, h_lines_full,
        )
        self.play(full_3col_table.animate.move_to(ORIGIN))
        self.wait()

        # ------------------------------------------------------
        # "The first cumulative frequency is simply 4."
        # ------------------------------------------------------
        self.play(TransformFromCopy(table_dict["rows"][0][1], table_dict["cum_texts"][0]))
        self.wait()

        # ------------------------------------------------------
        # "For the second row, we add 9 to the previous cumulative
        #  frequency of 4. This gives us 13."
        # "Next, we add 11 to 13, giving us 24."
        # "Then we add 5 to 24, which gives us 29."
        # "And finally, we add 2 to 29, giving us 31."
        #  -> a small running-addition "scratch pad" below the table,
        #     reused for each of the 4 steps.
        # ------------------------------------------------------
        for i in range(1, len(freqs)):
            prev_cum = table_dict["cum_texts"][i - 1]
            freq_val = table_dict["rows"][i][1]
            new_cum_value = cum_freqs[i]

            prev_copy = prev_cum.copy()
            freq_copy = freq_val.copy()
            plus = Text("+", font_size=32).set_color(BLACK)
            equals = Text("=", font_size=32).set_color(BLACK)
            result = Text(str(new_cum_value), font_size=32).set_color(CUM_COLOR)

            equation = VGroup(freq_copy, plus, prev_copy, equals, result).arrange(RIGHT, buff=0.2)
            equation.next_to(border_full, DOWN, buff=0.8)

            self.play(
                TransformFromCopy(prev_cum, prev_copy),
                TransformFromCopy(freq_val, freq_copy),
                Write(plus),
            )
            self.wait(0.3)
            self.play(Write(equals), Write(result))
            self.wait(0.5)

            self.play(TransformFromCopy(result, table_dict["cum_texts"][i]))
            self.play(FadeOut(prev_copy), FadeOut(plus), FadeOut(freq_copy), FadeOut(equals), FadeOut(result))
        
        self.wait()
        # "So the cumulative frequencies are 4, 13, 24, 29 and 31."
        # 1. Create the list of rectangles and save them to a variable
        rects = [SurroundingRectangle(c).set_color("#978F66") for c in table_dict["cum_texts"]]

        # 2. Play the creation animation using the saved variable
        self.play(LaggedStart(*[ShowCreation(r) for r in rects], lag_ratio=0.5, run_time=2.5))

        self.wait(2)
        # ------------------------------------------------------
        # "Now that we have calculated the cumulative frequencies, we
        #  can find the median. There are 31 values altogether. Since
        #  31 is an odd number, we find the middle position by adding
        #  1 to the total and dividing by 2."
        # ------------------------------------------------------
        odd_label = Text("Odd:", font_size=36).set_color(BLACK)
        position_formula = Tex(r"\frac{n+1}{2}", font_size=44).set_color(BLACK)
        odd_group = VGroup(odd_label, position_formula).arrange(RIGHT, buff=0.35)
        odd_group.next_to(border_full, DOWN, buff=0.4)

        self.play(Write(odd_label))
        self.wait()
        self.play(Write(position_formula))
        self.wait()

        # "So, 31 plus 1 gives us 32."
        n_sub = Tex(r"\frac{31+1}{2}", font_size=44).set_color(BLACK).move_to(position_formula)
        self.play(Transform(position_formula, n_sub))
        self.wait()

        thirty2_over_2 = Tex(r"\frac{32}{2}", font_size=44).set_color(BLACK).move_to(position_formula)
        self.play(Transform(position_formula, thirty2_over_2))
        self.wait()

        # "And 32 divided by 2 gives us 16."
        equals_16 = VGroup(
            Text("=", font_size=44).set_color(BLACK),
            Text("16", font_size=44).set_color(CUM_COLOR),
        ).arrange(RIGHT, buff=0.2)
        equals_16.next_to(position_formula, RIGHT, buff=0.3)
        self.play(Write(equals_16))
        self.play(FadeOut(VGroup(*rects)))
        self.wait()

        # "This tells us that the median is the 16th value in the
        #  ordered list."
        box_16 = SurroundingRectangle(equals_16[1], buff=0.1).set_color("#116CD3")
        self.play(ShowCreation(box_16))
        self.wait()
        self.play(FadeOut(box_16))
        self.wait(2)

        # # ------------------------------------------------------
        # # "Now we need to work out which value occupies the 16th
        # #  position. Notice that the cumulative frequency reaches 13
        # #  at a value of 1. This means that the first 13 positions in
        # #  the list are occupied by values up to 1."
        # # ------------------------------------------------------
        row1_highlight = VGroup(SurroundingRectangle(table_dict["rows"][1][0], buff=0.12),
                               SurroundingRectangle(table_dict["cum_texts"][1], buff=0.12)).set_color(GROUP_COLORS0[1])
        range_label_1 = Text("5 —— 13", font_size=35).set_color(GROUP_COLORS0[0])
        range_label_1.next_to(row1_highlight, RIGHT, buff=1)

        self.play(FadeIn(row1_highlight))
        self.wait(2)
        self.play(FadeIn(range_label_1))
        self.wait()

        # "The next cumulative frequency is 24 at a value of 2. This
        #  tells us that positions 14 through to 24 are occupied by
        #  the value 2."
        row2_highlight = VGroup(SurroundingRectangle(table_dict["rows"][2][0], buff=0.12),
                               SurroundingRectangle(table_dict["cum_texts"][2], buff=0.12)).set_color(GROUP_COLORS[1])
        range_label_2 = Text("14 —— 24", font_size=35).set_color(GROUP_COLORS0[1])
        range_label_2.next_to(row2_highlight, RIGHT, buff=1)

        self.play(FadeOut(row1_highlight), FadeOut(range_label_1), FadeIn(row2_highlight))
        self.wait(2)
        self.play(FadeIn(range_label_2))
        self.wait()

        # "Since the 16th position lies between 14 and 24, the 16th
        #  value must be 2."
        pos_16_marker = equals_16[1].copy()
        pos_16_marker.next_to(range_label_2, DOWN, buff=0.3)
        self.play(TransformFromCopy(equals_16[1], pos_16_marker))
        self.wait()

        between_box = SurroundingRectangle(
            VGroup(range_label_2, pos_16_marker), buff=0.15
        ).set_color("#827148")
        self.play(ShowCreation(between_box))
        self.wait(2)

        # ------------------------------------------------------
        # "Therefore, the median number of siblings is 2."
        # ------------------------------------------------------

        median_label = Text("Median = ", font_size=40).set_color(BLACK)
        median_value = table_dict["rows"][2][0].copy()
        median_conclusion = VGroup(median_label, median_value).arrange(RIGHT, buff=0.2)
        median_conclusion.next_to(full_3col_table, UP, buff=0.6)

        self.play(Write(median_label), TransformFromCopy(table_dict["rows"][2][0], median_value))
        self.wait()

        final_box = SurroundingRectangle(median_conclusion, buff=0.2).set_color("#116CD3")
        self.play(ShowCreation(final_box))
        self.wait(2)

        # ============================================================
        #  ODD vs EVEN NUMBER OF VALUES
        # ============================================================
        # "(Fade everything)"
        # ------------------------------------------------------------
        self.play(
            FadeOut(table_dict["header"]), FadeOut(table_dict["rows"]),
            FadeOut(table_dict["cum_texts"]), FadeOut(table_dict["h3_full"][0]),
            FadeOut(table_dict["v_line"]), FadeOut(v_line2),
            FadeOut(border_full), FadeOut(h_lines_full),
            FadeOut(odd_label), FadeOut(position_formula), FadeOut(equals_16),
            FadeOut(median_label), FadeOut(median_value), FadeOut(final_box),
            FadeOut(between_box), FadeOut(pos_16_marker), FadeOut(range_label_2), FadeOut(row2_highlight)
        )
        self.wait()

        # "Up until now, all of our examples have contained an odd
        #  number of values. But what happens if the total number of
        #  values is even? To understand this, let's compare an odd
        #  data set with an even one."
        bridge_title = Text("Odd vs Even Number of Values", font_size=38).set_color(BLACK)
        self.play(Write(bridge_title))
        self.wait(2)
        self.play(FadeOut(bridge_title))

        # ------------------------------------------------------------
        # "(Show the two ordered lists ... a row above the data with
        #  dark brown coloring and white text showing positions. Cross
        #  out numbers from both ends until only the middle values
        #  remain.)"
        # ------------------------------------------------------------
        def make_ordered_list_row(data_values, cell_width=0.875, cell_height=0.625):
            """Single-row (position row above, data row below) list --
            same visual language as the numbered pets/siblings grid
            earlier (dark-filled numbering cells), but as one row."""
            pos_rects = VGroup()
            pos_texts = VGroup()
            data_rects = VGroup()
            data_texts = VGroup()

            for i, v in enumerate(data_values):
                x = i * cell_width

                pos_rect = Rectangle(width=cell_width, height=cell_height)
                pos_rect.set_fill(CELL_FILL, opacity=1)
                pos_rect.set_stroke(CELL_FILL, width=1)
                pos_rect.move_to(np.array([x, cell_height, 0]))
                pos_rects.add(pos_rect)

                pos_text = Text(str(i + 1), font_size=22).set_color(WHITE)
                pos_text.move_to(pos_rect.get_center())
                pos_texts.add(pos_text)

                data_rect = Rectangle(width=cell_width, height=cell_height)
                data_rect.set_stroke(BLACK, width=1)
                data_rect.move_to(np.array([x, 0, 0]))
                data_rects.add(data_rect)

                data_text = Text(str(v), font_size=26).set_color(BLACK)
                data_text.move_to(data_rect.get_center())
                data_texts.add(data_text)

            group = VGroup(pos_rects, pos_texts, data_rects, data_texts)
            group.center()

            return {
                "group": group, "pos_rects": pos_rects, "pos_texts": pos_texts,
                "data_rects": data_rects, "data_texts": data_texts,
            }

        def make_cross(mobject, color="#FA3108"):
            """A simple X mark spanning a mobject's bounding box."""
            tl, tr = mobject.get_corner(UL), mobject.get_corner(UR)
            bl, br = mobject.get_corner(DL), mobject.get_corner(DR)
            line1 = Line(tl, br).set_color(color).set_stroke(width=3.5).scale(1.5)
            return VGroup(line1)

        odd_data = [7, 8, 8, 13, 17, 19, 20, 21, 21]
        even_data = [3, 3, 4, 6, 8, 9, 9, 11, 12, 13]

        odd_list = make_ordered_list_row(odd_data)
        even_list = make_ordered_list_row(even_data)

        odd_list["group"].move_to(UP * 1)
        even_list["group"].move_to(DOWN * 1)

        odd_tag = Text("Odd:", font_size=32).set_color(BLACK)
        odd_tag.next_to(odd_list["group"], LEFT, buff=0.5)

        even_tag = Text("Even:", font_size=32).set_color(BLACK)
        even_tag.next_to(even_list["group"], LEFT, buff=0.5)

        self.play(FadeIn(odd_tag), FadeIn(odd_list["data_rects"]), FadeIn(odd_list["data_texts"]),
                  FadeIn(odd_list["pos_rects"]), FadeIn(odd_list["pos_texts"]))
        self.wait()

        self.play(FadeIn(even_tag), FadeIn(even_list["data_rects"]), FadeIn(even_list["data_texts"]),
                  FadeIn(even_list["pos_rects"]), FadeIn(even_list["pos_texts"]))
        self.wait(2)

        # cross out from both ends, working inward, in parallel on both lists
        pairs_odd = [(0, 8), (1, 7), (2, 6), (3, 5)]
        pairs_even = [(0, 9), (1, 8), (2, 7), (3, 6)]
        red_crosses = []
        for (lo, ro), (le, re) in zip(pairs_odd, pairs_even):
            cross_o1 = make_cross(VGroup(odd_list["data_texts"][lo]))
            cross_o2 = make_cross(VGroup(odd_list["data_texts"][ro]))
            cross_e1 = make_cross(VGroup(even_list["data_texts"][le]))
            cross_e2 = make_cross(VGroup(even_list["data_texts"][re]))
            red_crosses.extend([cross_o1, cross_o2, cross_e1, cross_e2])
            self.play(
                ShowCreation(cross_o1), ShowCreation(cross_o2),
                ShowCreation(cross_e1), ShowCreation(cross_e2),
                run_time=0.6,
            )

        self.wait()
        red_crosses_group = VGroup(*red_crosses)

        # ------------------------------------------------------------
        # "Notice that for the odd data set, there is a single value
        #  sitting exactly in the middle. In this case, the median is
        #  simply 17."
        # ------------------------------------------------------------
        odd_middle_box = SurroundingRectangle(
            VGroup(odd_list["pos_texts"][4], odd_list["data_texts"][4]), buff=0.08
        ).set_color("#116CD3")
        self.play(ShowCreation(odd_middle_box))
        self.wait()

        odd_median_label = Text("Median = 17", font_size=30).set_color("#116CD3")
        odd_median_label.next_to(odd_list["group"], RIGHT, buff=0.6)
        self.play(Write(odd_median_label))
        self.wait(2)

        # ------------------------------------------------------------
        # "But for the even data set, something different happens.
        #  Instead of one middle value, we end up with two values in
        #  the middle: 8 and 9. So, which one should we choose as the
        #  median? The answer is that we don't choose either of them.
        #  Instead, we take the average of the two middle values."
        # ------------------------------------------------------------
        even_middle_box = SurroundingRectangle(
            VGroup(even_list["pos_texts"][4], even_list["data_texts"][4],
                   even_list["pos_texts"][5], even_list["data_texts"][5]),
            buff=0.08,
        ).set_color("#116CD3")
        self.play(ShowCreation(even_middle_box))
        self.wait()

        even_median_q = Text("Median = ?", font_size=30).set_color(QUESTION_COLOR)
        even_median_q.next_to(even_list["group"], RIGHT, buff=0.6)
        self.play(Write(even_median_q))
        self.play(even_median_q.animate.shift(UP * 0.15), rate_func=there_and_back, run_time=1.0)
        self.wait()
        self.play(FadeOut(even_median_q))

        # ------------------------------------------------------------
        # "(Bring down copies of 8 and 9. Show 8 + 9 = 17, then divide
        #  by 2 to get 8.5.)"
        #  "Adding 8 and 9 gives us 17."
        # ------------------------------------------------------------
        eight_copy = even_list["data_texts"][4].copy().scale(1.2)
        nine_copy = even_list["data_texts"][5].copy().scale(1.2)
        plus_sign_a = Text("+", font_size=36).set_color(BLACK)

        sum_setup_even = VGroup(eight_copy, plus_sign_a, nine_copy).arrange(RIGHT, buff=0.3)
        sum_setup_even.next_to(even_list["group"], DOWN, buff=0.5)

        self.play(
            TransformFromCopy(even_list["data_texts"][4], eight_copy),
            TransformFromCopy(even_list["data_texts"][5], nine_copy),
            Write(plus_sign_a),
        )
        self.wait()

        equals_sign_a = Text("=", font_size=36).set_color(BLACK)
        seventeen_val = Text("17", font_size=36).set_color(CUM_COLOR)
        equals_17_group = VGroup(equals_sign_a, seventeen_val).arrange(RIGHT, buff=0.15)
        equals_17_group.next_to(sum_setup_even, RIGHT, buff=0.3)
        self.play(Write(equals_17_group))
        self.wait()

        # "Dividing by 2 gives us 8.5."
        self.play(FadeOut(sum_setup_even), FadeOut(equals_sign_a))
        self.play(seventeen_val.animate.next_to(even_list["group"], DOWN, buff=1.0))

        frac_line_a = Line(LEFT * 0.35, RIGHT * 0.35).set_color(BLACK)
        frac_line_a.next_to(seventeen_val, DOWN, buff=0.15)
        two_denom_a = Text("2", font_size=36).set_color(BLACK)
        two_denom_a.next_to(frac_line_a, DOWN, buff=0.15)

        self.play(ShowCreation(frac_line_a), Write(two_denom_a))
        self.wait()

        equals_word_a = Text("=", font_size=36).set_color(BLACK)
        eight_five_val = Text("8.5", font_size=36).set_color(CUM_COLOR)
        equals_85_group = VGroup(equals_word_a, eight_five_val).arrange(RIGHT, buff=0.15)
        equals_85_group.next_to(VGroup(seventeen_val, frac_line_a, two_denom_a), RIGHT, buff=0.3)
        self.play(Write(equals_85_group))
        self.wait()

        # "So the median of this data set is 8.5."
        median_85_box = SurroundingRectangle(eight_five_val, buff=0.1).set_color("#116CD3")
        self.play(ShowCreation(median_85_box))
        self.wait(2)

        # ------------------------------------------------------------
        # "Now we can see from the list that the middle values were at
        #  the 5th and 6th position, but you might be wondering, how
        #  did we know mathematically that the two middle values were
        #  at these two positions? To do that for an even number of
        #  values, we first divide the total by 2. In this case, 10
        #  divided by 2 is 5. Then we take the next position, which is
        #  6. Now using the data at these two positions and taking the
        #  average would give us the median."
        # ------------------------------------------------------------
        self.play(
            FadeOut(median_85_box), FadeOut(seventeen_val), FadeOut(frac_line_a),
            FadeOut(two_denom_a), FadeOut(equals_85_group),
        )
        self.wait()

        even_rule_label = Text("Even:", font_size=36).set_color(BLACK)
        even_rule_label.next_to(even_list["group"], DOWN, buff=0.7).shift(LEFT * 0.7)
        self.play(Write(even_rule_label))
        self.wait()

        pos_formula_general = Tex(r"\frac{n}{2}", font_size=44).set_color(BLACK)
        pos_formula_general.next_to(even_rule_label, RIGHT, buff=0.3)
        self.play(Write(pos_formula_general))
        self.wait()

        pos_formula_general_10 = Tex(r"\frac{10}{2}", font_size=44).set_color(BLACK).move_to(pos_formula_general)
        self.play(Transform(pos_formula_general, pos_formula_general_10))
        self.wait()

        equals_5_group = Text("= 5", font_size=44).set_color(CUM_COLOR)
        equals_5_group.next_to(pos_formula_general, RIGHT, buff=0.3)
        self.play(Write(equals_5_group))
        self.wait()

        next_pos_label = Text("next position = 6", font_size=32).set_color(CUM_COLOR)
        next_pos_label.next_to(pos_formula_general, DOWN, buff=0.4)
        self.play(Write(next_pos_label))
        self.wait(2)

        # ------------------------------------------------------------
        # "Having understood that, now let's return to our previous
        #  example involving the number of siblings."
        #  -> fade the odd/even comparison, bring back the frequency
        #     table
        # ------------------------------------------------------------
        self.play(
            FadeOut(odd_tag), FadeOut(odd_list["group"]), FadeOut(odd_median_label), FadeOut(odd_middle_box),
            FadeOut(even_tag), FadeOut(even_list["group"]), FadeOut(even_middle_box),
            FadeOut(even_rule_label), FadeOut(pos_formula_general), FadeOut(equals_5_group), FadeOut(next_pos_label),
                FadeOut(red_crosses_group),)
        self.wait()

        # "(Bring back the frequency table.)"
        self.play(FadeIn(full_3col_table), FadeIn(table_dict["cum_texts"]))
        self.wait(2)

        # ------------------------------------------------------------
        # "Previously, there were 31 students. Let's make the total
        #  even by changing the final frequency from 2 to 3. This
        #  increases the total number of students from 31 to 32."
        # ------------------------------------------------------------
        new_freq_val = Text("3", font_size=34).set_color(BLACK).move_to(table_dict["rows"][4][1])
        self.play(Transform(table_dict["rows"][4][1], new_freq_val))
        self.wait(2)

        # "As a result, the final cumulative frequency also changes
        #  from 31 to 32."
        new_cum_val = Text("32", font_size=34).set_color(CUM_COLOR).move_to(table_dict["cum_texts"][4])
        self.play(Transform(table_dict["cum_texts"][4], new_cum_val))
        self.wait(2)

        # ------------------------------------------------------------
        # "Now we need to find the median for this new data set. Since
        #  there are 32 values altogether, we begin by dividing 32 by
        #  2. This gives us 16. The next position is 17. So the median
        #  will be found by taking the average of the values at
        #  positions 16 and 17."
        # ------------------------------------------------------------
        even_label_siblings = Text("Even:", font_size=36).set_color(BLACK)
        pos_formula_siblings = Tex(r"\frac{n}{2}", font_size=44).set_color(BLACK)
        even_group_siblings = VGroup(even_label_siblings, pos_formula_siblings).arrange(RIGHT, buff=0.35)
        even_group_siblings.next_to(border_full, DOWN, buff=0.5)

        self.play(Write(even_label_siblings))
        self.wait()
        self.play(Write(pos_formula_siblings))
        self.wait()

        pos_formula_siblings_32 = Tex(r"\frac{32}{2}", font_size=44).set_color(BLACK).move_to(pos_formula_siblings)
        self.play(Transform(pos_formula_siblings, pos_formula_siblings_32))
        self.wait()

        equals_16_siblings = VGroup(
            Text("=", font_size=44).set_color(BLACK),
            Text("16", font_size=44).set_color(CUM_COLOR),
            Text(" , 17", font_size=44).set_color(CUM_COLOR),
        ).arrange(RIGHT, buff=0.2)
        equals_16_siblings.next_to(pos_formula_siblings, RIGHT, buff=0.3)
        self.play(Write(equals_16_siblings[0]), Write(equals_16_siblings[1]))
        self.wait()
        self.play(Write(equals_16_siblings[2]))
        self.wait()

        avg_positions_note = Text("Median = average of positions 16 & 17", font_size=32).set_color("#2E7670")
        avg_positions_note.next_to(full_3col_table, UP, buff=0.6)
        self.play(Write(avg_positions_note))
        self.wait(2)

        # ------------------------------------------------------------
        # "Now let's locate those positions using the cumulative
        #  frequency column. From the previous example, we know that
        #  positions 14 through to 24 are occupied by the value 2.
        #  This means that both the 16th position and the 17th
        #  position contain the value 2."
        # ------------------------------------------------------------
        row2_highlight_final = VGroup(
            SurroundingRectangle(table_dict["rows"][2][0], buff=0.12),
            SurroundingRectangle(table_dict["cum_texts"][2], buff=0.12),
        ).set_color("#254F22")
        range_label_2_final = Text("14 ——— 24", font_size=32).set_color("#2E7670")
        range_label_2_final.next_to(row2_highlight_final, RIGHT, buff=0.8)

        self.play(FadeIn(row2_highlight_final))
        self.wait()
        self.play(FadeIn(range_label_2_final))
        self.wait()

        positions_note_final = Text("16 & 17", font_size=30).set_color("#993131")
        positions_note_final.next_to(range_label_2_final, DOWN, buff=0.3)
        self.play(Write(positions_note_final))
        self.wait(2)

        # ------------------------------------------------------------
        # "So we calculate the average. 2 plus 2 equals 4. And 4
        #  divided by 2 equals 2. Therefore, the median number of
        #  siblings is 2."
        # ------------------------------------------------------------
        self.play(
            FadeOut(even_group_siblings), FadeOut(avg_positions_note),
            FadeOut(row2_highlight_final), FadeOut(range_label_2_final), FadeOut(positions_note_final),
            FadeOut(equals_16_siblings)
        )
        self.wait()

        two_copy_a = table_dict["rows"][2][0].copy()
        two_copy_b = table_dict["rows"][2][0].copy()
        plus_sign_b = Text("+", font_size=40).set_color(BLACK)

        sum_setup_final = VGroup(two_copy_a, plus_sign_b, two_copy_b).scale(1.2).arrange(RIGHT, buff=0.3)
        sum_setup_final.next_to(border_full, DOWN, buff=0.5)

        self.play(
            TransformFromCopy(table_dict["rows"][2][0], two_copy_a),
            TransformFromCopy(table_dict["rows"][2][0], two_copy_b),
            Write(plus_sign_b),
        )
        self.wait()

        equals_4_group = Text("= 4", font_size=40).set_color(CUM_COLOR)
        equals_4_group.next_to(sum_setup_final, RIGHT, buff=0.3)
        self.play(Write(equals_4_group))
        self.wait()

        self.play(FadeOut(sum_setup_final), FadeOut(equals_4_group[0]))
        four_val = equals_4_group[1]
        self.play(four_val.animate.next_to(border_full, DOWN, buff=0.5))

        frac_line_b = Line(LEFT * 0.3, RIGHT * 0.3).set_color(BLACK)
        frac_line_b.next_to(four_val, DOWN, buff=0.15)
        two_denom_b = Text("2", font_size=40).set_color(BLACK)
        two_denom_b.next_to(frac_line_b, DOWN, buff=0.15)
        self.play(ShowCreation(frac_line_b), Write(two_denom_b))
        self.wait()

        equals_2_group = Text("= 2", font_size=44).set_color(CUM_COLOR)
        equals_2_group.next_to(VGroup(four_val, frac_line_b, two_denom_b), RIGHT, buff=0.3)
        self.play(Write(equals_2_group))
        self.wait(2)

        # ------------------------------------------------------------
        # "Therefore, the median number of siblings is 2."
        # ------------------------------------------------------------
        median_label_final = Text("Median = ", font_size=40).set_color(BLACK)
        median_value_final = table_dict["rows"][2][0].copy()
        median_conclusion_final = VGroup(median_label_final, median_value_final).arrange(RIGHT, buff=0.2)
        median_conclusion_final.next_to(full_3col_table, UP, buff=0.6)

        self.play(Write(median_label_final), TransformFromCopy(table_dict["rows"][2][0], median_value_final))
        self.wait()

        final_answer_box = SurroundingRectangle(median_conclusion_final, buff=0.2).set_color("#116CD3")
        self.play(ShowCreation(final_answer_box))
        self.wait(2)
