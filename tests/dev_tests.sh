echo '------- determine QUADS version -------------'
docker exec quads bin/quads-cli --version

echo '------- define 3 clouds ---------------------'
docker exec quads bin/quads-cli --define-cloud cloud01 --description cloud01 --cloud-owner quads
docker exec quads bin/quads-cli --define-cloud cloud02 --description cloud02 --cloud-owner quads
docker exec quads bin/quads-cli --define-cloud cloud03 --description cloud03 --cloud-owner quads --cc-users "cc1 cc2"

echo '------- redefine cloud01 w/o force ----------'
docker exec quads bin/quads-cli --define-cloud cloud01 --description cloud01
echo '------- redefine cloud01 w/force ------------'
docker exec quads bin/quads-cli --define-cloud cloud01 --description cloud01 --force

echo '------- define hosts ------------------------'
docker exec quads bin/quads-cli --define-host host01.example.com --default-cloud cloud01 --host-type vendor
docker exec quads bin/quads-cli --define-host host02.example.com --default-cloud cloud01 --host-type vendor

echo '------- redefine host01 w/o force ----------'
docker exec quads bin/quads-cli --define-host host01.example.com --default-cloud cloud01 --host-type vendor
echo '------- redefine host01 w/force ------------'
docker exec quads bin/quads-cli --define-host host01.example.com --default-cloud cloud01 --host-type vendor --force


echo '------- list owners -------------------------'
docker exec quads bin/quads-cli --ls-owner
echo '------- list tickets ------------------------'
docker exec quads bin/quads-cli --ls-ticket
echo '------- list qinq ---------------------------'
docker exec quads bin/quads-cli --ls-qinq
echo '------- list wipe ---------------------------'
docker exec quads bin/quads-cli --ls-wipe
echo '------- list ccusers ------------------------'
docker exec quads bin/quads-cli --ls-cc-user
echo '------- list owners w/cloudonly cloud01 -----'
docker exec quads bin/quads-cli --ls-owner --cloud-only cloud01
echo '------- list tickets w/cloudonly cloud01 ----'
docker exec quads bin/quads-cli --ls-ticket --cloud-only cloud01
echo '------- list qinq  w/cloudonly cloud01 ------'
docker exec quads bin/quads-cli --ls-qinq --cloud-only cloud01
echo '------- list wipe w/cloudonly cloud01 -------'
docker exec quads bin/quads-cli --ls-wipe --cloud-only cloud01
echo '------- list ccusers w/cloudonly cloud01 ----'
docker exec quads bin/quads-cli --ls-cc-user --cloud-only cloud01


echo '------- Add schedules'
docker exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2018-04-27 08:00" --schedule-end "2018-08-19 08:00" --schedule-cloud cloud01
docker exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2019-04-27 08:00" --schedule-end "2019-08-19 08:00" --schedule-cloud cloud02
docker exec quads bin/quads-cli --add-schedule --host host01.example.com --schedule-start "2016-04-27 08:00" --schedule-end "2016-08-19 08:00" --schedule-cloud cloud03

echo '------- List schedules'
docker exec quads bin/quads-cli --ls-schedule --host host01.example.com

echo '------- delete schedules'
docker exec quads bin/quads-cli --rm-schedule 1 --host host01.example.com

echo '------- List schedules'
docker exec quads bin/quads-cli --ls-schedule --host host01.example.com

echo '------- delete schedules'
docker exec quads bin/quads-cli --rm-schedule 0 --host host01.example.com
docker exec quads bin/quads-cli --rm-schedule 0 --host host01.example.com

echo '------- Add interfaces'
docker exec quads bin/quads-cli --add-interface em1 --interface-mac 00:00:00:00:00:00  --interface-switch-ip 10.12.67.247 --interface-port xe-0/0/0 --host host01.example.com

echo '------- List interfaces'
docker exec quads bin/quads-cli --ls-interface --host host01.example.com

echo '------- delete interfaces'
docker exec quads bin/quads-cli --rm-interface em1 --host host01.example.com

echo '------- remove hosts and clouds -------------'
docker exec quads bin/quads-cli --rm-host host01.example.com
docker exec quads bin/quads-cli --rm-host host02.example.com
docker exec quads bin/quads-cli --rm-cloud cloud01
docker exec quads bin/quads-cli --rm-cloud cloud02
docker exec quads bin/quads-cli --rm-cloud cloud03

echo '------- remove bogus hosts and clouds -------'
docker exec quads bin/quads-cli --rm-host bogus_host
docker exec quads bin/quads-cli --rm-cloud bogus_cloud
