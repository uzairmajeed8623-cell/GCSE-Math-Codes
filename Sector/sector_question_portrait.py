from email import header
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manimlib import *
from sector_common import build_border, build_question_text, build_diagram, lay_out_side_by_side, build_header

# ------------------------------------------------------------------
# Portrait (YouTube Shorts) version of the OAB sector question.
# Sector diagram sits upper-RIGHT, question text sits upper-LEFT,
# side by side, both anchored to the top of the frame - leaving the
# lower portion of the screen empty for the solution scene to use.
#
# Render with a portrait resolution, e.g.:
#   manimgl sector_question_portrait.py SectorReflexAngleQuestionPortrait -r "1080x1920" -w
#
# This file depends on sector_common.py living in the same folder.
# ------------------------------------------------------------------


class SectorReflexAngleQuestionPortrait(InteractiveScene):
    samples = 4

    def construct(self):
        self.set_background_color(WHITE)

        border = build_border()
        header = build_header(border)
        self.add(border)
        self.add(header)          # or self.play(FadeIn(header)) if you want it animated in
        qt = build_question_text()
        dg = build_diagram()
        lay_out_side_by_side(qt.group, dg.group, border)

        # ------------------------------------------------------------------
        # Reveal
        # ------------------------------------------------------------------
        self.play(Write(qt.stem_block))
        self.wait()

        self.play(ShowCreation(dg.sector_arc))
        self.play(ShowCreation(dg.radius_OA), ShowCreation(dg.radius_OB),
                   FadeIn(dg.sector_dots))
        self.play(
            LaggedStart(*[Write(l) for l in dg.sector_labels], lag_ratio=0.2),
            Write(dg.radius_label),
        )
        self.wait()

        self.play(Write(qt.perimeter_block))
        self.wait()

        self.play(Write(qt.find_block))
        self.play(Write(qt.round_block))
        self.wait(2)