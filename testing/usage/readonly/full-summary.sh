#!/bin/sh
#
# simple script that contiuously does a fully-summary

while /tmp/quadsXXXX/quads/bin/quads-cli --full-summary; do
    echo '===='
done
