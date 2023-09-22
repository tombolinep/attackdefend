# attackdefend

cd C:\Users\peter\IdealProjects\attackdefend\src

pyinstaller --name dobnob --add-data "assets;assets" main.py

import pstats
stats = pstats.Stats('profile_result.out')
stats.sort_stats('cumulative')
stats.print_stats()
