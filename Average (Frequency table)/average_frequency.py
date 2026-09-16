from manimlib import *

class Dice(InteractiveScene):
    def construct(self):
        # Test
        image_path = Path(self.file_writer.output_directory, "D:\manim-master\Media\person_throwing_dice.png").resolve()
        image = TexturedSurface(Square3D(resolution=(101, 101)), image_path)
        image.set_shape(FRAME_WIDTH, FRAME_HEIGHT)
        image.set_shading(0.1, 0.1, 0.1)
        self.add(image)

        # Make waves
        frame = self.frame
        center = np.array([0.8, -1.04, 0])

        def wave(x, y, z, t):
            dist = get_dist(center, [x, y, z])
            scale = 0.025 * np.exp(-2 * dist * dist)
            nudge1 = scale * math.sin(2 * TAU * x - 5 * TAU * t)
            nudge2 = 3 * scale * math.sin(3 * TAU * y - 5 * TAU * t)
            return (x, y + nudge1, z + nudge2)

        frame.reorient(0, 0, 0, (0, 0, 0.0), 4.39)
        self.play(
            Homotopy(wave, image, rate_func=linear),
            frame.animate.to_default_state(),
            run_time=12,
        )

class Average(InteractiveScene):
    def construct(self):
        grid = NumberPlane(
            axis_config = {"stroke_color" : GREY, "stroke_opacity":0.3},
            background_line_style={"stroke_color": GREY, "stroke_width":2, "stroke_opacity":0.3})
        
        self.add(grid)

        unordered = [4,1,5,1,3,3,1,2,5,1,6,2,3,5,2,4,6,5,2,1]

        # Create unordered numbers
        unordered_mobs = VGroup(*[
            Text(str(n), font_size=40).set_color(BLACK)
            for n in unordered
        ])

        unordered_mobs.arrange_in_grid(n_rows=4, n_cols=5, buff=0.6)
        unordered_mobs.shift(1*UP + 4*LEFT)

        # Animate appearance
        self.wait()
        self.play(LaggedStart(*[
            FadeIn(num) for num in unordered_mobs
        ], lag_ratio=0.1))

        self.wait()

        rows0 = VGroup()

        for value in range(1,7):

            row_numbers = [Text(str(value), font_size=40).set_color(BLACK)
                           for n in unordered if n == value]

            row = VGroup(*row_numbers).arrange(RIGHT, buff=0.4)

            rows0.add(row)

        rows0.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        rows0.shift(0.5*UP + 4.5*LEFT)

        # transform unordered into grouped rows
        self.play(ReplacementTransform(unordered_mobs, rows0), run_time = 1.25, rate_func = smooth)

        self.wait()

        #________________________________________________

        # -------- Frequency Table --------
        #________________________________________________

        numbers = [1,2,3,4,5,6]
        freqs = [5,4,3,2,4,2]

        # Header
        h1 = Text("Number", font_size=36).set_color(BLACK)
        h2 = Text("Frequency", font_size=36).set_color(BLACK)
        header = VGroup(h1, h2).arrange(RIGHT, buff=1)

        # Rows
        rows = VGroup()
        for n, f in zip(numbers, freqs):

            num = Text(str(n), font_size=36).set_color(BLACK)
            frq = Text(str(f), font_size=36).set_color(BLACK)

            row = VGroup(num, frq).arrange(RIGHT, buff=2)
            rows.add(row)

        rows.arrange(DOWN, buff=0.5)

        # Combine header and rows
        table_content = VGroup(header, rows)
        table_content.arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        table_color = "#462802"
        # Create border rectangle
        border = SurroundingRectangle(table_content, buff=0.4).set_color(table_color)

        # Vertical separator
        v_line = Line(
            border.get_top() + LEFT*0.2,
            border.get_bottom() + LEFT*0.2
        ).set_color(table_color)

        # Horizontal lines
        h_lines = VGroup()
        for row in rows:
            line = Line(
                border.get_left(),
                border.get_right()
            ).move_to(row.get_top() + UP*0.28 + RIGHT*0.75).set_color(table_color)
            h_lines.add(line)

        table = VGroup(border, v_line, h_lines, table_content)

        # Position table on right side
        table.to_edge(RIGHT*1.2)

        # Animate
        self.play(Write(header))
        for row in rows:
            self.play(Write(row), run_time=0.3)

        self.play(
            ShowCreation(border),
            ShowCreation(v_line),
            ShowCreation(h_lines), run_time = 0.5
        )
        self.wait(2)

        dice_question_logo(self)
        self.wait()

        plus_rows = VGroup()
        for row in rows0:
            new_row = row.copy() 
            pluses = VGroup()
            for i in range(len(row)-1):
                plus = Text("+", font_size=36).set_color(BLACK)
                plus.move_to(
                    (row[i].get_right() + row[i+1].get_left())/2
                )
                pluses.add(plus)
            # add plus signs into THIS row
            end_plus = Text("+", font_size=36).set_color(BLACK)
            end_plus.next_to(new_row[-1], RIGHT, buff=0.15)
            end_plus.set_opacity(0)  # hidden initially
            new_row.add(*pluses, end_plus)
            plus_rows.add(new_row)

        plus_rows[-1].remove(plus_rows[-1][-1])

        # animate appearance
        self.play(LaggedStart(*[FadeIn(p) for p in plus_rows], lag_ratio= 0.05), FadeOut(rows0))

        first_row_pos = plus_rows[0].get_center()

        self.play(plus_rows.animate.arrange(RIGHT, buff=0.15).move_to(first_row_pos).shift(1.7*RIGHT + DOWN*2).scale(0.75),
                    )
        end_pluses = VGroup(*[row[-1] for row in plus_rows])

        self.play(end_pluses.animate.set_opacity(1))

        frac_line = Line(plus_rows.get_left(),plus_rows.get_right()).set_color(BLACK)
        frac_line.next_to(plus_rows, DOWN, buff=0.2)
        denominator = Text("20", font_size=30).set_color(BLACK)
        denominator.next_to(frac_line, DOWN, buff=0.2)

        self.play(ShowCreation(frac_line))
        self.play(Write(denominator))
        self.wait(2)

        dice2 = SurroundingRectangle(rows[1][0], color = "#750A0A")
        dice2_fr = SurroundingRectangle(rows[1][1], color = "#750A0A")
        box = SurroundingRectangle(plus_rows[1][1:6],color="#2E7670",buff=0.2).shift(LEFT*0.13)
        eight = Text("8", font_size=34).set_color("#454033")
        eight.next_to(box, UP, buff=0.2)
        eight_multiple = VGroup(Text("2 × 4 =", font_size=30), Text("8", font_size = 30)).arrange(RIGHT
                                                                ).set_color("#344F1F").next_to(rows[1][1], RIGHT)

        self.play(ShowCreation(dice2), ShowCreation(dice2_fr) )
        self.wait()
        self.play(ShowCreation(box))
        self.wait()
        self.play(Write(eight))
        self.wait()
        self.play(ShowCreation(eight_multiple))
        self.wait()

        dice1 = SurroundingRectangle(rows[0][0], color = "#750A0A")
        dice1_fr = SurroundingRectangle(rows[0][1], color = "#750A0A")
        box1 = SurroundingRectangle(plus_rows[0][1:6],color="#FF9001",buff=0.2).shift(LEFT*0.15)
        five = Text("5", font_size=34).set_color("#454033")
        five.next_to(box1, UP, buff=0.2)
        five_multiple = VGroup(Text("1 × 5 =", font_size=30), Text("5", font_size = 30)).arrange(RIGHT
                                                                        ).set_color("#344F1F").next_to(rows[0][1], RIGHT)        

        self.play(ShowCreation(dice1), ShowCreation(dice1_fr),
                    ShowCreation(box1))
        self.wait()
        self.play(Write(five_multiple))
        self.wait()
        self.play( Write(five))
        self.wait()

        dice3 = SurroundingRectangle(rows[2][0], color = "#750A0A")
        dice3_fr = SurroundingRectangle(rows[2][1], color = "#750A0A")
        box3 = SurroundingRectangle(plus_rows[2][1:4],color="#93637F",buff=0.2).shift(LEFT*0.1)
        nine = Text("9", font_size=34).set_color("#454033")
        nine.next_to(box3, UP, buff=0.2)
        nine_multiple = VGroup(Text("3 × 3 =", font_size=30), Text("9", font_size=30)).arrange(RIGHT
                                                        ).set_color("#344F1F").next_to(rows[2][1], RIGHT)        

        self.play(ShowCreation(dice3), ShowCreation(dice3_fr),
                    ShowCreation(box3))
        self.wait()
        self.play(Write(nine_multiple), Write(nine))
        self.wait()

        dice4 = SurroundingRectangle(rows[3][0], color = "#750A0A")
        dice4_fr = SurroundingRectangle(rows[3][1], color = "#750A0A")
        box4 = SurroundingRectangle(plus_rows[3][1:3],color="#B75E5A",buff=0.2).shift(LEFT*0.12)
        eight1 = Text("8", font_size=34).set_color("#454033")
        eight1.next_to(box4, UP, buff=0.2)
        eight1_multiple = VGroup(Text("4 × 2 =", font_size=30), Text("8", font_size=30)).arrange(RIGHT
                                                        ).set_color("#344F1F").next_to(rows[3][1], RIGHT) 
        
        dice5 = SurroundingRectangle(rows[4][0], color = "#750A0A")
        dice5_fr = SurroundingRectangle(rows[4][1], color = "#750A0A")
        box5 = SurroundingRectangle(plus_rows[4][1:6],color="#D21F2B",buff=0.2).shift(LEFT*0.12)
        twenty = Text("20", font_size=34).set_color("#454033")
        twenty.next_to(box5, UP, buff=0.2)
        twenty_multiple = VGroup(Text("5 × 4 =", font_size=30), Text("20", font_size=30)).arrange(RIGHT
                                                        ).set_color("#344F1F").next_to(rows[4][1], RIGHT)

        dice6 = SurroundingRectangle(rows[5][0], color = "#750A0A")
        dice6_fr = SurroundingRectangle(rows[5][1], color = "#750A0A")
        box6 = SurroundingRectangle(plus_rows[5][1:3],color="#7BB570",buff=0.2).shift(LEFT*0.12)
        twelve = Text("12", font_size=34).set_color("#454033")
        twelve.next_to(box6, UP, buff=0.2)
        twelve_multiple = VGroup(Text("6 × 2 =", font_size=30), Text("12", font_size=30)).arrange(RIGHT
                                                        ).set_color("#344F1F").next_to(rows[5][1], RIGHT) 
        
        self.play(ShowCreation(dice4), ShowCreation(dice4_fr),
                    ShowCreation(box4))
        self.play(Write(eight1_multiple), Write(eight1))
        self.wait()

        self.play(ShowCreation(dice5), ShowCreation(dice5_fr),
                    ShowCreation(box5))
        self.play(Write(twenty_multiple), Write(twenty))
        self.wait()

        self.play(ShowCreation(dice6), ShowCreation(dice6_fr),
                    ShowCreation(box6))
        self.play(Write(twelve_multiple), Write(twelve))
        self.wait(2)

        average_table_total = VGroup(twelve_multiple[1], five_multiple[1], twenty_multiple[1], eight1_multiple[1],
                                     eight_multiple[1], nine_multiple[1])
        total_freq_multiple = Text("62", font_size = 40).set_color("#3D7D72").next_to(border, DOWN).shift(RIGHT*2.2)
        self.play(TransformFromCopy(average_table_total,total_freq_multiple))

        result_numbers = VGroup( five, eight, nine, eight1, twenty, twelve)
        pluses = VGroup()

        for i in range(len(result_numbers) - 1):
            plus = Text("+", font_size=34).set_color("#454033")

            plus.move_to(
                (result_numbers[i].get_right() + result_numbers[i+1].get_left()) / 2
            )

            pluses.add(plus)
        
        self.play(LaggedStart(*[FadeIn(p) for p in pluses], lag_ratio=0.2))

        sum_expression = VGroup()

        for i in range(len(result_numbers)):
            sum_expression.add(result_numbers[i])
            if i < len(pluses):
                sum_expression.add(pluses[i])

        self.play(sum_expression.animate.arrange(RIGHT, buff=0.3).move_to(2*UP).shift(3*LEFT))

        equals = Text("=", font_size=36).set_color("#454033")
        equals.next_to(sum_expression, RIGHT, buff=0.3)
        total = Text("62", font_size=36).set_color("#3D7D72")
        total.next_to(equals, RIGHT, buff=0.3)

        self.play(Write(equals))
        self.play(TransformFromCopy(sum_expression, total))
        self.wait()

        numerator1 = Text("62", font_size = 36).set_color("#454033").shift(1.5*DOWN+LEFT*3.5)
        frac = Line(numerator1.get_left(), numerator1.get_right()).set_color(BLACK)
        frac.next_to(numerator1, DOWN, buff = 0.2)
        denominator1 = Text("20", font_size = 36).set_color("#454033").next_to(frac,DOWN, buff = 0.2)
        mean_text = Text("Mean =", font_size = 36).set_color("#454033").next_to(frac,LEFT, buff = 0.2)
        mean_value = VGroup(Text(" =", font_size = 36), Text("3.1", font_size = 36)).arrange(RIGHT).set_color("#454033").next_to(frac, RIGHT, buff = 0.2)
        mean_border = SurroundingRectangle(mean_value[1]).set_color("#BF7524")
        self.play(Write(numerator1), Write(frac), Write(denominator1), Write(mean_text))
        self.play(Write(mean_value), ShowCreation(mean_border))

        self.wait()
        self.play(FadeOut(table), FadeOut(mean_border), FadeOut(mean_value), FadeOut(mean_text), FadeOut(numerator1),
                  FadeOut(frac), FadeOut(denominator1), FadeOut(equals), FadeOut(result_numbers), FadeOut(pluses),
                  FadeOut(dice1), FadeOut(dice2), FadeOut(dice3), FadeOut(dice4), FadeOut(dice5), FadeOut(dice6),
                    FadeOut(dice6_fr), FadeOut(dice5_fr), FadeOut(dice4_fr),FadeOut(dice3_fr),FadeOut(dice2_fr),FadeOut(dice2_fr),
                    FadeOut(dice1_fr), FadeOut(denominator), FadeOut(total), FadeOut(total_freq_multiple), FadeOut(eight1_multiple),
                    FadeOut(eight_multiple), FadeOut(nine_multiple), FadeOut(twelve_multiple), FadeOut(twenty_multiple), 
                    FadeOut(five_multiple), FadeOut(rows0), FadeOut(box), FadeOut(box1), FadeOut(box3), FadeOut(box4), 
                    FadeOut(box5), FadeOut(frac_line), FadeOut(box6), FadeOut(plus_rows))

