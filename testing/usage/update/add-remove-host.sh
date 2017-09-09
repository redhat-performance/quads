
    while true ; do echo ==== adding foo
      if /tmp/quadsXXXX/quads/bin/quads-cli --define-host foo.example.com \
                                           --host-type none \
                                           --default-cloud cloud01; then
        sleep $((1 + RANDOM % 5))
      else
        break
      fi
      echo ==== deleting foo
      if /tmp/quadsXXXX/quads/bin/quads-cli --rm-host foo.example.com
      then
        sleep $((1 + RANDOM % 5))
      else
        break
      fi
    done
