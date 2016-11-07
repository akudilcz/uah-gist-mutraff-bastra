!/bin/bash

# -----------------------------------------------------------------------
# GRID SCENARIOS
# -----------------------------------------------------------------------

# --- NO BASTRA: no MAPS applied
generate_scene.sh canogrid_noBastra_nomaps_randomtraffic.param
generate_scene.sh canogrid_noBastra_nomaps_dirtraffic.param
generate_scene.sh canogrid_noBastra_nomaps_fulltraffic.param

# --- BASTRA: no MAPS applied <-- THIS SHOULD BE IRRELEVANT
# generate_scene.sh canogrid_Bastra_logit05_nomaps_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit05_nomaps_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit10_nomaps_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit10_nomaps_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit20_nomaps_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit20_nomaps_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit50_nomaps_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit50_nomaps_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit100_nomaps_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit100_nomaps_fulltraffic.param

# --- BASTRA: rand05x1-timeALL MAPS applied
# 1MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh canogrid_Bastra_logit05_rand05x1-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand05x1-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x1-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x1-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x1-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x1-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x1-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x1-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x1-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x1-timeALL_fulltraffic.param

# --- BASTRA: rand05x2-timeALL MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh canogrid_Bastra_logit05_rand05x2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand05x2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x2-timeALL_fulltraffic.param

# --- BASTRA: rand05x4-timeALL MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh canogrid_Bastra_logit05_rand05x4-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand05x4-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x4-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x4-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x4-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x4-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x4-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x4-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x4-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x4-timeALL_fulltraffic.param

# --- BASTRA: rand05x8-timeALL MAPS applied
# 8MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh canogrid_Bastra_logit05_rand05x8-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand05x8-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x8-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x8-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x8-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x8-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x8-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x8-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x8-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x8-timeALL_fulltraffic.param

# --- BASTRA: rand05x2-time2000 MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh canogrid_Bastra_logit05_rand05x2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand05x2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x2-time2000_fulltraffic.param

# --- BASTRA: rand05x4-time2000 MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh canogrid_Bastra_logit05_rand05x4-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand05x4-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x4-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand05x4-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x4-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand05x4-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x4-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand05x4-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x4-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand05x4-time2000_fulltraffic.param

# --- BASTRA: rand2-timeALL MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh canogrid_Bastra_logit05_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-timeALL_fulltraffic.param

# --- BASTRA: rand2-timeALL MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh canogrid_Bastra_logit05_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-timeALL_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-timeALL_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-timeALL_fulltraffic.param

# --- BASTRA: rand2-time2000 MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh canogrid_Bastra_logit05_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-time2000_fulltraffic.param

# --- BASTRA: rand2-time2000 MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh canogrid_Bastra_logit05_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit05_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit10_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit20_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit50_rand2-time2000_fulltraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-time2000_randomtraffic.param
generate_scene.sh canogrid_Bastra_logit100_rand2-time2000_fulltraffic.param

# --- BASTRA: Directed Penalty Maps
# generate_scene.sh canogrid_noBastra_directedPenalty_randomtraffic.param
# generate_scene.sh canogrid_noBastra_directedPenalty_dirtraffic.param
# generate_scene.sh canogrid_noBastra_directedPenalty_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit10_directedPenalty_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit10_directedPenalty_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit20_directedPenalty_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit20_directedPenalty_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit50_directedPenalty_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit50_directedPenalty_fulltraffic.param
# generate_scene.sh canogrid_Bastra_logit100_directedPenalty_randomtraffic.param
# generate_scene.sh canogrid_Bastra_logit100_directedPenalty_fulltraffic.param


# -----------------------------------------------------------------------
# RADIAL/SPIDER SCENARIOS
# -----------------------------------------------------------------------

# --- NO BASTRA: no MAPS applied
generate_scene.sh radial_noBastra_nomaps_randomtraffic.param
generate_scene.sh radial_noBastra_nomaps_dirtraffic.param
generate_scene.sh radial_noBastra_nomaps_fulltraffic.param