class Example1(Scene):
    def construct(self):

        grid = NumberPlane(
            axis_config = {"stroke_color" : GREY, "stroke_opacity":0.3},
            background_line_style={"stroke_color": GREY, "stroke_width":2, "stroke_opacity":0.3})
        
        self.add(grid)

        image_path = Path(self.file_writer.output_directory, "D:\manim-master\Media\seacher5.png").resolve()
        image = TexturedSurface(Square3D(resolution=(101, 101)), image_path)
        image.set_shape(FRAME_WIDTH*0.46*0.75, FRAME_HEIGHT*1.1*0.75)
        image.set_shading(0.1, 0.1, 0.1)
        image.move_to(ORIGIN).shift(LEFT*4.8+UP*0.26)
        self.play(FadeIn(image))
        self.wait()
        #self.add(SurroundingRectangle(image, buff=0).set_color(BLACK))

        # Data
        books = [1, 2, 3, 4, 5]
        freq = [4, 6, 7, 5, 3]
        product = [b * f for b, f in zip(books, freq)]

        rows = 6   # 1 header + 5 data rows
        cols = 3

        cell_width = 2.5
        cell_height = 0.8

        # Create grid
        grid = VGroup()
        cells = {}

        for i in range(rows):
            for j in range(cols):
                rect = Rectangle(
                    width=cell_width,
                    height=cell_height
                )
                rect.move_to(
                    RIGHT * j * cell_width +
                    DOWN * i * cell_height
                )
                grid.add(rect)
                cells[(i, j)] = rect

        grid.set_color(BLACK)
        grid.move_to(ORIGIN).shift(RIGHT*2.2)

        # Show grid
        self.play(FadeIn(grid))

        # --------- FUNCTION TO ADD TEXT ---------
        entries = {}

        def add_text(i, j, content):
            text = Tex(str(content)).scale(0.7).set_color(BLACK)
            text.move_to(cells[(i, j)].get_center())
            entries[(i, j)] = text
            return text

        # --------- HEADERS ---------
        headers = ["Books", "Frequency", "Product"]

        header_texts = VGroup(*[
            add_text(0, j, headers[j]) for j in range(cols)
        ])

        self.play(Write(header_texts))
        self.wait()

        # --------- FILL FIRST TWO COLUMNS ---------
        data_texts = VGroup()

        for i in range(5):
            row = i + 1
            data_texts.add(add_text(row, 0, books[i]).set_color("#2E7670"))       #8D452B
            data_texts.add(add_text(row, 1, freq[i]).set_color("#C77203"))            #195557

        for i, j in zip([0,2,4,6,8], [1,3,5,7,9]):
            self.play(Write(data_texts[i]), Write(data_texts[j]))
            self.wait()
        self.wait()

        mean = Text("Mean", font_size = 44).set_color(BLACK).next_to(grid, UP*1.5)
        self.play(Write(mean))
        self.wait(2)

        # --------- STEP-BY-STEP PRODUCT COLUMN ---------

        products = VGroup()
        for i in range(5):
            row = i + 1

            # Highlight current row
            highlight = VGroup(
                cells[(row, 0)],
                cells[(row, 1)]
            ).copy().set_fill(YELLOW, opacity=0.3)

            self.play(FadeIn(highlight))

            # Optional: show multiplication
            calc = Tex(f"{books[i]} \\times {freq[i]} = {product[i]}").set_color("#4D5A1B")
            calc.next_to(grid, DOWN)

            self.play(Write(calc))
            # Add product to table
            prod_text = add_text(row, 2, product[i]).set_color("#D21F2B")    #540502
            products.add(prod_text)
            if i == 0:
                self.play(Transform(calc[4].copy(), prod_text))
            else:
                self.play(Transform(calc[4:6].copy(), prod_text))

            self.play(FadeOut(calc), FadeOut(highlight))

        self.wait()

        # --------- TOTAL ---------
        total = sum(product)

        total_text = Tex(f"Total = {total}").set_color(BLACK)
        total_text.next_to(grid, DOWN)

        self.play(TransformFromCopy(products, total_text[6:8]), FadeIn(total_text[0:6]))
        self.wait(2)

        # --------- MEAN ---------
        meann = total / 25
        mean_text = Tex(f"\\frac{{{total}}}{{25}} = {meann}").set_color(BLACK)
        mean_text.next_to(grid, DOWN).shift(RIGHT*0.5)
        eq = Text("=", font_size = 45).next_to(mean_text[0], 0.8*LEFT).shift(DOWN*0.36)
        eq.set_color(BLACK)
        border = SurroundingRectangle(mean_text[6:10]).set_color("#852007")

        self.play(TransformFromCopy(total_text[6:8], mean_text[0:2]), FadeOut(total_text), Write(mean_text[2:5]))
        self.wait(2)
        self.play(Write(mean_text[5:10]), mean.animate.next_to(mean_text[0], 2.3*LEFT).shift(DOWN*0.28), FadeIn(eq),
                  ShowCreation(border))



