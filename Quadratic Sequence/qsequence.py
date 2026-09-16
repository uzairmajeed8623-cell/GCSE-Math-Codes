from manimlib import *

class QSequence(InteractiveScene):

    def construct(self):
        grid = NumberPlane(
            axis_config = {"stroke_color" : GREY, "stroke_opacity":0.3},
            background_line_style={"stroke_color": GREY, "stroke_width":2, "stroke_opacity":0.3})
        
        equation1 = Tex(R"2n^2 + 4n + 3").move_to(UP*3).set_color(BLACK)
        general_equation = Tex(R"an^2 + bn + c").move_to(UP*2).set_color(BLACK)

        cofficients_color = "#454033"
        cofficient_a_rect= SurroundingRectangle(general_equation[0]).set_stroke(color = cofficients_color)
        cofficient_b_rect= SurroundingRectangle(general_equation[4]).set_stroke(color = cofficients_color)
        cofficient_c_rect= SurroundingRectangle(general_equation[7]).set_stroke(color = cofficients_color)
        power_rect= SurroundingRectangle(general_equation[2]).set_stroke(color = "#726a55")
            
        self.add(grid)
        self.play(Write(equation1))
        self.wait(2)
        self.play(Write(general_equation))
        self.wait(2)
        self.play(ShowCreation(cofficient_a_rect), ShowCreation(cofficient_c_rect), ShowCreation(cofficient_b_rect))
        self.wait()
        self.play(ShowCreation(power_rect))
        self.wait()
        self.play(FadeOut(cofficient_a_rect), FadeOut(cofficient_b_rect), FadeOut(cofficient_c_rect),
                  FadeOut(power_rect))
        
        cofficient_values = Tex(R"a = 1,    b = 3,    c = 1").move_to(UP*1).set_color("#445544")
        new_expression = Tex(R"1n^2 + 3n + 1").set_color(BLACK)
        question_5_terms = Text("Work out the first 5 terms in the sequence", font_size = 35).set_color("#8B0303").move_to(LEFT*2.2+UP*2)


        self.play(Write(cofficient_values))
        self.wait()
        self.play(general_equation.animate.become(new_expression))
        self.wait()
        self.play(FadeOut(equation1), cofficient_values.animate.move_to(UP*3+RIGHT*5), general_equation.animate.move_to(UP*3+LEFT*5.2),
                  )
        self.play(Write(question_5_terms), FadeOut(general_equation[0]))

        # Create 4 lines, spaced 2 units apart
        v_lines = VGroup(*[Line(UP*1.5, DOWN*2).set_color(BLACK) for _ in range(4)]).arrange(buff=2.8).move_to(DOWN*0.5)
        n_values = VGroup(*[Tex(f"n = {i}").set_color(BLACK) for i in range(1,6)]).arrange(buff =1.7).move_to(LEFT*0.5 + UP)
        self.play(ShowCreation(v_lines), FadeIn(n_values))
        self.wait()
        terms_color = "#395B64"
        first_term = Tex(R"(1)^2 + 3(1) + 1", font_size= 40).set_color(terms_color).next_to(n_values[0], DOWN).shift([0.5,-0.2,0])
        first_term_soln = Tex(R"5", font_size= 45).set_color("#3674B5").next_to(first_term, DOWN).shift([-0.7, - 0.2,0 ])

        self.play(ShowCreation(first_term))
        self.wait()
        self.play(ShowCreation(first_term_soln))
        self.wait()
        
        sec_term = Tex(R"(2)^2 + 3(2) + 1", font_size= 40).set_color(terms_color).next_to(n_values[1], DOWN).shift([0.55,-0.2,0])
        sec_term_soln = Tex(R"11", font_size= 45).set_color("#3674B5").next_to(sec_term, DOWN).shift([-0.7, - 0.2,0 ])

        self.play(ShowCreation(sec_term))
        self.wait()
        self.play(ShowCreation(sec_term_soln))
        self.wait()

        third_term = Tex(R"(3)^2 + 3(3) + 1", font_size= 40).set_color(terms_color).next_to(n_values[2], DOWN).shift([0.56,-0.2,0])
        third_term_soln = Tex(R"19", font_size= 45).set_color("#3674B5").next_to(third_term, DOWN).shift([-0.7, - 0.2,0 ])

        fourth_term = Tex(R"(4)^2 + 3(4) + 1", font_size= 40).set_color(terms_color).next_to(n_values[3], DOWN).shift([0.52,-0.2,0])
        fourth_term_soln = Tex(R"29", font_size= 45).set_color("#3674B5").next_to(fourth_term, DOWN).shift([-0.7, - 0.2,0 ])

        fifth_term = Tex(R"(5)^2 + 3(5) + 1", font_size= 40).set_color(terms_color).next_to(n_values[4], DOWN).shift([0.53,-0.2,0])
        fifth_term_soln = Tex(R"41", font_size= 45).set_color("#3674B5").next_to(fifth_term, DOWN).shift([-0.7, - 0.2,0 ])

        self.play(FadeIn(third_term), FadeIn(third_term_soln), FadeIn(fourth_term), FadeIn(fourth_term_soln),
                  FadeIn(fifth_term), FadeIn(fifth_term_soln))
        self.wait()

        self.play(FadeOut(first_term), FadeOut(sec_term), FadeOut(third_term), FadeOut(fourth_term),
                  FadeOut(fifth_term), FadeOut(n_values), FadeOut(v_lines), FadeOut(general_equation),
                  FadeOut(question_5_terms))
        self.play(first_term_soln.animate.shift(UP*3))
        self.play(sec_term_soln.animate.next_to(first_term_soln, RIGHT*4), run_time = 0.4, rate_func = smooth)
        self.play(third_term_soln.animate.next_to(sec_term_soln, RIGHT*4), run_time = 0.4,rate_func = smooth)
        self.play(fourth_term_soln.animate.next_to(third_term_soln, RIGHT*4), run_time = 0.4, rate_func = smooth)
        self.play(fifth_term_soln.animate.next_to(fourth_term_soln, RIGHT*4), run_time = 0.4, rate_func = smooth)
        self.wait()

        nth_exp_question = Text("Find the expression for the nth term_", font_size = 38).set_color("#8B0303").next_to(fourth_term_soln.get_left(), UP, buff = 0.7)
        self.play(Write(nth_exp_question))
        self.wait()

        
        brace = Brace(Line(first_term_soln.get_left(), sec_term_soln.get_center()), DOWN, buff = 0.3).set_color("#E35336")
        braces = VGroup(brace)
        for _ in range(3):
            new_brace = brace.copy().next_to(braces[-1], RIGHT,buff = 0.05)
            braces.add(new_brace)

        first_differences = VGroup()
        for i, br in zip([6,8,10,12], braces):
            f_diff= Tex(f"{i}").set_color("#E35336").next_to(br, DOWN)
            first_differences.add(f_diff)

        self.play(FadeIn(first_differences[0]), FadeIn(braces[0]))
        self.wait() 
        self.play(FadeIn(first_differences[1]), FadeIn(braces[1]))
        self.wait()
        self.play(FadeIn(first_differences[2]), FadeIn(braces[2]))
        self.wait()
        self.play(FadeIn(first_differences[3]), FadeIn(braces[3]))
        self.wait()

        first_diff_text = Text("First Difference", font_size = 38).set_color("#E35336").next_to(first_differences[-1], RIGHT, buff = 1)
        self.play(FadeIn(first_diff_text))
        self.wait()

        sec_different_brace = Brace(Line(first_differences[0].get_center(), first_differences[1].get_center()), DOWN, buff = 0.3).set_color("#344F1F")
        constant_2nd_diff = Tex(R"2").set_color("#344F1F").next_to(sec_different_brace,DOWN)
        sec_diff_brace= VGroup(sec_different_brace, constant_2nd_diff)
        sec_braces = VGroup(sec_diff_brace)
        for _ in range(2):
            sec_new_brace = sec_diff_brace.copy().next_to(sec_braces[-1], RIGHT,buff = 0.05)
            sec_braces.add(sec_new_brace)

        second_diff_text = Text("Second Difference", font_size = 38).set_color("#344F1F").next_to(constant_2nd_diff, 4.62*RIGHT, buff = 1)

        self.play(FadeIn(sec_braces))
        self.wait()
        self.play(FadeIn(second_diff_text))
        self.wait(2)

        general_equation = Tex(R"an^2 + bn + c").set_color("#77224d").shift(DOWN)
        gen_eq_rect      = SurroundingRectangle(general_equation).set_stroke(color = "#7a3b5b")
        gen_eq_group = VGroup(general_equation, gen_eq_rect)

        self.play(FadeIn(gen_eq_group))
        self.wait()
        self.play(gen_eq_group.animate.move_to(UP*2.3+ RIGHT *5))

        vertical_lines = VGroup(*[Line(UP*1.5, DOWN*2).set_color(BLACK) for _ in range(2)]).arrange(buff=4.8).move_to(DOWN*2.0+LEFT*0.2)

        self.play(ShowCreation(vertical_lines))
        self.wait()

     #   first_eq = Text("2a = first term \n    of 2nd diff", font_size = 40).set_color("#116CD3").next_to(vertical_lines[0], 2*LEFT).shift(UP)
        first_eq = VGroup(Text("2a = ", font_size=42), Text("first term\nof 2nd diff", font_size=42)
                                ).arrange(RIGHT).set_color("#116CD3").next_to(vertical_lines[0], 2*LEFT).shift(UP)   
        sec_eq = VGroup(Text("3a + b =", font_size = 42), Text("first term\nof 1st diff", font_size = 40)
                                ).arrange(RIGHT).set_color("#750A0A").next_to(vertical_lines[1], 0.8*LEFT).shift(UP)
        third_eq = VGroup(Text("a + b + c =", font_size =42), Text("first \nterm of\nsequence", font_size = 40)
                          ).arrange(RIGHT).set_color("#D3117C").next_to(vertical_lines[1], 0.6*RIGHT).shift(1*UP)
        self.play(Write(first_eq))
        self.wait()
        self.play(Write(sec_eq))
        self.wait()
        self.play(Write(third_eq))
        self.wait()

        highight_2nd_diff = SurroundingRectangle(constant_2nd_diff).set_color(BLACK)
        replacement1 = constant_2nd_diff.copy()
        a_answer = Text("a = 1", font_size = 42).set_color("#116CD3").next_to(first_eq[0], DOWN*2).shift(RIGHT*0.35)

        self.play(ShowCreation(highight_2nd_diff))
        self.wait()
        self.play(replacement1.animate.move_to(first_eq[1].get_left()+[0.2,0,0]).set_color("#116CD3"), FadeOut(first_eq[1]),
                    run_time=1.5)
        self.wait()
        self.play(Write(a_answer))
        self.wait()

        highight_1st_diff = SurroundingRectangle(first_differences[0]).set_color(BLACK)
        replacement2 = first_differences[0].copy()
        sec_eq2 = VGroup(Text("3(1) + b = ", font_size = 42), Tex(R"6")).arrange(RIGHT).set_color("#750A0A").next_to(sec_eq[0], DOWN*2).shift(RIGHT*0.45)
        sec_eq3 = VGroup(Text("-3 + 3 + b = ", font_size = 42), Tex(R"-3 + 6")).arrange(RIGHT).set_color("#750A0A").next_to(sec_eq[0], DOWN*2).shift(RIGHT*1.2)
        sec_eq4 = VGroup(Text("b = ", font_size = 42), Tex(R"3")).arrange(RIGHT).set_color("#750A0A").next_to(sec_eq3[0], DOWN*2).shift(LEFT*0.7)

        self.play(ShowCreation(highight_1st_diff))
        self.wait()
        self.play(replacement2.animate.move_to(sec_eq[1].get_left()+[0.2,0,0]).set_color("#750A0A"), FadeOut(sec_eq[1]),
                    run_time=1.5)
        self.wait()
        self.play(Write(sec_eq2))
        self.wait()
        self.play(Transform(sec_eq2,sec_eq3))
        self.wait()
        self.play(Write(sec_eq4))
        self.wait()

        highight_1st_term = SurroundingRectangle(first_term_soln).set_color(BLACK)
        replacement3 = first_term_soln.copy()
        third_eq2 = VGroup(Text("1 + 3 + c = ", font_size = 42), Tex(R"5")).arrange(RIGHT).set_color("#D3117C").next_to(third_eq[0], DOWN*2).shift(RIGHT*0.23)
        third_eq3 = VGroup(Text("4 + c = ", font_size = 42), Tex(R"5")).arrange(RIGHT).set_color("#D3117C").next_to(third_eq[0], DOWN*2).shift(RIGHT*0.2)
        third_eq4 = VGroup(Text("-4 + 4 + c = ", font_size = 42), Tex(R"-4 + 5")).arrange(RIGHT).set_color("#D3117C").next_to(third_eq[0], DOWN*2).shift(RIGHT*0.85)
        third_eq5 = VGroup(Text("c = ", font_size = 42), Tex(R"1")).arrange(RIGHT).set_color("#D3117C").next_to(third_eq4[0], DOWN*2).shift(LEFT*0.7)


        self.play(ShowCreation(highight_1st_term))
        self.play(replacement3.animate.move_to(third_eq[1].get_left() + [0.2,0,0]).set_color("#D3117C"),
                  FadeOut(third_eq[1]), run_time = 1.5)
        self.wait()
        self.play(Write(third_eq2))
        self.wait()
        self.play(Transform(third_eq2, third_eq3))
        self.wait()
        self.play(Transform(third_eq2, third_eq4))
        self.wait()
        self.play(Write(third_eq5))
        self.wait()
        self.play(FadeOut(third_eq), FadeOut(third_eq2), FadeOut(sec_eq2), FadeOut(first_eq), 
                  FadeOut(sec_eq), FadeOut(third_eq), FadeOut(replacement1), FadeOut(replacement2),
                  FadeOut(replacement3), FadeOut(vertical_lines))
        self.wait()
        self.play(a_answer.animate.shift(UP+RIGHT))
        self.play(sec_eq4.animate.next_to(a_answer, RIGHT*2))
        self.play(third_eq5.animate.next_to(sec_eq4, RIGHT*2))
        self.wait()

        final_equation = Tex(R"1n^2 + 3n + 1").set_color(BLACK).next_to(sec_eq4, DOWN*2)
        final_eq_boundary = SurroundingRectangle(final_equation).set_color(BLACK)
        final_equation1 = Tex(R"n^2 + 3n + 1").set_color(BLACK).next_to(sec_eq4, DOWN*2)
        final_eq1_boundary = SurroundingRectangle(final_equation1).set_color(BLACK)
        f_eq_group = VGroup(final_equation, final_eq_boundary)

        self.play(Transform(gen_eq_group, f_eq_group))
        self.wait()
        self.play(Transform(gen_eq_group, VGroup(final_equation1, final_eq1_boundary)))
        self.wait()


