#!/usr/bin/env bash
# Rebuild every CV design (docx + pdf). Fonts must be installed first:
#   python3 font_prep/build_fonts.py <dir with extracted @fontsource packages>
set -euo pipefail
cd "$(dirname "$0")"
python3 build_cv.py CV_Ali_Obais_Habib.docx
soffice --headless --convert-to pdf CV_Ali_Obais_Habib.docx >/dev/null
mkdir -p designs
cd templates
python3 t2_banner.py   ../designs/CV_Design2_Banner.docx
python3 t3_classic.py  ../designs/CV_Design3_Classic.docx
python3 t4_sidebar.py  ../designs/CV_Design4_Sidebar.docx
python3 t5_timeline.py ../designs/CV_Design5_Timeline.docx
cd ../designs
for f in *.docx; do soffice --headless --convert-to pdf "$f" >/dev/null; done