def dice_question_logo(scene):

    # Dice body
    dice = Square(side_length=1.5, color=BLACK, stroke_width=0)
    dice.set_fill("#2B0101", opacity=1)

    dots = VGroup(
        Dot([-0.35,0.35,0], radius=0.08).set_color(WHITE),
        Dot([0.35,0.35,0], radius=0.08).set_color(WHITE),
        Dot([0,0,0], radius=0.08).set_color(WHITE),
        Dot([-0.35,-0.35,0], radius=0.08).set_color(WHITE),
        Dot([0.35,-0.35,0], radius=0.08).set_color(WHITE),
    )

    dice_group = VGroup(dice, dots)

    # Eyes
    eye_left = Circle(radius=0.22, fill_color=WHITE, fill_opacity=1, stroke_width=0)
    eye_right = Circle(radius=0.22, fill_color=WHITE, fill_opacity=1, stroke_width=0)

    eyes = VGroup(eye_left, eye_right)
    eyes.arrange(RIGHT, buff=0.35)
    eyes.move_to(dice.get_top() + UP*0.1)

    # Pupils
    pupil_left = Dot(radius=0.1).set_color(BLACK)
    pupil_right = Dot(radius=0.1).set_color(BLACK)

    pupil_left.move_to(eye_left.get_center())
    pupil_right.move_to(eye_right.get_center())

    pupils = VGroup(pupil_left, pupil_right)

    # Pupil highlight
    pup3d_left = Dot(radius=0.04).set_color(WHITE)
    pup3d_right = Dot(radius=0.04).set_color(WHITE)

    pup3d_left.move_to(pupil_left.get_corner(UL) + UL*-0.05)
    pup3d_right.move_to(pupil_right.get_corner(UL) + UL*-0.05)

    pup3d = VGroup(pup3d_left, pup3d_right)

    # Eyebrows
    brow_left = Arc(radius=0.35, start_angle=PI, angle=PI/2.5, color=BLACK)\
        .set_stroke(width=4).rotate(-120*DEG)

    brow_right = Arc(radius=0.35, start_angle=PI, angle=PI/2.5, color=BLACK)\
        .set_stroke(width=4).rotate(-120*DEG)

    brows = VGroup(brow_left, brow_right)
    brows.arrange(RIGHT, buff=0.35)
    brows.next_to(eyes, UP, buff=0.05)
    Full_body = VGroup(dice_group, eyes, pupils, pup3d, brows)
    Full_body.shift(LEFT)

    #Question Mark
    question_mark = Text("?", font_size=55).set_color(BLACK)
    question_mark.next_to(eyes, 1.3*RIGHT, buff=0.2)
    # Animation

    scene.play(
        FadeIn(Full_body)
    )

    scene.wait(0.4)

    scene.play(
        pupil_left.animate.shift(UP*0.07 + RIGHT*0.07),
        pupil_right.animate.shift(UP*0.07 + RIGHT*0.07),
        pup3d_left.animate.shift(UP*0.07 + RIGHT*0.07),
        pup3d_right.animate.shift(UP*0.07 + RIGHT*0.07),
        brows.animate.shift(UP*0.15),
        FadeIn(question_mark),
        run_time=0.6
    )
    #scene.play(ApplyMethod(question_mark.shift, UP*0.1))
    scene.play(question_mark.animate.shift(UP*0.2), rate_func=there_and_back, run_time =1.5)

    scene.wait(2)

    scene.play(FadeOut(Full_body), FadeOut(question_mark))

