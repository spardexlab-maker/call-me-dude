# -*- coding: utf-8 -*-
"""English version of the CV content — a faithful translation of content.py.

Same structure as content.py so templates can switch language by import.
Place names use common English transliterations.
"""
from content import (PHONE, EMAIL, EMAIL2, N_DONE, N_ONGOING, N_TOTAL)

NAME = "Ali Obais Habib"
TITLE = "Consultant Mechanical Engineer  |  Chairman of the Board & General Manager of Executive Projects"
LOCATION = "Republic of Iraq"

SUMMARY = (
    "Consultant Mechanical Engineer with over 30 years of professional and executive experience in "
    "mechanical engineering and in managing and directing major construction and industrial projects in "
    "Iraq. Holds a strong track record that includes delivering a broad portfolio of fully completed "
    "projects, alongside leading strategic ongoing projects in infrastructure (wastewater treatment plants, "
    "water supply and pumping stations), major teaching hospitals, residential towers and complexes, and "
    "bridge and urban road projects. Combines senior leadership as Chairman of the Board of \"Al-Nama Group "
    "for Investment and Industrial Development\" with comprehensive central management of all strategic "
    "projects at \"Al-Ezza Group for Contracting and Investments\", in addition to managing national "
    "investment partnerships."
)

DONE_WATER = [
    "Tuwairij Central Sewage Treatment Plant (Holy Karbala Governorate)",
    "Al-Shamiya Sewage Treatment Plant (Al-Diwaniyah Governorate)",
    "Al-Rumaitha Sewage Treatment Plant (Al-Muthanna Governorate)",
    "Karbala Central Sewerage Networks and Stations Project (Completed Phase)",
    "Ghammas Water Project and Associated Pumping Stations (Al-Diwaniyah Governorate)",
    "Water and Infrastructure Project in Asmaa Al-Zuhoor",
]
DONE_BRIDGES = [
    "Nader Overpass Project, Hillah City (Babylon Governorate)",
    "Al-Butaira Concrete Overpass Project (Maysan Governorate)",
]
ONGOING_INFRA = [
    "Kubaisa District Sewerage Networks and Stations Project (Al-Anbar Governorate)",
    "Sab' Al-Bour Sewerage Networks and Treatment Plant Project (Baghdad Governorate)",
    "Anah District Sewerage Networks and Stations Project (Al-Anbar Governorate)",
    "Al-Musayyib Water Project with Pumping and Distribution Stations (Babylon Governorate)",
    "Al-Khalis Sewerage Networks and Treatment Plant Project (Diyala Governorate)",
    "West Baqubah Sewerage Networks and Station Project (Diyala Governorate)",
    "Ali Al-Sharqi District Sewerage Networks Project (Maysan Governorate)",
    "Integrated Infrastructure and Services Projects for Al-Hawraa District (Phases 1 and 2), "
    "Kut City (Wasit Governorate)",
]
ONGOING_HOUSING = [
    "Al-Ezza Residential Complex, Maysan Governorate (3,000 housing units with full infrastructure and services)",
    "Al-Firdaws Residential Investment Complex, Holy Karbala (multi-storey buildings and complexes)",
    "Al-Sahab Residential Tower Project, Holy Karbala (multi-storey tower)",
    "Baghdad Dream Towers Project, Baghdad (integrated residential complexes and hotel towers)",
]
ONGOING_HEALTH = [
    "Karbala Specialized Obstetrics and Gynecology Hospital (300-bed capacity)",
    "Kirkuk General Hospital (400-bed capacity)",
    "Al-Shaheed Al-Sadr Hospital, Al-Najaf Al-Ashraf Governorate",
    "Al-Sadr Hospital, Maysan Governorate",
    "Al-Rahmaniya Hospital, Al-Shuala (100-bed capacity – Baghdad)",
]

PORTFOLIO = [
    ("First: Completed Projects", None),
    ("Completed Wastewater Treatment and Water Projects", DONE_WATER),
    ("Completed Bridges, Roads and Urban Construction Works", DONE_BRIDGES),
    ("Second: Ongoing Strategic Projects (Under Implementation and Development)", None),
    ("Integrated Sewerage Networks and Infrastructure Projects", ONGOING_INFRA),
    ("Residential Development and High-Rise Towers", ONGOING_HOUSING),
    ("Buildings and Healthcare Projects", ONGOING_HEALTH),
]

