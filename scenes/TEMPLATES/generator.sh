#!/bin/bash

# -----------------------------------------------------------------------
# Create param_file
#	Param_file: canogrid_Bastra_logit05_rand05x2-timeALL_fulltraffic
# -----------------------------------------------------------------------
function params_create() {
  p_net_name="$1"
  p_bastra="$2"
  p_map="$3"
  p_traffic="$4"
  p_logit="$5"

  p_roadlen="50"
  p_lanes="1"
  p_maxspeed="13.9"
  p_time_ini="0"
  p_time_end="4000"
  p_map_ini="0"
  p_map_end="10000"
  p_traffic_rand="3000"
  p_traffic_dir="200"
  p_grid_size="0"
  p_spider_arms="0"
  p_spider_circ="0"
  p_use_bastra="false"
  p_fore_steps="0"
  p_fore_tries="0"
  p_fore_halt="0"
  p_fore_penalty="1"

  # ----------------
  case "$p_net_name" in
    grid16)	p_grid_size="16"
		p_net_type="grid"
    		;;
    radial16)	p_spider_arms="16"
    		p_spider_circ="16"
		p_net_type="radial"
		;;
  esac

  # ----------------
  case "$p_traffic" in
    randomtraffic)	p_traffic_rand="3000"
			p_traffic_dir="0"
    			;;
    dirtraffic)		p_traffic_rand="0"
			p_traffic_dir="200"
    			;;
    fulltraffic)	p_traffic_rand="3000"
			p_traffic_dir="200"
    			;;
  esac

  # ----------------
  if [[ "$p_map" =~ .*time([0-9]+).* ]]
  then
    p_map_ini="${BASH_REMATCH[1]}"
  fi

  # ----------------
  if [ "$p_bastra" == "Bastra" ]
  then
    p_prefix="${p_net_name}_${p_bastra}_${p_map}_${p_traffic}_logit${p_logit}"
    p_use_bastra="true"
  else
    p_prefix="${p_net_name}_${p_bastra}_${p_map}_${p_traffic}"
    p_logit="1"
  fi

  # ----------------
  p_filename="param/${p_prefix}.param"
  echo "Creating $p_filename"
  echo "# generate_scene.sh $p_filename" >> $p_index_tmp
cat <<EOF > $p_filename
#!/bin/bash
export __PREFIX="${p_prefix}"
export __TRAFFIC_TYPE="$p_traffic"
export __USE_BASTRA="$p_bastra"
export __MAP_USAGE="$p_map"
export __MAP_TIME_INI="$p_map_ini"
export __MAP_TIME_END="$p_map_end"
export __NET_NAME="$p_net_name"
export __ROADLENGTH="$p_roadlen"
export __NET_TYPE="$p_net_type"
export __LANES="$p_lanes"
export __MAX_SPEED="$p_maxspeed"
export __SIMUL_TIME_INI="$p_time_ini"
export __SIMUL_TIME_END="$p_time_end"
export __TRAFFIC_BASELINE="$p_traffic_rand"
export __TRAFFIC_BRANCH="$p_traffic_dir"
export __GRID_SIZE="$p_grid_size"
export __SPIDER_ARMS="$p_spider_arms"
export __SPIDER_CIRCLES="$p_spider_circ"
export __BASTRA_USE_BALANCE="$p_use_bastra"
export __BASTRA_LOGIT="$p_logit"
export __BASTRA_FORESIGHT_STEPS="$p_fore_steps"
export __BASTRA_FORESIGHT_TRIES="$p_fore_tries"
export __BASTRA_FORESIGHT_HALTING="$p_fore_halt"
export __BASTRA_FORESIGHT_PENALTY="$p_fore_penalty"
EOF
}

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
NETWORK_TYPES="grid16 radial16"
MAP_TYPES="\
nomaps directedPenalty reference \
rand05x1_timeALL rand05x2_timeALL rand05x4_timeALL rand05x8_timeALL \
rand05x2_time2000 rand05x4_time2000 \
rand2x2_timeALL rand2x4_timeALL rand2x2_time2000 rand2x4_time2000 \
"
TRAFFIC_TYPES="randomtraffic dirtraffic fulltraffic"
LOGIT="05 10 20 50 100"
BASTRA="noBastra Bastra"

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
p_index="param/index.out"
p_index_tmp="/tmp/index.tmp"
cat <<EOF > $p_index
# -------------------
# Scene params created on `date`
EOF
for NetworkType in ${NETWORK_TYPES}
do
  for Bastra in ${BASTRA}
  do
    cat <<EOF >> $p_index
# -----------------------------------
# NETWORK ${NetworkType} - ${Bastra}
# -----------------------------------
EOF
    > $p_index_tmp
    for Map in ${MAP_TYPES}
    do
      for Traffic in ${TRAFFIC_TYPES}
      do
        for Logit in ${LOGIT}
        do
		params_create $NetworkType $Bastra $Map $Traffic $Logit
        done
      done
    done
    sort -u $p_index_tmp >> $p_index
  done
done

echo "Generated $p_index"