# --- BASTRA: no MAPS applied <-- THIS SHOULD BE IRRELEVANT
# generate_scene.sh radial_Bastra_logit100_nomaps_randomtraffic.param
# generate_scene.sh radial_Bastra_logit100_nomaps_fulltraffic.param
# generate_scene.sh radial_Bastra_logit10_nomaps_randomtraffic.param
# generate_scene.sh radial_Bastra_logit10_nomaps_fulltraffic.param
# generate_scene.sh radial_Bastra_logit20_nomaps_randomtraffic.param
# generate_scene.sh radial_Bastra_logit20_nomaps_fulltraffic.param
# generate_scene.sh radial_Bastra_logit50_nomaps_randomtraffic.param
# generate_scene.sh radial_Bastra_logit50_nomaps_fulltraffic.param

# --- BASTRA: rand05x1-timeALL MAPS applied
# 1MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh radial_Bastra_logit05_rand05x1-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand05x1-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x1-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x1-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x1-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x1-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x1-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x1-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x1-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x1-timeALL_fulltraffic.param

# --- BASTRA: rand05x2-timeALL MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh radial_Bastra_logit05_rand05x2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand05x2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x2-timeALL_fulltraffic.param

# --- BASTRA: rand05x4-timeALL MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh radial_Bastra_logit05_rand05x4-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand05x4-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x4-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x4-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x4-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x4-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x4-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x4-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x4-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x4-timeALL_fulltraffic.param

# --- BASTRA: rand05x8-timeALL MAPS applied
# 8MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh radial_Bastra_logit05_rand05x8-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand05x8-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x8-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x8-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x8-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x8-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x8-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x8-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x8-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x8-timeALL_fulltraffic.param

# --- BASTRA: rand05x2-time2000 MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh radial_Bastra_logit05_rand05x2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand05x2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x2-time2000_fulltraffic.param

# --- BASTRA: rand05x4-time2000 MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh radial_Bastra_logit05_rand05x4-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand05x4-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x4-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand05x4-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x4-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand05x4-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x4-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand05x4-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x4-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand05x4-time2000_fulltraffic.param

# --- BASTRA: rand2-timeALL MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh radial_Bastra_logit05_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-timeALL_fulltraffic.param

# --- BASTRA: rand2-timeALL MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied all the sim time.
generate_scene.sh radial_Bastra_logit05_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-timeALL_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-timeALL_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-timeALL_fulltraffic.param

# --- BASTRA: rand2-time2000 MAPS applied
# 2MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh radial_Bastra_logit05_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-time2000_fulltraffic.param

# --- BASTRA: rand2-time2000 MAPS applied
# 4MAP with random weigths with 0.5 Normal deviation, applied from 2000 Time
generate_scene.sh radial_Bastra_logit05_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit05_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit10_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit20_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit50_rand2-time2000_fulltraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-time2000_randomtraffic.param
generate_scene.sh radial_Bastra_logit100_rand2-time2000_fulltraffic.param

# --- BASTRA: Directed Penalty Maps
# generate_scene.sh radial_noBastra_directedPenalty_randomtraffic.param
# generate_scene.sh radial_noBastra_directedPenalty_dirtraffic.param
# generate_scene.sh radial_noBastra_directedPenalty_fulltraffic.param
# generate_scene.sh radial_Bastra_logit10_directedPenalty_randomtraffic.param
# generate_scene.sh radial_Bastra_logit10_directedPenalty_fulltraffic.param
# generate_scene.sh radial_Bastra_logit20_directedPenalty_randomtraffic.param
# generate_scene.sh radial_Bastra_logit20_directedPenalty_fulltraffic.param
# generate_scene.sh radial_Bastra_logit50_directedPenalty_randomtraffic.param
# generate_scene.sh radial_Bastra_logit50_directedPenalty_fulltraffic.param
# generate_scene.sh radial_Bastra_logit100_directedPenalty_randomtraffic.param
# generate_scene.sh radial_Bastra_logit100_directedPenalty_fulltraffic.param