STATS = [("30+", "Years of experience"), (str(N_TOTAL), "Strategic projects"),
         (str(N_DONE), "Completed projects"), (str(N_ONGOING), "Ongoing projects")]

COMPETENCIES = [
    ("Strategic Management and Leadership",
     "Managing and directing mega construction and electromechanical projects (Megaprojects), leading "
     "alliances and partnerships, supply chain management, operational planning and budget estimation"),
    ("Negotiation and Contract Management",
     "Advanced negotiation techniques, management of engineering and commercial contracts, resolution of "
     "contractual disputes, and management of FIDIC contracts and investment partnerships"),
    ("Specialized Engineering Software",
     "AutoCAD for preparing and reviewing engineering, mechanical and construction drawings and designs"),
    ("Administrative and Office Software",
     "Professional proficiency in Microsoft Office (including Word, Excel, PowerPoint, Project) for "
     "technical reporting, scheduling and data management"),
]

SKILL_TAGS = ["Megaprojects Management", "Alliances and Partnerships", "Supply Chain Management",
              "Operational Planning and Budgeting", "Advanced Negotiation",
              "Engineering and Commercial Contracts", "FIDIC Contracts", "Contractual Dispute Resolution",
              "AutoCAD", "Microsoft Office", "Microsoft Project"]

ROLES = [
    {
        "title": "Chairman of the Board",
        "org": "Al-Nama Group for Investment and Industrial Development (Industrial and Investment Sector)",
        "dates": "2019 – Present",
        "bullets": [
            (None, "Set the strategic plans and provided overall supervision of establishing and managing "
                   "the Group's integrated industrial portfolio, which includes:"),
            ("Glass Fiber Reinforced Concrete (GRC) Plants",
             "Supervising the manufacture of complex architectural moulds and modern engineered façades"),
            ("Concrete and Cement Products Plants",
             "Managing automated production lines for interlocking pavers, curbstones and Shtaiker units "
             "for urban and residential projects"),
            ("Industrial Alcohol and Solvents Plants",
             "Operating distillation and chemical distribution lines for specialized and industrial purposes"),
            ("Plastics Manufacturing Plants",
             "Producing and supplying plastic materials and accessories for construction projects and "
             "specialized applications"),
            ("Central Workshops and Electrical Departments",
             "Supervising assembly and mechanical and electrical maintenance workshops, and the manufacture "
             "of industrial control panels"),
        ],
        "groups": [],
    },
    {
        "title": "General Manager of Projects",
        "org": "Al-Ezza Group for Contracting and Investments",
        "dates": "2004 – Present",
        "bullets": [
            (None, "Executive leadership and comprehensive engineering and administrative supervision of the "
                   "Group's strategic project portfolio across the governorates of Iraq, classified by "
                   "operational status"),
            (None, f"The portfolio comprises {N_TOTAL} projects: {N_DONE} completed and {N_ONGOING} ongoing "
                   "and under development"),
        ],
        "groups": PORTFOLIO,
    },
    {
        "title": "Technical Project Manager – Karbala Sewage Treatment Plants",
        "org": "Al-Ezza Group",
        "dates": "2008 – 2012",
        "bullets": [
            (None, "Direct field and technical supervision of the supply, installation and testing of "
                   "mechanical and hydraulic systems, lifting stations and central treatment facilities"),
            (None, "Leading technical teams, conducting operational tests and the final handover of the project"),
        ],
        "groups": [],
    },
]

PARTNERSHIP = {
    "title": "Board Member and Shareholding Partner",
    "org": "Noor Al-Sibtain Mill",
    "text": "\"Noor Al-Sibtain Mill\" investment project for grain production and securing food security, "
            "in partnership with the Imam Hussain Holy Shrine",
}

EDUCATION = {"degree": "B.Sc. in Mechanical Engineering", "school": "University of Technology — Baghdad, Iraq",
             "year": "Class of 1994"}

LANGUAGES = [("Arabic", "Native language (full proficiency in speaking and writing)"),
             ("English", "Professional second language (full proficiency in engineering dealings, "
                         "correspondence and technical negotiations)")]
