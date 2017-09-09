#!/bin/sh
#
# simple test script to add and remove a host schedule
#


while true ; do
    echo '=== adding host schedule to host01.example.com'
    if /tmp/quadsXXXX/quads/bin/quads-cli --host host01.example.com \
      --add-schedule --schedule-start '2017-10-01 22:00' \
                     --schedule-end   '2017-10-30 22:00' \
                     --schedule-cloud cloud02 ; then
      :
    else
      break
    fi
    echo '=== deleting host schedule from host01.example.com'
    if /tmp/quadsXXXX/quads/bin/quads-cli --host host01.example.com \
      --rm-schedule 0 ; then
      :
    else
      break
    fi
done
