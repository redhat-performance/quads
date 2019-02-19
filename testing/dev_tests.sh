echo '------- define 3 clouds ---------------------'
../bin/quads-cli --define-cloud cloud01 --description cloud01
../bin/quads-cli --define-cloud cloud02 --description cloud02
../bin/quads-cli --define-cloud cloud03 --description cloud03

echo '------- redefine cloud01 w/o force ----------'
../bin/quads-cli --define-cloud cloud01 --description cloud01
echo '------- redefine cloud01 w/force ------------'
../bin/quads-cli --define-cloud cloud01 --description cloud01 --force

echo '------- define hosts ------------------------'
../bin/quads-cli --define-host host01.example.com --default-cloud cloud01 --host-type vendor
../bin/quads-cli --define-host host02.example.com --default-cloud cloud01 --host-type vendor

echo '------- redefine host01 w/o force ----------'
../bin/quads-cli --define-host host01.example.com --default-cloud cloud01 --host-type vendor
echo '------- redefine host01 w/force ------------'
../bin/quads-cli --define-host host01.example.com --default-cloud cloud01 --host-type vendor --force


echo '------- list owners -------------------------'
../bin/quads-cli --ls-owner
echo '------- list tickets ------------------------'
../bin/quads-cli --ls-ticket
echo '------- list qinq ---------------------------'
../bin/quads-cli --ls-qinq
echo '------- list wipe ---------------------------'
../bin/quads-cli --ls-wipe
echo '------- list ccusers ------------------------'
../bin/quads-cli --ls-cc-user
echo '------- list owners w/cloudonly cloud01 -----'
../bin/quads-cli --ls-owner --cloud-only cloud01
echo '------- list tickets w/cloudonly cloud01 ----'
../bin/quads-cli --ls-ticket --cloud-only cloud01
echo '------- list qinq  w/cloudonly cloud01 ------'
../bin/quads-cli --ls-qinq --cloud-only cloud01
echo '------- list wipe w/cloudonly cloud01 -------'
../bin/quads-cli --ls-wipe --cloud-only cloud01
echo '------- list ccusers w/cloudonly cloud01 ----'
../bin/quads-cli --ls-cc-user --cloud-only cloud01


echo '------- Add schedules'
../bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2018-04-27 08:00" --schedule-end "2018-08-19 08:00" --schedule-cloud cloud01
../bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2019-04-27 08:00" --schedule-end "2019-08-19 08:00" --schedule-cloud cloud02
../bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2016-04-27 08:00" --schedule-end "2016-08-19 08:00" --schedule-cloud cloud03

echo '------- List schedules'
../bin/quads-cli --ls-schedule --host host01.example.com

echo '------- delete schedules'
../bin/quads-cli --rm-schedule 1 --host host01.example.com

echo '------- List schedules'
../bin/quads-cli --ls-schedule --host host01.example.com

echo '------- delete schedules'
../bin/quads-cli --rm-schedule 0 --host host01.example.com
../bin/quads-cli --rm-schedule 0 --host host01.example.com

echo '------- Add interfaces'
../bin/quads-cli --add-interface em1 --interface-mac 00:00:00:00:00:00  --interface-type test --interface-port xe-0/0/0 --host host01.example.com

echo '------- List interfaces'
../bin/quads-cli --ls-interface --host host01.example.com

echo '------- delete interfaces'
../bin/quads-cli --rm-interface em1 --host host01.example.com

echo '------- remove hosts and clouds -------------'
../bin/quads-cli --rm-host host01.example.com
../bin/quads-cli --rm-host host02.example.com
../bin/quads-cli --rm-cloud cloud01
../bin/quads-cli --rm-cloud cloud02
../bin/quads-cli --rm-cloud cloud03

echo '------- remove bogus hosts and clouds -------'
../bin/quads-cli --rm-host bogus_host
../bin/quads-cli --rm-cloud bogus_cloud