class QSequence1(InteractiveScene):
    def construct(self):
        grid = NumberPlane(
            axis_config = {"stroke_color" : GREY, "stroke_opacity":0.3},
            background_line_style={"stroke_color": GREY, "stroke_width":2, "stroke_opacity":0.3})
        
        self.add(grid)

        sequence = VGroup(*[Tex(f"{i}").set_color(BLACK) for i in [19,15,9,1]]).arrange(buff = 2).shift(UP*2)
        first_diff_braces = VGroup(*[Brace(Line(sequence[i].get_center(), sequence[i+1].get_center()-[0.1,0,0]), DOWN, buff = 0.3
                                        ).set_color("#E35336") for i in range(3)])
        f_diff_f_term = Tex(r"15 - 19").set_color("#454033").next_to(first_diff_braces[0], DOWN)
        f_diff_f_term1 = Tex(r"-4").set_color("#4DA30C").next_to(f_diff_f_term, DOWN*1.5 +LEFT*-0)

        f_diff_s_term = Tex(r"9 - 15").set_color("#454033").next_to(first_diff_braces[1], DOWN)
        f_diff_s_term1 = Tex(r"-6").set_color("#4DA30C").next_to(f_diff_s_term, DOWN*1.5 +LEFT*-0)

        f_diff_t_term = Tex(r"1 - 9").set_color("#454033").next_to(first_diff_braces[2], DOWN)
        f_diff_t_term1 = Tex(r"-8").set_color("#4DA30C").next_to(f_diff_t_term, DOWN*1.5 +LEFT*-0)

        f_diff_text = Text("First Difference", font_size = 38).set_color("#4DA30C").next_to(f_diff_f_term, LEFT)


        self.play(Write(sequence))
        self.wait()
        self.play(FadeIn(first_diff_braces[0]), Write(f_diff_f_term))
        self.wait()
        self.play(Write(f_diff_f_term1))
        self.wait()
        self.play(FadeIn(first_diff_braces[1]), Write(f_diff_s_term))
        self.wait()
        self.play(Write(f_diff_s_term1))
        self.wait()
        self.play(FadeIn(first_diff_braces[2]), Write(f_diff_t_term))
        self.wait()
        self.play(Write(f_diff_t_term1))
        self.wait()
        self.play(FadeOut(f_diff_f_term), FadeOut(f_diff_s_term), FadeOut(f_diff_t_term))
        self.play(Write(f_diff_text), f_diff_f_term1.animate.shift(UP*0.7 + LEFT*0.2), f_diff_s_term1.animate.shift(UP*0.7+ LEFT*0.2), 
                  f_diff_t_term1.animate.shift(UP*0.7 + LEFT*0.2))
        self.wait()


        sec_diff_brace1 = Brace(Line(f_diff_f_term1.get_center(), f_diff_s_term1.get_center()), DOWN, buff = 0.3).set_color("#750A0A")
        sec_diff_brace2 = sec_diff_brace1.copy().next_to(sec_diff_brace1, RIGHT*0.8)
        sec_diff_f_term = Tex(r"-6 - (-4)").set_color("#116CD3").next_to(sec_diff_brace1, DOWN)
        sec_diff_f_term1 = Tex(r"-2").set_color("#116CD3").next_to(sec_diff_f_term, DOWN)
        sec_diff_s_term = Tex(r"-8 - (-6)").set_color("#116CD3").next_to(sec_diff_brace2, DOWN)
        sec_diff_s_term1 = Tex(r"-2").set_color("#116CD3").next_to(sec_diff_s_term, DOWN)
        sec_diff_text = Text("Second Difference", font_size = 38).set_color("#116CD3").next_to(sec_diff_f_term, 2.8*LEFT)


        self.play(FadeIn(sec_diff_brace1), Write(sec_diff_f_term))
        self.wait()
        self.play(Write(sec_diff_f_term1))
        self.wait()
        self.play(FadeIn(sec_diff_brace2), Write(sec_diff_s_term))
        self.wait()
        self.play(Write(sec_diff_s_term1))
        self.wait()
        self.play(FadeOut(sec_diff_f_term), FadeOut(sec_diff_s_term))
        self.play(Write(sec_diff_text), sec_diff_f_term1.animate.shift(UP*0.7 + LEFT*0.2), sec_diff_s_term1.animate.shift(UP*0.7 + LEFT*0.2))
        self.wait()

        vertical_lines = VGroup(*[Line(UP*1.1, DOWN*2).set_color(BLACK) for _ in range(2)]).arrange(buff=4.8).move_to(DOWN*2.2+LEFT*0.2)
        first_eq = Text("2a = -2", font_size=42).set_color("#116CD3").next_to(vertical_lines[0], 6*LEFT).shift(UP)   
        sec_eq = Text("3a + b = -4", font_size = 42).set_color("#750A0A").next_to(vertical_lines[1], 4.8*LEFT).shift(UP)
        third_eq = Text("a + b + c = 19", font_size =42).set_color("#D3117C").next_to(vertical_lines[1], 3.5*RIGHT).shift(1*UP)
        highlight_sec_diff = SurroundingRectangle(sec_diff_f_term1).set_color(BLACK)
        highlight_first_diff = SurroundingRectangle(f_diff_f_term1).set_color(BLACK)
        highlight_sequence = SurroundingRectangle(sequence[0]).set_color(BLACK)
        firs_eq_soln = Text("a = -1", font_size=42).set_color("#116CD3").next_to(first_eq, 2*DOWN)
        first_eq_soln = VGroup(SurroundingRectangle(firs_eq_soln).set_color("#454033"), firs_eq_soln) 
        sec_eq_soln = Text("3(-1) + b = -4", font_size= 42).set_color("#750A0A").move_to(sec_eq)
        sec_eq_soln1 = Text("-3 + b = -4", font_size= 42).set_color("#750A0A").move_to(sec_eq)
        sec_eq_sol2 = Text("b = -1", font_size=42).set_color("#750A0A").next_to(sec_eq, 2*DOWN) 
        sec_eq_soln2 = VGroup(SurroundingRectangle(sec_eq_sol2).set_color("#454033"), sec_eq_sol2)

        self.play(ShowCreation(vertical_lines))
        self.play(Write(first_eq))
        self.play(ShowCreation(highlight_sec_diff))
        self.wait()
        self.play(Write(sec_eq))
        self.play(ShowCreation(highlight_first_diff))
        self.wait()
        self.play(Write(third_eq))
        self.play(ShowCreation(highlight_sequence))
        self.wait()

        divide_by_2 = VGroup(*[Tex(r"\divisionsymbol 2").set_color(BLACK) for _ in range(2)]).arrange(buff = 2).next_to(vertical_lines[0], 2*LEFT).next_to(first_eq, DOWN)
        self.play(ShowCreation(divide_by_2))
        self.wait()
        self.play(FadeOut(divide_by_2), Write(first_eq_soln))
        self.wait()
        self.play(Transform(sec_eq, sec_eq_soln))
        self.wait(2)
        self.play(Transform(sec_eq, sec_eq_soln1))
        self.wait()
        add_3 = VGroup(*[Tex(r"+3").set_color(BLACK) for _ in range(2)]).arrange(buff = 2).next_to(vertical_lines[1], 2*LEFT).next_to(sec_eq, DOWN)

        self.play(ShowCreation(add_3))
        self.wait()
        self.play(FadeOut(add_3), Write(sec_eq_soln2))
        self.wait()

        a_value = firs_eq_soln[-2:].copy()
        b_value = sec_eq_sol2[-2:].copy()
        third_eq_soln = Text("-2", font_size= 42).set_color("#D3117C").move_to(third_eq[2])
        self.play(a_value.animate.move_to(third_eq[0]).set_color("#D3117C"), FadeOut(third_eq[0]))
        self.play(b_value.animate.move_to(third_eq[2]).set_color("#D3117C"), FadeOut(third_eq[2]))
        self.wait()
        self.play(Transform(VGroup(a_value, b_value,third_eq[1]), third_eq_soln))
        self.wait()

        add_2 = VGroup(*[Tex(r"+2").set_color(BLACK) for _ in range(2)]).arrange(buff = 1.5).next_to(vertical_lines[1], 6*RIGHT).shift(0.3*UP)
        third_eq_sol2 = Text("c = 21", font_size=42).set_color("#D3117C").next_to(third_eq, 2*DOWN)
        third_eq_soln2= VGroup(SurroundingRectangle(third_eq_sol2).set_color("#454033"), third_eq_sol2)
        general_equation = Tex(R"an^2 + bn + c", font_size= 60).move_to(UP*0.5).set_color("#335063")
        general_equation1 = Tex(R"-1n^2 - 1n + 21", font_size= 60).move_to(UP*0.5).set_color("#335063")
        general_equation2 = Tex(R"-n^2 - n + 21", font_size= 60).move_to(UP*0.5).set_color("#335063")
        
        self.play(ShowCreation(add_2))
        self.wait(2)
        self.play(FadeOut(add_2), Write(third_eq_soln2))
        self.wait()
        self.play(FadeOut(vertical_lines), FadeOut(a_value), FadeOut(b_value), FadeOut(third_eq), FadeOut(first_eq),
                  FadeOut(sec_eq), FadeOut(first_diff_braces), FadeOut(sec_diff_brace1), FadeOut(sec_diff_brace2),
                  FadeOut(f_diff_f_term1), FadeOut(f_diff_s_term1), FadeOut(f_diff_t_term1), FadeOut(f_diff_text),
                  FadeOut(sec_diff_f_term1), FadeOut(sec_diff_s_term1), FadeOut(sec_diff_text), 
                  FadeOut(highlight_first_diff), FadeOut(highlight_sec_diff), FadeOut(highlight_sequence),
                  first_eq_soln.animate.shift(UP*3))
        self.play(sec_eq_soln2.animate.next_to(firs_eq_soln, DOWN))
        self.play(third_eq_soln2.animate.next_to(sec_eq_soln2, DOWN),Write(general_equation))
        self.wait()
        self.play(Transform(general_equation, general_equation1))
        self.wait()
        self.play(Transform(general_equation, general_equation2), ShowCreation(SurroundingRectangle(general_equation2).set_color(BLACK)))
        self.wait()


