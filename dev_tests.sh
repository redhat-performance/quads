echo '------- define 3 clouds ---------------------'
quads --define-cloud cloud01 --description cloud01
quads --define-cloud cloud02 --description cloud02
quads --define-cloud cloud03 --description cloud03

echo '------- redefine cloud01 w/o force ----------'
quads --define-cloud cloud01 --description cloud01
echo '------- redefine cloud01 w/force ------------'
quads --define-cloud cloud01 --description cloud01 --force

echo '------- define hosts ------------------------'
quads --define-host host01.example.com --default-cloud cloud01 --host-type vendor
quads --define-host host02.example.com --default-cloud cloud01 --host-type vendor

echo '------- redefine host01 w/o force ----------'
quads --define-host host01.example.com --default-cloud cloud01 --host-type vendor
echo '------- redefine host01 w/force ------------'
quads --define-host host01.example.com --default-cloud cloud01 --host-type vendor --force


echo '------- list owners -------------------------'
quads --ls-owner
echo '------- list tickets ------------------------'
quads --ls-ticket
echo '------- list qinq ---------------------------'
quads --ls-qinq
echo '------- list wipe ---------------------------'
quads --ls-wipe
echo '------- list ccusers ------------------------'
quads --ls-cc-user
echo '------- list owners w/cloudonly cloud01 -----'
quads --ls-owner --cloud-only cloud01
echo '------- list tickets w/cloudonly cloud01 ----'
quads --ls-ticket --cloud-only cloud01
echo '------- list qinq  w/cloudonly cloud01 ------'
quads --ls-qinq --cloud-only cloud01
echo '------- list wipe w/cloudonly cloud01 -------'
quads --ls-wipe --cloud-only cloud01
echo '------- list ccusers w/cloudonly cloud01 ----'
quads --ls-cc-user --cloud-only cloud01


echo '------- Add schedules'
quads --add-schedule --host host01.example.com --schedule-start "2018-04-27 08:00" --schedule-end "2018-08-19 08:00" --schedule-cloud cloud01
quads --add-schedule --host host01.example.com --schedule-start "2019-04-27 08:00" --schedule-end "2019-08-19 08:00" --schedule-cloud cloud02
quads --add-schedule --host host01.example.com --schedule-start "2016-04-27 08:00" --schedule-end "2016-08-19 08:00" --schedule-cloud cloud03

echo '------- List schedules'
quads --ls-schedule --host host01.example.com

echo '------- delete schedules'
quads --rm-schedule 1 --host host01.example.com

echo '------- List schedules'
quads --ls-schedule --host host01.example.com

echo '------- delete schedules'
quads --rm-schedule 0 --host host01.example.com
quads --rm-schedule 0 --host host01.example.com

echo '------- Add interfaces'
quads --add-interface em1 --interface-mac 00:00:00:00:00:00  --interface-type test --interface-port xe-0/0/0 --host host01.example.com

echo '------- List interfaces'
quads --ls-interface --host host01.example.com

echo '------- delete interfaces'
quads --rm-interface em1 --host host01.example.com

echo '------- remove hosts and clouds -------------'
quads --rm-host host01.example.com
quads --rm-host host02.example.com
quads --rm-cloud cloud01
quads --rm-cloud cloud02
quads --rm-cloud cloud03

echo '------- remove bogus hosts and clouds -------'
quads --rm-host bogus_host
quads --rm-cloud bogus_cloud
