#!/bin/sh
#
# simple script to add and remove a cloud continuously

while true ; do
    echo '=== adding cloud99'
    if /tmp/quadsXXXX/quads/bin/quads-cli --define-cloud cloud99 --description "bogus" ; then
      :
    else
      break
    fi
    echo '=== deleting cloud99'
    if /tmp/quadsXXXX/quads/bin/quads-cli --rm-cloud cloud99 ; then
      :
    else
      break
    fi
done
