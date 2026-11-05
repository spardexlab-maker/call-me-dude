#!/usr/bin/env bash
# Rebuild all 6 CV designs (docx + pdf) into designs/. Fonts must be installed first:
#   python3 font_prep/build_fonts.py <dir with extracted @fontsource packages>
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p designs
cd templates
python3 t1_standard.py ../designs/CV_Design1_Standard.docx
python3 t2_banner.py   ../designs/CV_Design2_Banner.docx
python3 t3_classic.py  ../designs/CV_Design3_Classic.docx
python3 t4_sidebar.py  ../designs/CV_Design4_Sidebar.docx
python3 t5_timeline.py ../designs/CV_Design5_Timeline.docx
python3 t6_framed.py   ../designs/CV_Design6_Framed.docx
cd ../designs
for f in CV_Design*.docx; do soffice --headless --convert-to pdf "$f" >/dev/null 2>&1; done