def create_dice(number, size=1.5):

    # Base square
    dice = Square(side_length=size, stroke_width=0)
    dice.set_fill("#2B0101", opacity=1)

    # Standard dot positions (relative layout)
    pos = {
        "tl": [-0.35, 0.35, 0],
        "tr": [0.35, 0.35, 0],
        "ml": [-0.35, 0, 0],
        "mr": [0.35, 0, 0],
        "bl": [-0.35, -0.35, 0],
        "br": [0.35, -0.35, 0],
        "c":  [0, 0, 0],
    }

    # Mapping number → dot positions
    dot_map = {
        1: ["c"],
        2: ["tl", "br"],
        3: ["tl", "c", "br"],
        4: ["tl", "tr", "bl", "br"],
        5: ["tl", "tr", "c", "bl", "br"],
        6: ["tl", "tr", "ml", "mr", "bl", "br"],
    }

    # Create dots
    dots = VGroup(*[
        Dot(pos[p], radius=0.08).set_color(WHITE)
        for p in dot_map[number]
    ])

    # Scale dots relative to dice size
    dots.scale(size / 1.5)

    return VGroup(dice, dots)


class FrequencyAverage(InteractiveScene):
    def construct(self):
        grid = NumberPlane(
            axis_config = {"stroke_color" : GREY, "stroke_opacity":0.3},
            background_line_style={"stroke_color": GREY, "stroke_width":2, "stroke_opacity":0.3})
        
        self.add(grid)

        numbers = ["10 - 15", "15 - 20", "20 - 25", "25 - 30"] 
        freqs = [4,7,6,3]
        h1 = Text("Height", font_size=36).set_color(BLACK)
        unit = Text("(cm)", font_size = 36).set_color(BLACK)
        table_dict = create_frequency_table(numbers, freqs, h1, unit)

        table = table_dict["table"]
        header = table_dict["header"]
        rows = table_dict["rows"]
        numbers_col = table_dict["numbers_col"]
        freqs_col = table_dict["freqs_col"]

        self.play(ShowCreation(header), FadeIn(rows),
            FadeIn(table_dict["border"]),
            FadeIn(table_dict["v_line"]),
            FadeIn(table_dict["h_lines"]),
        )

        mean = VGroup(Text("Mean", font_size = 46), Text("?", font_size = 50)).set_color(BLACK).arrange(RIGHT)
        mean.next_to(table, 2*RIGHT)

        self.play(Write(mean))
        self.play(mean[1].animate.shift(UP*0.2), rate_func=there_and_back, run_time =1.5)

        self.play(FadeOut(table_dict["border"]), FadeOut(table_dict["v_line"]), FadeOut(table_dict["h_lines"]),
                  FadeOut(mean), FadeOut(header), FadeOut(rows))
        
        dice_list = [create_dice(i, size= 0.5) for i in range(1, 7)]
        dice_group = VGroup(*dice_list)
        dice_group.arrange(RIGHT, buff=0.4)
        dice_group.move_to(3.8*LEFT + 2.3*UP)
        self.play(LaggedStart(*[FadeIn(d) for d in dice_group],lag_ratio=0.7), run_time = 5)

        heights = [12.3, 12.8, 13.1, 14.6]
        base_height = 12.3

        stems = []
        leaves_list = []
        scale_f = []

        for h in heights:
            stem, leaves = create_plant()
            scale_factor = h / base_height
            stem.scale(scale_factor*1.1)
            leaves.scale(scale_factor)
            stems.append(stem)
            leaves_list.append(leaves)
            scale_f.append(scale_factor)

        # Position first plant under dice 1
        stems[0].next_to(dice_group[0], DOWN, buff=0.8)
        leaves_list[0].move_to(stems[0]).shift(UP*0.2)

        #Position remaining plants relative to previous
        for i in range(1, 4):
            stems[i].next_to(stems[i-1], RIGHT, buff=0.4)
            leaves_list[i].move_to(stems[i]).shift(UP*0.2)

        for i in range(0,4):
            self.play(FadeIn(stems[i]), FadeIn(leaves_list[i]), run_time = 0.54)
        self.wait()

        plant_heights= VGroup()
        for h, i, s in zip(["12.3cm", "12.8cm", "13.1cm", "14.6cm"], [0,1,2,3], scale_f):
            height = Text(h, font_size = 28).set_color(BLACK).next_to(stems[i], DOWN, buff = (1.5 - 0.8*s))
            plant_heights.add(height)
        plant_heights[3].shift(0.1*LEFT)

        for i in range(0,4):
            self.play(FadeIn(plant_heights[i]), run_time = 2.3)
        self.wait()

        height_list = [15.6, 16.5, 17.4, 17.8, 18.2, 18.7, 19.4, 20.3, 21.1, 21.9, 22.4, 23.1, 24.3, 25.6, 26.1, 27.3]

        # Create more list numbers
        heights_list = VGroup(*[Text(str(n) + "cm", font_size=28).set_color(BLACK) for n in height_list])

        heights_list.arrange_in_grid(n_rows=4, n_cols=4, h_buff=0.62, v_buff= 0.3)
        heights_list.align_to(plant_heights[0], LEFT).shift(DOWN*2.3 + LEFT*0.015)

        self.play(LaggedStart(*[FadeIn(p) for p in heights_list], lag_ratio= 0.1))
        self.wait(2)

        #Adding Frequnecy table again
        table.shift(RIGHT*3.7)
        self.play(ShowCreation(header), 
            FadeIn(table_dict["border"]),
            FadeIn(table_dict["v_line"]),
            FadeIn(table_dict["h_lines"]),
        )
        self.wait()

        #Blurring the plant heights
        first_interval_blur = blur(plant_heights)
        interval_blurs = blur(heights_list)
        self.play(TransformFromCopy(plant_heights[0:3], rows[0]), FadeOut(plant_heights), FadeIn(first_interval_blur))
        self.wait()
        self.play(TransformFromCopy(heights_list[0:7], rows[1]), FadeOut(heights_list[0:7]), FadeIn(interval_blurs[0:7]))
        self.wait()
        self.play(TransformFromCopy(heights_list[7:13], rows[2]), FadeOut(heights_list[7:13]), FadeIn(interval_blurs[7:13]))
        self.wait()
        self.play(TransformFromCopy(heights_list[13:16], rows[3]), FadeOut(heights_list[13:16]), FadeIn(interval_blurs[13:16]))
        self.wait(2)

        #Highlighting first interval
        highlight_f_interval = SurroundingRectangle(rows[0][0]).set_color("#18786C")
        highlight_f_frequency = SurroundingRectangle(rows[0][1]).set_color("#BF7524")
        self.play(DrawBorderThenFill(highlight_f_interval))
        self.wait()
        self.play(DrawBorderThenFill(highlight_f_frequency))
        self.wait(2)
        mean.next_to(table, UP, buff=0.5)
        self.play(ShowCreation(mean))
        self.play(mean[1].animate.shift(UP*0.2), rate_func=there_and_back, run_time =1.5)
        self.play(FadeOut(dice_group))
        self.wait(2)
        #Again showing first four plant heights
        self.play(FadeOut(first_interval_blur), FadeIn(plant_heights))

        #Adding the first four heights
        pluses = VGroup()
        for i in range(len(plant_heights)-1):
            plus = Text("+", font_size=36).set_color(BLACK)
            plus.move_to((plant_heights[i].get_right() + plant_heights[i+1].get_left())/2)
            pluses.add(plus)

        self.play(LaggedStart(*[FadeIn(p) for p in pluses], lag_ratio= 0.05))

        sum_f_interval = VGroup(Text("=", font_size = 28).set_color(BLACK), 
                                Text("52.8cm", font_size = 28).set_color("#6B060E")).arrange(RIGHT)
        sum_f_interval.next_to(plant_heights[3], RIGHT, buff = 0.1)
        self.play(Write(sum_f_interval))
        self.wait(2)

        mid_point = VGroup(Text("Midpoint", font_size = 32), Text("=", font_size = 30)
                           ).set_color(BLACK).arrange(RIGHT).next_to(stems[0], UP*2.6).shift(RIGHT*0.6)
        numerator = Text("Lower Boundary + Upper Boundary", font_size = 25).set_color("#454033")
        frac = Line(numerator.get_left(), numerator.get_right()).set_color(BLACK)
        frac.next_to(mid_point[1], RIGHT, buff = 0.2)
        numerator.next_to(frac, UP, buff = 0.05)
        denominator = Text("2", font_size = 25).set_color("#454033").next_to(frac, DOWN, buff = 0.2)

        self.play(FadeIn(mid_point[0]))
        self.wait(2)
        self.play(FadeIn(mid_point[1]),FadeIn(numerator), FadeIn(frac), FadeIn(denominator))

        self.wait(2)
        mid_f_interval = mid_p("10 + 15")
        mid_f_interval.next_to(rows[0][0], RIGHT*1.4).shift(0.08*DOWN)
        mid_f_interval1 = Text("12.5", font_size = 30).set_color("#993131").next_to(rows[0][0], RIGHT*2.0)
        self.play(ShowCreation(mid_f_interval))
        self.wait()
        self.play(Transform(mid_f_interval, mid_f_interval1))
        self.wait(3)

        f_row_mid_x_freq = VGroup(Text("12.5 × 4 =", font_size = 25).set_color("#37454F"), Text("50", font_size = 27).set_color("#993131"))
        f_row_mid_x_freq.arrange(RIGHT, buff = 0.2).next_to(rows[0][1], RIGHT*1.1)

        self.play(Write(f_row_mid_x_freq[0]))
        self.wait()
        self.play(Write(f_row_mid_x_freq[1]))
        self.wait()

        highlight_f_freq_multiple = SurroundingRectangle(f_row_mid_x_freq[1]).set_color("#4D5A1B")
        highlight_f_interval_sum = SurroundingRectangle(sum_f_interval[1]).set_color("#4D5A1B")
        self.play(DrawBorderThenFill(highlight_f_freq_multiple))
        self.wait()
        self.play(DrawBorderThenFill(highlight_f_interval_sum))
        self.wait(2)

        mid_s_interval = mid_p("15 + 20")
        mid_s_interval.next_to(rows[1][0], RIGHT*1.4).shift(0.08*DOWN)
        mid_s_interval1 = Text("17.5", font_size = 30).set_color("#993131").next_to(rows[1][0], RIGHT*2.0)
        self.play(ShowCreation(mid_s_interval))
        self.play(Transform(mid_s_interval, mid_s_interval1))
        self.wait()

        mid_t_interval = Text("22.5", font_size = 30).set_color("#993131").next_to(rows[2][0], RIGHT*2.0)
        mid_fo_interval = Text("27.5", font_size = 30).set_color("#993131").next_to(rows[3][0], RIGHT*2.0)
        self.play(ShowCreation(mid_t_interval))
        self.wait()
        self.play(ShowCreation(mid_fo_interval))
        self.play(FadeOut(mid_point), FadeOut(numerator), FadeOut(denominator), FadeOut(frac),
                  FadeOut(plant_heights), FadeOut(pluses), FadeOut(sum_f_interval), FadeOut(interval_blurs),
                  FadeOut(highlight_f_freq_multiple), FadeOut(highlight_f_interval_sum))

        s_row_mid_x_freq = VGroup(Text("17.5 × 7 =", font_size = 25).set_color("#37454F"), Text("122.5", font_size = 27).set_color("#993131"))
        s_row_mid_x_freq.arrange(RIGHT, buff = 0.1).next_to(rows[1][1], RIGHT*0.99)

        t_row_mid_x_freq = VGroup(Text("22.5 × 6 =", font_size = 25).set_color("#37454F"), Text("135", font_size = 27).set_color("#993131"))
        t_row_mid_x_freq.arrange(RIGHT, buff = 0.1).next_to(rows[2][1], RIGHT*0.99)

        fo_row_mid_x_freq = VGroup(Text("27.5 × 3 =", font_size = 25).set_color("#37454F"), Text("82.5", font_size = 27).set_color("#993131"))
        fo_row_mid_x_freq.arrange(RIGHT, buff = 0.1).next_to(rows[3][1], RIGHT*0.99)

        self.play(Write(s_row_mid_x_freq[0]))
        self.play(Write(s_row_mid_x_freq[1]))
        self.wait()
        self.play(Write(t_row_mid_x_freq[0]))
        self.play(Write(t_row_mid_x_freq[1]))
        self.wait()
        self.play(Write(fo_row_mid_x_freq[0]))
        self.play(Write(fo_row_mid_x_freq[1]))
        self.wait()

        copy1 = f_row_mid_x_freq[1].copy().scale(1.2)
        copy2 = s_row_mid_x_freq[1].copy().scale(1.2)
        copy3 = t_row_mid_x_freq[1].copy().scale(1.2)
        copy4 = fo_row_mid_x_freq[1].copy().scale(1.2)
        copy1_pos = stems[1].get_bottom() + DOWN
        copy2_pos = copy1_pos + 1.2*RIGHT
        copy3_pos = copy2_pos + 1.2*RIGHT
        copy4_pos = copy3_pos + 1.2*RIGHT
        plus = Text("+", font_size = 28).set_color(BLACK).move_to((copy1_pos + 0.5*RIGHT))
        plus2 = plus.copy().move_to((copy2_pos + copy3_pos)/2 + 0.1*RIGHT)
        plus3 = plus.copy().move_to((copy3_pos + copy4_pos)/2)
        sum_of_all_heights = Text("390", font_size = 32).set_color("#2E7670").move_to(copy2_pos)


        self.play(copy1.animate.move_to(copy1_pos), copy2.animate.move_to(copy2_pos), copy3.animate.move_to(copy3_pos), 
                  copy4.animate.move_to(copy4_pos),  FadeIn(plus), FadeIn(plus2), FadeIn(plus3))
        self.wait()
        self.play(Transform(VGroup(copy1, copy2, copy3, copy4, plus, plus2, plus3), sum_of_all_heights))

        fra = Line(sum_of_all_heights.get_left(), sum_of_all_heights.get_right()).set_color(BLACK)
        fra.next_to(sum_of_all_heights, DOWN, buff = 0.05)
        total_freq = Text("20", font_size = 32).set_color("#2E7670").next_to(fra, DOWN, buff = 0.1)
        self.play(FadeIn(fra), FadeIn(total_freq))

        est_mean = VGroup(Text("=", font_size = 32).set_color(BLACK) , 
                          Text("19.5", font_size = 32).set_color("#2E7670")).arrange(RIGHT).next_to(fra)
        estim_mean = VGroup(Text("Estimated \n   Mean", font_size = 32).set_color(BLACK) , 
                          Text("=", font_size = 32).set_color(BLACK)).arrange(RIGHT).next_to(fra, LEFT)
        highlight_est_mean = SurroundingRectangle(est_mean[1]).set_color("#FF9001")
        self.play(Write(est_mean), Write(estim_mean), ShowCreation(highlight_est_mean))
        self.wait()