class QSequence2(InteractiveScene):

    def construct(self):
        grid = NumberPlane(
            axis_config = {"stroke_color" : GREY, "stroke_opacity":0.3},
            background_line_style={"stroke_color": GREY, "stroke_width":2, "stroke_opacity":0.3})
        
        self.add(grid)

        general_eq = Tex(r"an^2 + bn + c", font_size = 55).set_color("#454033").shift(UP*2.5)
        general_eq_boundary = SurroundingRectangle(general_eq).set_color(BLACK)
        n_values = VGroup(*[Tex(f"n = {i}").set_color(BLACK) for i in [1,2,3]]).arrange(buff = 3.3).next_to(general_eq, 2*DOWN)
        terms = VGroup(*[Tex(f"a({i})^2 + b({i}) + c").set_color("#750A0A").next_to(n_values[i-1], DOWN*2) for i in [1,2,3]])
        f_term = Tex(r"a + b + c").set_color("#344F1F").next_to(terms[0], DOWN*2)
        s_term = Tex(r"4a + 2b + c").set_color("#344F1F").next_to(terms[1], DOWN*2)
        t_term = Tex(r"9a + 3b + c").set_color("#344F1F").next_to(terms[2], DOWN*2)

        self.play(Write(general_eq), ShowCreation(general_eq_boundary))
        self.wait()
        self.play(Write(n_values[0]))
        self.play(Write(terms[0]))
        self.wait()
        self.play(Write(f_term))
        self.wait()
        self.play(Write(n_values[1]))
        self.play(Write(terms[1]))
        self.wait()
        self.play(Write(s_term))
        self.wait()
        self.play(Write(n_values[2]))
        self.play(Write(terms[2]))
        self.wait()
        self.play(Write(t_term))
        self.wait()
        self.play(FadeOut(terms), FadeOut(n_values))

        general_sequence = VGroup(f_term, s_term, t_term)
        self.play(general_sequence.animate.arrange(buff=1.0).move_to(UP*1.3))

        s_f = 0.1   #shift factor
        Braces1 = Brace(Line(general_sequence[0].get_left()+ [s_f,0,0], general_sequence[1].get_center()), DOWN, buff = 0.3).set_color(BLACK).shift(s_f*LEFT)
        Braces2 = Brace(Line(general_sequence[1].get_center(), general_sequence[2].get_right()- [s_f,0,0]), DOWN, buff = 0.3).set_color(BLACK).shift(s_f*RIGHT)
        Braces = VGroup(Braces1, Braces2)
        
        d_f = 1.5    #DOwn factor
        f_diff_f_term0 = Tex(r"4a + 2b + c - (a + b + c)").set_color("#116CD3").next_to(Braces[0], d_f*DOWN)
        f_diff_f_term1 = Tex(r"4a + 2b + c - a - b - c").set_color("#116CD3").next_to(Braces[0], d_f*DOWN)
        f_diff_f_term2 = Tex(r"4a - a + 2b - b + c - c").set_color("#116CD3").next_to(Braces[0], d_f*DOWN)
        f_diff_f_term3 = Tex(r"3a + b").set_color("#116CD3").next_to(Braces[0], d_f*DOWN)
        f_diff_text = Text("First \nDifference", font_size = 35).set_color("#335063").next_to(f_diff_f_term0, 0.8*LEFT)

        f_diff_s_term0 = Tex(r"9a + 3b + c - (4a + 2b + c)").set_color("#116CD3").next_to(Braces[1], d_f*DOWN)
        f_diff_s_term1 = Tex(r"9a + 3b + c - 4a - 2b - c").set_color("#116CD3").next_to(Braces[1], d_f*DOWN)
        f_diff_s_term2 = Tex(r"9a - 4a + 3b - 2b + c - c").set_color("#116CD3").next_to(Braces[1], d_f*DOWN)
        f_diff_s_term3 = Tex(r"5a + b").set_color("#116CD3").next_to(Braces[1], d_f*DOWN)
        
        self.play( Write(f_diff_text) , FadeIn(Braces[0]))
        self.play(Write(f_diff_f_term0))
        self.wait()
        self.play(f_diff_f_term0.animate.become(f_diff_f_term1))
        self.wait()
        self.play(f_diff_f_term0.animate.become(f_diff_f_term2))
        self.wait()
        self.play(f_diff_f_term0.animate.become(f_diff_f_term3))
        self.wait()
        self.play(FadeIn(Braces[1]))
        self.play(Write(f_diff_s_term0))
        self.wait()
        self.play(f_diff_s_term0.animate.become(f_diff_s_term1))
        self.wait()
        self.play(f_diff_s_term0.animate.become(f_diff_s_term2))
        self.wait()
        self.play(f_diff_s_term0.animate.become(f_diff_s_term3))
        
        Braces_2 = Brace(Line(f_diff_f_term3.get_center(), f_diff_s_term3.get_center()), DOWN, buff = 0.3).set_color("#750A0A")
        s_diff_f_term0 = Tex(r"5a + b - (3a + b)").set_color("#4DA30C").next_to(Braces_2, d_f*DOWN)
        s_diff_f_term1 = Tex(r"2a").set_color("#4DA30C").next_to(Braces_2, d_f*DOWN)
        sec_diff_text = Text("Second \nDifference", font_size = 35).set_color("#335063").next_to(s_diff_f_term0, LEFT).shift(2.9*LEFT)


        self.play(Write(sec_diff_text) , FadeIn(Braces_2))
        self.play(Write(s_diff_f_term0))
        self.play(s_diff_f_term0.animate.become(s_diff_f_term1))
        self.wait()

        highlight_constant_diff = SurroundingRectangle(s_diff_f_term1).set_color("#3D8108")
        highlight_f_diff  = SurroundingRectangle(f_diff_f_term3).set_color("#2F5BEB")
        highlight_f_sequence = SurroundingRectangle(f_term).set_color("#2D461B")

        self.play(ShowCreation(highlight_constant_diff))
        self.wait()
        self.play(ShowCreation(highlight_f_diff))
        self.wait()
        self.play(ShowCreation(highlight_f_sequence))