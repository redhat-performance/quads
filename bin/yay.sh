#!/usr/bin/sh
# yay lets you parse config values in shells scripts from
# our global ../conf/quads.yml configuration.  This lets us
# have one authoritative place for configuration across all
# tooling within QUADS.  Python has a library for this already
# so this is only needed for shell and expect.
# Original credit goes to:
# https://github.com/HumanNeuroscienceLab/gunther/blob/master/include/yay.sh

yay_parse() {

   # find input file
   for f in "$1" "$1.yay" "$1.yml"
   do
     [[ -f "$f" ]] && input="$f" && break
   done
   [[ -z "$input" ]] && exit 1

   # use given dataset prefix or imply from file name
   [[ -n "$2" ]] && local prefix="$2" || {
     local prefix=$(basename "$input"); prefix=${prefix%.*}
   }

   echo "declare -g -A $prefix;"

   local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
   sed -n -e "s|^\($s\)\($w\)$s:$s\"\(.*\)\"$s\$|\1$fs\2$fs\3|p" \
          -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p" "$input" |
   awk -F$fs '{
      indent       = length($1)/2;
      key          = $2;
      value        = $3;

      # No prefix or parent for the top level (indent zero)
      root_prefix  = "'$prefix'_";
      if (indent ==0 ) {
        prefix = "";          parent_key = "'$prefix'";
      } else {
        prefix = root_prefix; parent_key = keys[indent-1];
      }

      keys[indent] = key;

      # remove keys left behind if prior row was indented more than this row
      for (i in keys) {if (i > indent) {delete keys[i]}}

      if (length(value) > 0) {
         # value
         printf("%s%s[%s]=\"%s\";\n", prefix, parent_key , key, value);
         printf("%s%s[keys]+=\" %s\";\n", prefix, parent_key , key);
      } else {
         # collection
         printf("%s%s[children]+=\" %s%s\";\n", prefix, parent_key , root_prefix, key);
         printf("declare -g -A %s%s;\n", root_prefix, key);
         printf("%s%s[parent]=\"%s%s\";\n", root_prefix, key, prefix, parent_key);
      }
   }'
}

# helper to load yay data file
yay() { eval $(yay_parse "$@"); }