def mid_p(numer):
    numerator = Text(numer, font_size = 23).set_color("#454033")
    frac = Line(numerator.get_left(), numerator.get_right()).set_color(BLACK)
    numerator.next_to(frac, UP, buff = 0.05)
    denominator = Text("2", font_size = 23).set_color("#454033").next_to(frac, DOWN, buff = 0.1)
    full_frac = VGroup(numerator, frac, denominator)
    return full_frac

def blur(list):
    blurred_heights = VGroup()
    for h in list:
        layers = VGroup(*[h.copy().set_opacity(0.05/(i+1)).scale(1 + 0.3*i) for i in range(4)])
        blurred_heights.add(layers)
    return blurred_heights

def create_frequency_table(numbers, freqs, h1, unit):

    # Header
    h2 = Text("Frequency", font_size=36).set_color(BLACK)
    header = VGroup(h1, h2).arrange(RIGHT, buff=2.5)

    # Rows
    rows = VGroup()
    for n, f in zip(numbers, freqs):

        num = Text(n, font_size=36).set_color(BLACK)
        frq = Text(str(f), font_size=36).set_color(BLACK)

        row = VGroup(num, frq).arrange(RIGHT, buff=1.8)
        rows.add(row)

    rows.arrange(DOWN, buff=0.8)
    unit.next_to(header[0], RIGHT*0.6)
    header = VGroup(header, unit)

    # Table content
    table_content = VGroup(header, rows)
    table_content.arrange(DOWN, buff=0.6, aligned_edge=LEFT)

    table_color = "#462802"

    # Border
    border = SurroundingRectangle(table_content, buff=0.4).set_color(table_color)

    # Vertical line
    v_line = Line(
        border.get_top() + RIGHT*0.1,
        border.get_bottom() + RIGHT*0.1
    ).set_color(table_color)

    # Horizontal lines
    h_lines = VGroup()
    for row in rows:
        line = Line(
            border.get_left(),
            border.get_right()
        ).move_to(row.get_top() + UP*0.35 + RIGHT*1.03).set_color(table_color)
        h_lines.add(line)

    # Final table group
    table = VGroup(border, v_line, h_lines, table_content)

    # 👉 IMPORTANT: return all parts
    return {
        "table": table,
        "header": header,
        "rows": rows,
        "numbers_col": VGroup(*[row[0] for row in rows]),
        "freqs_col": VGroup(*[row[1] for row in rows]),
        "border": border,
        "v_line": v_line,
        "h_lines": h_lines,
    }

def create_plant():
    stem = SVGMobject("D:/manim-master/Media/stem.svg")
    leaves = SVGMobject("D:/manim-master/Media/leaves.svg")

    for s in stem:
        s.set_stroke(width=6)

    stem.scale(0.7).set_z_index(-1)
    leaves.scale(0.5).set_z_index(1)

    leaves.move_to(stem).shift(UP*0.2)

    return stem, leaves

class TomatoHeight(InteractiveScene):

    def construct(self):
            # Test
            image_path = Path(self.file_writer.output_directory, "D:\manim-master\Media\somato_measurement.png").resolve()
            image = TexturedSurface(Square3D(resolution=(101, 101)), image_path)
            image.set_shape(FRAME_WIDTH, FRAME_HEIGHT)
            image.set_shading(0.1, 0.1, 0.1)
            self.add(image)

            # Make waves
            frame = self.frame

            frame.reorient(0, 0, 0, (0, 0, 0.0), 4.39)
            self.play(
                frame.animate.to_default_state(),
                run_time=5,
            )